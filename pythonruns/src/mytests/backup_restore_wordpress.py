import os
import posixpath
import shlex
import subprocess

import paramiko

# Credentials and hosts come from the environment (see .env.example); nothing secret is hardcoded.
# LOCAL server configs
LOCAL_WP_PATH = os.getenv("WP_LOCAL_PATH", r"C:\Users\Edu\Local Sites")
LOCAL_DB_NAME = os.getenv("WP_LOCAL_DB_NAME", "local")
LOCAL_DB_USER = os.getenv("WP_LOCAL_DB_USER", "")
LOCAL_DB_PASSWORD = os.getenv("WP_LOCAL_DB_PASSWORD", "")

# REMOTE server configs
REMOTE_SERVER = os.getenv("WP_REMOTE_SERVER", "")
REMOTE_USER = os.getenv("WP_REMOTE_USER", "")
REMOTE_PASSWORD = os.getenv("WP_REMOTE_PASSWORD", "")  # used for sudo; SSH auth prefers the key below
REMOTE_KEY_FILE = os.path.expanduser(os.getenv("WP_REMOTE_KEY_FILE", "~/.ssh/id_ed25519"))
REMOTE_WP_PATH = os.getenv("WP_REMOTE_PATH", "/var/www/site/")
REMOTE_DB_NAME = os.getenv("WP_REMOTE_DB_NAME", "site")
REMOTE_DB_USER = os.getenv("WP_REMOTE_DB_USER", "")
REMOTE_DB_PASSWORD = os.getenv("WP_REMOTE_DB_PASSWORD", "")

# Refuse SHA-1 RSA signatures ("ssh-rsa"); rsa-sha2-256/512 and ed25519/ecdsa keys still work.
# Mitigates the paramiko SHA-1 advisory, which has no patched release.
DISABLED_ALGORITHMS = {"pubkeys": ["ssh-rsa"], "keys": ["ssh-rsa"]}

# DB dump files
DB_DUMP_LOCAL_FILE_NAME = "backup_local.sql"
DB_DUMP_REMOTE_FILE_NAME = "backup_remote.sql"
DB_DUMP_LOCAL_FILE = os.path.join(LOCAL_WP_PATH, DB_DUMP_LOCAL_FILE_NAME)
DB_DUMP_REMOTE_FILE = posixpath.join(REMOTE_WP_PATH, DB_DUMP_REMOTE_FILE_NAME)

# Files archive
FILES_ARCHIVE_LOCAL_NAME = "wp_files_local.tar.gz"
FILES_ARCHIVE_REMOTE_NAME = "wp_files_remote.tar.gz"
FILES_ARCHIVE_LOCAL = os.path.join(LOCAL_WP_PATH, FILES_ARCHIVE_LOCAL_NAME)
FILES_ARCHIVE_REMOTE = posixpath.join(REMOTE_WP_PATH, FILES_ARCHIVE_REMOTE_NAME)


def create_ssh_client(server=REMOTE_SERVER, user=REMOTE_USER, key_file_path=REMOTE_KEY_FILE):
    """Connect with host-key verification against ~/.ssh/known_hosts (unknown hosts are rejected)."""
    print("SSH connecting...")
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
    try:
        ssh.connect(
            server,
            username=user,
            key_filename=key_file_path if os.path.isfile(key_file_path) else None,
            disabled_algorithms=DISABLED_ALGORITHMS,
        )
        print("SSH connection established.")
        return ssh
    except paramiko.AuthenticationException:
        print("Authentication failed when connecting to the remote server.")
    except paramiko.SSHException as e:
        print(f"SSH error (is the host in known_hosts?): {e}")
    except OSError as e:
        print(f"Network error: {e}")
    ssh.close()
    return None


def run_remote(ssh, cmd, stdin_secret=None):
    """Run a command and wait for it; secrets go through stdin so they never appear in a process list."""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    if stdin_secret is not None:
        stdin.write(stdin_secret + "\n")
        stdin.flush()
    stdin.channel.shutdown_write()
    status = stdout.channel.recv_exit_status()
    if status != 0:
        print(f"Remote command failed ({status}): {stderr.read().decode(errors='replace').strip()}")
    return status == 0


def mysql_remote_cmd(tool, redirect):
    """Build a remote mysql/mysqldump command that reads the password from stdin into MYSQL_PWD."""
    q = shlex.quote
    return f"read -r MYSQL_PWD && export MYSQL_PWD && {tool} -u {q(REMOTE_DB_USER)} {q(REMOTE_DB_NAME)} {redirect}"


def local_mysql_env():
    return {**os.environ, "MYSQL_PWD": LOCAL_DB_PASSWORD}


