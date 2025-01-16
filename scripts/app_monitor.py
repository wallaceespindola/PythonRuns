import argparse
import logging
import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv

# ========== Start Log Configs ==========

# Set up logging to file and console
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler for logging to a file
file_handler = logging.FileHandler("app_monitor.log")
file_handler.setLevel(logging.INFO)

# Console handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define a logging format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ========== End Log Configs ==========

# Expected HTTP response status code
EXPECTED_STATUS = 200

# ========== Start Email Configs ==========

# Load environment variables from .env file
load_dotenv()

# Email configuration, from environment variables
EMAIL_SUBJECT = "Alert: one or more URLs are down"
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

# ========== End Email Configs ==========

# List of URLs to check
URLS = [
    "http://195.31.150.176:3000/",
    "http://195.31.150.176:8000/",
]


def check_url(url):
    """
    Checks the URL to ensure it returns the expected HTTP status.
    """
    try:
        logger.info(f"Checking URL: {url}")
        response = requests.get(url, timeout=10)
        if response.status_code == EXPECTED_STATUS:
            logger.info(f"OK: {url} is online - status code {response.status_code}.")
            return True
        else:
            logger.warning(f"URL {url} returned status code {response.status_code}, expected {EXPECTED_STATUS}.")
            return False
    except requests.exceptions.RequestException as e:
        if "NameResolutionError" in str(e):
            logger.error(f"DNS resolution failed for {url}. Skipping restart.")
        else:
            logger.error(f"Error checking URL {url}: {e}")
        return False


def restart_apache():
    """
    Restarts the Apache server using systemctl.
    """
    logger.info("========== Restarting Apache server... ==========")
    try:
        subprocess.run(["sudo", "systemctl", "restart", "apache2"], check=True)
        logger.info("Apache server restarted successfully.")
    except subprocess.CalledProcessError as e:
        logger.error("Failed to restart Apache server: %s", e)


def restart_python_apps():
    """
    Calls the script to restart Python applications.
    """
    logger.info("========== Restarting Python applications... ==========")
    try:
        start_script = "/root/scripts/start_apps.sh"
        if os.path.exists(start_script):
            subprocess.run(["/bin/bash", start_script], check=True)
            logger.info("Python applications restarted successfully.")
        else:
            logger.error("Failed to restart Python applications: %s script not found.", start_script)
    except subprocess.CalledProcessError as e:
        logger.error("Failed to restart Python applications: %s", e)


def send_email(message):
    """
    Sends an email with the specified message.
    """
    logger.info("========== Sending notification email... ==========")
    # Validate email configuration
    missing_vars = []
    for var_name, var_value in [
        ("SMTP_USERNAME", SMTP_USERNAME),
        ("SMTP_PASSWORD", SMTP_PASSWORD),
        ("EMAIL_FROM", EMAIL_FROM),
        ("EMAIL_TO", EMAIL_TO),
    ]:
        if not var_value:
            missing_vars.append(var_name)
    if missing_vars:
        logger.error(f"Missing environment variables for email: {', '.join(missing_vars)}")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = EMAIL_SUBJECT
        msg.attach(MIMEText(message, "plain", "utf-8"))

        logger.debug("Email From: %s", EMAIL_FROM)
        logger.debug("Email To: %s", EMAIL_TO)
        logger.debug("Email Subject:%s", EMAIL_SUBJECT)
        logger.debug("Email Content:%s", message)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # Initiates ESMTP communication and gets the server capabilities.
            server.starttls()  # Secure the connection
            logger.info("Logging in to SMTP server...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            logger.info("Sending email...")
            server.send_message(msg)

        logger.info("Alert email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        logger.error("SMTP Authentication Error: %s", e)
    except smtplib.SMTPRecipientsRefused as e:
        logger.error("SMTP Recipients Refused: %s", e)
    except smtplib.SMTPException as e:
        logger.error("SMTP Error: %s", e)
    except Exception as e:
        logger.exception("Failed to send alert email: %s", e)


def main(restart_services, send_only_email):
    logger.info("==================================================")
    logger.info("============== Starting URL checks ===============")
    logger.info("==================================================")

    # Lists to store URLs that are up and down
    up_urls = []
    down_urls = []

    # Accumulate the check results
    for url in URLS:
        if check_url(url):
            up_urls.append(url)
        else:
            down_urls.append(url)

    # Log the results
    logger.info("========== Summary of URL checks: ==========")
    logger.info(">>> URLs that are up:")
    for url in up_urls:
        logger.info(url)

    if len(down_urls) > 0:
        logger.warning(">>> URLs that are down:")
        for url in down_urls:
            logger.warning(url)
    else:
        logger.info(">>> ALL URLS ARE OK, NOTHING DOWN. ")

    # Check if any URL checks failed
    if down_urls:
        message = f"One or more URLs are down:\n\n" + "\n".join(down_urls)
        logger.warning(message)

        # Send email if the -e or --email option is provided
        if send_only_email:
            send_email(message)

        # Restart services if the -r or --restart option is provided
        if restart_services:
            logger.warning("Restarting Apache server and Python apps as per the -r flag...")
            restart_apache()
            restart_python_apps()
            send_email(message)
    else:
        logger.info("======= All URLs are up and running correctly. =======")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Monitor URLs and optionally restart services or send email if URLs are down.",
        epilog="Example usage: python app_monitor.py -r OR python app_monitor.py -e",
    )
    parser.add_argument(
        "-r",
        "--restart",
        action="store_true",
        help="Restart Apache and Python applications if URLs are down.",
    )
    parser.add_argument(
        "-e",
        "--email",
        action="store_true",
        help="Send email notification if URLs are down without restarting services.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the main function with the restart_services and send_only_email flags
    main(restart_services=args.restart, send_only_email=args.email)
