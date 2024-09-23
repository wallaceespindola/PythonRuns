import argparse
import logging
import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv

# ========== start log configs ==========

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

# ========== end log configs ==========

# Expected HTTP response status code
EXPECTED_STATUS = 200

# ========== start email configs ==========

# Load environment variables from .env file
load_dotenv()

# Get the user and password from environment variables
user = os.getenv("USER")
password = os.getenv("PASSWORD")

# Email configuration
EMAIL_SUBJECT = "Alert: one or more URLs are down"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

# ========== end email configs ==========

# List of URLs to check
URLS = [
    "http://195.31.150.176:3000/",
    "http://195.31.150.176:4000/",
    "http://195.31.150.176:5000/",  # python
    "http://195.31.150.176:7000/api",  # python
    "http://195.31.150.176:9000/",  # python
    # "http://195.31.150.176:6000/",
    # "http://195.31.150.176:8000/",
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
        logger.error(f"Failed to restart Apache server: {e}")


def restart_python_apps():
    """
    Calls the script to restart Python applications.
    """
    logger.info("========== Restarting Python applications... ==========")
    try:
        subprocess.run(["/bin/bash", "./scripts/start_apps.sh"], check=True)
        logger.info("Python applications restarted successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart Python applications: {e}")


def send_email(message):
    """
    Sends an email with the specified message.
    """
    logger.info("========== Sending notification email... ==========")
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = EMAIL_SUBJECT
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Alert email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")


def main(restart_services):

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
        logger.warning(">>> One or more URLs are down.")
        if restart_services:
            logger.warning("Restarting Apache server and Python apps as per the -r flag...")
            restart_apache()
            restart_python_apps()

        # Send email notification
        message = f"One or more URLs are down:\n\n" + "\n".join(down_urls)
        send_email(message)
    else:
        logger.info("======= All URLs are up and running correctly. =======")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Monitor URLs and optionally restart services if URLs are down.",
        epilog="Example usage: python app_monitor.py -r",
    )
    parser.add_argument(
        "-r",
        "--restart",
        action="store_true",
        help="Restart Apache and Python applications if URLs are down.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the main function with the restart_services flag
    main(restart_services=args.restart)