def backup_remote_database():
    """
    Function to backup REMOTE database
    """
    print("Starting REMOTE DB backup...")
    ssh = create_ssh_client()
    if ssh is not None:
        with ssh:
            cmd = mysql_remote_cmd("mysqldump", f"> {shlex.quote(DB_DUMP_REMOTE_FILE)}")
            if run_remote(ssh, cmd, REMOTE_DB_PASSWORD):
                with ssh.open_sftp() as sftp:
                    if file_exists(sftp, DB_DUMP_REMOTE_FILE):
                        print(f">>> Remote DB backup file created: {DB_DUMP_REMOTE_FILE}")
                    else:
                        print(f">>> Remote DB backup file NOT FOUND: {DB_DUMP_REMOTE_FILE}")
        print("Finished REMOTE DB backup.")


def backup_local_database():
    """
    Function to backup LOCAL database
    """
    print("Starting LOCAL DB backup...")
    with open(DB_DUMP_LOCAL_FILE, "wb") as out:
        subprocess.run(["mysqldump", "-u", LOCAL_DB_USER, LOCAL_DB_NAME], stdout=out, env=local_mysql_env(), check=True)
    print("Finished LOCAL DB backup.")

    # Verify if the file was created
    if os.path.isfile(DB_DUMP_LOCAL_FILE):
        print(f">>> Local DB backup file created: {DB_DUMP_LOCAL_FILE}")


def backup_remote_files():
    """
    Function to backup REMOTE WordPress files
    """
    print("Starting REMOTE files backup...")
    q = shlex.quote
    tar_cmd = f"tar -czf {q(FILES_ARCHIVE_REMOTE)} --exclude={q(FILES_ARCHIVE_REMOTE_NAME)} -C {q(REMOTE_WP_PATH)} ."
    ssh = create_ssh_client()
    if ssh is not None:
        with ssh:
            if run_remote(ssh, tar_cmd):
                with ssh.open_sftp() as sftp:
                    if file_exists(sftp, FILES_ARCHIVE_REMOTE):
                        print(f">>> Remote files archive created: {FILES_ARCHIVE_REMOTE}")
                    else:
                        print(f">>> Remote files archive NOT FOUND: {FILES_ARCHIVE_REMOTE}")
        print("Finished REMOTE files backup.")


def backup_local_files():
    """
    Function to backup LOCAL WordPress files
    """
    print("Starting LOCAL files backup...")
    subprocess.run(
        ["tar", "-czf", FILES_ARCHIVE_LOCAL, f"--exclude={FILES_ARCHIVE_LOCAL_NAME}", "-C", LOCAL_WP_PATH, "."],
        check=True,
    )
    print("Finished LOCAL files backup.")

    # Verify if the file was created
    if os.path.isfile(FILES_ARCHIVE_LOCAL):
        print(f">>> Local files archive created: {FILES_ARCHIVE_LOCAL}")


def file_exists(sftp, file_path):
    try:
        sftp.stat(file_path)
        return True
    except FileNotFoundError:
        return False


def transfer_files_local_to_remote():
    """
    Function to transfer files to REMOTE server
    """
    print("Transferring files to REMOTE server...")
    ssh = create_ssh_client()
    if ssh is not None:
        with ssh, ssh.open_sftp() as sftp:
            sftp.put(DB_DUMP_LOCAL_FILE, posixpath.join(REMOTE_WP_PATH, DB_DUMP_LOCAL_FILE_NAME))
            sftp.put(FILES_ARCHIVE_LOCAL, posixpath.join(REMOTE_WP_PATH, FILES_ARCHIVE_LOCAL_NAME))
        print(f"Files transferred to REMOTE server: {REMOTE_WP_PATH}")


def transfer_files_remote_to_local():
    """
    Function to transfer files to LOCAL server from REMOTE server
    """
    print("Transferring files to LOCAL server...")
    ssh = create_ssh_client()
    if ssh is not None:
        with ssh, ssh.open_sftp() as sftp:
            sftp.get(DB_DUMP_REMOTE_FILE, os.path.join(LOCAL_WP_PATH, DB_DUMP_REMOTE_FILE_NAME))
            sftp.get(FILES_ARCHIVE_REMOTE, os.path.join(LOCAL_WP_PATH, FILES_ARCHIVE_REMOTE_NAME))
        print(f"Files transferred to LOCAL server: {LOCAL_WP_PATH}")


def restore_remote_database():
    """
    Function to restore database on remote server
    """
    print("Starting REMOTE DB restore...")
    ssh = create_ssh_client()
    if ssh is not None:
        with ssh:
            dump = posixpath.join(REMOTE_WP_PATH, DB_DUMP_LOCAL_FILE_NAME)
            run_remote(ssh, mysql_remote_cmd("mysql", f"< {shlex.quote(dump)}"), REMOTE_DB_PASSWORD)
        print("Finished REMOTE DB restore.")


def restore_local_database():
    """
    Function to restore database on LOCAL server
    """
    print("Starting LOCAL DB restore...")
    try:
        with open(os.path.join(LOCAL_WP_PATH, DB_DUMP_REMOTE_FILE_NAME), "rb") as dump:
            subprocess.run(["mysql", "-u", LOCAL_DB_USER, LOCAL_DB_NAME], stdin=dump, env=local_mysql_env(), check=True)
        print("Finished LOCAL DB restore.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"An error occurred during LOCAL DB restore: {e}")


def restore_remote_files():
    """
    Function to restore WordPress files on REMOTE server
    """
    print("Starting REMOTE files restore...")
    ssh = create_ssh_client()
    if ssh is not None:
        with ssh:
            archive = posixpath.join(REMOTE_WP_PATH, FILES_ARCHIVE_LOCAL_NAME)
            run_remote(ssh, f"tar -xzf {shlex.quote(archive)} -C {shlex.quote(REMOTE_WP_PATH)}")
        print("Finished REMOTE files restore.")


def restore_local_files():
    """
    Function to restore WordPress files on LOCAL server
    """
    print("Starting LOCAL files restore...")
    try:
        archive = os.path.join(LOCAL_WP_PATH, FILES_ARCHIVE_REMOTE_NAME)
        subprocess.run(["tar", "-xzf", archive, "-C", LOCAL_WP_PATH], check=True)
        print("Finished LOCAL files restore.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"An error occurred during LOCAL files restore: {e}")


def restart_remote_apache():
    """
    Function to restart Apache on REMOTE server
    """
    print("Restarting Apache on REMOTE server...")
    ssh = create_ssh_client()
    if ssh is not None:
        with ssh:
            # -S reads the sudo password from stdin, -p '' suppresses the prompt
            if run_remote(ssh, "sudo -S -p '' systemctl restart apache2", REMOTE_PASSWORD):
                print("Apache restarted on REMOTE server.")


def restart_local_apache():
    """
    Function to restart Apache on LOCAL server
    """
    print("Restarting Apache on LOCAL server...")
    try:
        subprocess.run(["systemctl", "restart", "apache2"], check=True)
        print("Apache restarted on LOCAL server.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"An error occurred while restarting Apache on LOCAL: {e}")


def backup_remote():
    print("@@@ Starting REMOTE backup process...")
    backup_remote_database()
    print("--------------------------------")
    backup_remote_files()
    print("@@@ Backup REMOTE complete.")


def backup_local():
    print("@@@ Starting LOCAL backup process...")
    backup_local_database()
    print("--------------------------------")
    backup_local_files()
    print("@@@ Backup LOCAL complete.")


def restore_remote():
    print("Restoring DB and files on REMOTE server...")
    restore_remote_database()
    restore_remote_files()
    print("Restore REMOTE complete.")


def restore_local():
    print("Restoring DB and files on LOCAL server...")
    restore_local_database()
    restore_local_files()
    print("Restore LOCAL complete.")


def full_backup_remote_restore_local():
    backup_remote()
    transfer_files_remote_to_local()
    restore_local()
    restart_local_apache()
    check_site_live()


def full_backup_local_restore_remote():
    backup_local()
    transfer_files_local_to_remote()
    restore_remote()
    restart_remote_apache()
    check_site_live()


def check_site_live(url="https://skipy.online/"):
    print(f"Checking if site [{url}] is live...\n")

    # Using curl to check if the site is live
    try:
        response = subprocess.check_output(["curl", "-Is", url], stderr=subprocess.STDOUT).decode("utf-8")

        # Check for HTTP response status
        if "HTTP/2 200" in response or "HTTP/1.1 200" in response:
            print(">>> The site is live!\n")
        else:
            print("The site might not be live. Response:")
            print(response)
    except subprocess.CalledProcessError as e:
        print("Failed to reach the site. Error:")
        print(e.output.decode("utf-8"))


def check_site_list_live():
    urls = [
        "https://skipy.io/",
        "https://skipy.app/",
        "https://skipy.online/",
        "https://www.skipy.io/",
        "https://www.skipy.app/",
        "https://www.skipy.online/",
        "https://skipy.online/wp-admin/",
        "https://skipy.online/wp-login.php",
    ]
    for url in urls:
        check_site_live(url)


if __name__ == "__main__":
    print("========== Starting backup process ==========")
    # Uncomment the necessary function to use
    # full_backup_local_restore_remote()
    # full_backup_remote_restore_local()
    # backup_local()

    backup_remote()

    # transfer_files_remote_to_local()
    # check_site_live()
    # check_site_list_live()
    print("========== Process completed successfully ==========")
