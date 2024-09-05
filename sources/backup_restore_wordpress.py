import os
import subprocess

import paramiko
from paramiko import SFTPClient

# LOCAL server configs
LOCAL_WP_PATH = r'C:\Users\Edu\Local Sites'
LOCAL_DB_NAME = 'local'
LOCAL_DB_USER = 'user'
LOCAL_DB_PASSWORD = 'password'

# REMOTE server configs
REMOTE_SERVER = 'ipaddrs'  # 'qjump.hstgr.cloud'
REMOTE_USER = 'user'
REMOTE_PASSWORD = 'pass'
REMOTE_WP_PATH = '/var/www/site/'
REMOTE_DB_NAME = 'site'
REMOTE_DB_USER = 'aaaa'
REMOTE_DB_PASSWORD = 'aaaa123'

# DB dump files
DB_DUMP_LOCAL_FILE_NAME = "backup_local.sql"
DB_DUMP_REMOTE_FILE_NAME = "backup_remote.sql"
DB_DUMP_LOCAL_FILE = LOCAL_WP_PATH + DB_DUMP_LOCAL_FILE_NAME
DB_DUMP_REMOTE_FILE = REMOTE_WP_PATH + DB_DUMP_REMOTE_FILE_NAME

# Files archive
FILES_ARCHIVE_LOCAL_NAME = "wp_files_local.tar.gz"
FILES_ARCHIVE_REMOTE_NAME = "wp_files_remote.tar.gz"
FILES_ARCHIVE_LOCAL = LOCAL_WP_PATH + FILES_ARCHIVE_LOCAL_NAME
FILES_ARCHIVE_REMOTE = REMOTE_WP_PATH + FILES_ARCHIVE_REMOTE_NAME


def create_ssh_client(server=REMOTE_SERVER, user=REMOTE_USER, password=REMOTE_PASSWORD):
    print("SSH connecting...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(server, username=user, password=password)
        print("SSH connection established.")
        return ssh
    except paramiko.AuthenticationException:
        print("Authentication failed when connecting to the remote server.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def create_sftp_client_with_pass(server=REMOTE_SERVER, user=REMOTE_USER, password=REMOTE_PASSWORD):
    print("SFTP connecting...")
    try:
        transport = paramiko.Transport((server, 22))
        print(f"Connecting to {server} with username {user}...")
        transport.connect(username=user, password=password)
        sftp = SFTPClient.from_transport(transport)
        print("SFTP connection established.")
        return sftp, transport
    except paramiko.AuthenticationException as e:
        print("Authentication failed when connecting to the remote server for SFTP.")
        print(f"Details: {e}")
        transport.close()
        return None, None
    except Exception as e:
        print(f"An error occurred during SFTP connection: {e}")
        if transport.is_active():
            transport.close()
        return None, None


def create_sftp_client_with_key(server=REMOTE_SERVER, user=REMOTE_USER, key_file_path="~/.ssh/id_rsa"):
    print("SFTP connecting...")
    try:
        key = paramiko.RSAKey.from_private_key_file(os.path.expanduser(key_file_path))
        transport = paramiko.Transport((server, 22))
        print(f"Connecting to {server} with username {user} using SSH key...")
        transport.connect(username=user, pkey=key)
        sftp = SFTPClient.from_transport(transport)
        print("SFTP connection established.")
        return sftp, transport
    except paramiko.AuthenticationException as e:
        print("Authentication failed when connecting to the remote server for SFTP.")
        print(f"Details: {e}")
        if transport.is_active():
            transport.close()
        return None, None
    except Exception as e:
        print(f"An error occurred during SFTP connection: {e}")
        if transport.is_active():
            transport.close()
        return None, None


def backup_remote_database():
    """
    Function to backup REMOTE database
    """
    print("Starting REMOTE DB backup...")
    dump_cmd = f"mysqldump -u {REMOTE_DB_USER} -p{REMOTE_DB_PASSWORD} {REMOTE_DB_NAME} >{DB_DUMP_REMOTE_FILE}"
    ssh = create_ssh_client(REMOTE_SERVER, REMOTE_USER, REMOTE_PASSWORD)
    if ssh is not None:
        ssh.exec_command(dump_cmd)
        ssh.close()
        print("Finished REMOTE DB backup.")

        sftp, transport = create_sftp_client_with_key(REMOTE_SERVER, REMOTE_USER)
        if sftp is not None and transport is not None:
            if file_exists(sftp, DB_DUMP_REMOTE_FILE):
                print(f">>> Remote DB backup file created: {DB_DUMP_REMOTE_FILE}")
            else:
                print(f">>> Remote DB backup file NOT FOUND: {FILES_ARCHIVE_REMOTE}")
            sftp.close()
            transport.close()


def backup_local_database():
    """
    Function to backup LOCAL database
    """
    print("Starting LOCAL DB backup...")
    dump_cmd = f"mysqldump -u {LOCAL_DB_USER} -p{LOCAL_DB_PASSWORD} {LOCAL_DB_NAME} > {DB_DUMP_LOCAL_FILE}"
    subprocess.run(dump_cmd, shell=True, check=True)
    print("Finished LOCAL DB backup.")

    # Verify if the file was created
    if os.path.isfile(DB_DUMP_LOCAL_FILE):
        print(f">>> Local DB backup file created: {DB_DUMP_LOCAL_FILE}")


def backup_remote_files():
    """
    Function to backup REMOTE WordPress files
    """
    print("Starting REMOTE files backup...")
    tar_cmd = f'tar -czvf {FILES_ARCHIVE_REMOTE_NAME} -C "{REMOTE_WP_PATH}" .'
    ssh = create_ssh_client(REMOTE_SERVER, REMOTE_USER, REMOTE_PASSWORD)
    if ssh is not None:
        ssh.exec_command(tar_cmd)
        ssh.close()
        print("Finished REMOTE files backup.")

        sftp, transport = create_sftp_client_with_key(REMOTE_SERVER, REMOTE_USER)
        if sftp is not None and transport is not None:
            if file_exists(sftp, FILES_ARCHIVE_REMOTE):
                print(f">>> Remote files archive created: {FILES_ARCHIVE_REMOTE}")
            else:
                print(f">>> Remote files archive NOT FOUND: {FILES_ARCHIVE_REMOTE}")
            sftp.close()
            transport.close()


def backup_local_files():
    """
    Function to backup LOCAL WordPress files
    """
    print("Starting LOCAL files backup...")
    tar_cmd = f'tar -czvf {FILES_ARCHIVE_LOCAL_NAME} -C "{LOCAL_WP_PATH}" .'
    subprocess.run(tar_cmd, shell=True, check=True)
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
    sftp, transport = create_sftp_client_with_key(REMOTE_SERVER, REMOTE_USER)
    if sftp is not None and transport is not None:
        sftp.put(DB_DUMP_LOCAL_FILE, os.path.join(REMOTE_WP_PATH, DB_DUMP_LOCAL_FILE_NAME))
        sftp.put(FILES_ARCHIVE_LOCAL, os.path.join(REMOTE_WP_PATH, FILES_ARCHIVE_LOCAL_NAME))

        sftp.close()
        transport.close()
        print(
            f"Files transferred to REMOTE server: {REMOTE_WP_PATH}{DB_DUMP_LOCAL_FILE}, {REMOTE_WP_PATH}{FILES_ARCHIVE_LOCAL}"
        )


def transfer_files_remote_to_local():
    """
    Function to transfer files to LOCAL server from REMOTE server
    """
    print("Transferring files to LOCAL server...")
    sftp, transport = create_sftp_client_with_key(REMOTE_SERVER, REMOTE_USER)
    if sftp is not None and transport is not None:
        sftp.get(os.path.join(LOCAL_WP_PATH, DB_DUMP_REMOTE_FILE_NAME), DB_DUMP_REMOTE_FILE)
        sftp.get(os.path.join(LOCAL_WP_PATH, FILES_ARCHIVE_REMOTE_NAME), FILES_ARCHIVE_REMOTE)

        sftp.close()
        transport.close()
        print(f"Files transferred to LOCAL server: {DB_DUMP_REMOTE_FILE}, {FILES_ARCHIVE_REMOTE}")


def restore_remote_database():
    """
    Function to restore database on remote server
    """
    print("Starting REMOTE DB restore...")
    ssh = create_ssh_client(REMOTE_SERVER, REMOTE_USER, REMOTE_PASSWORD)
    if ssh is not None:
        db_restore_cmd = f"mysql -u {REMOTE_DB_USER} -p{REMOTE_DB_PASSWORD} {REMOTE_DB_NAME} < {os.path.join(REMOTE_WP_PATH, DB_DUMP_LOCAL_FILE)}"
        ssh.exec_command(db_restore_cmd)
        ssh.close()
        print("Finished REMOTE DB restore.")


def restore_local_database():
    """
    Function to restore database on LOCAL server
    """
    print("Starting LOCAL DB restore...")
    try:
        db_restore_cmd = f"mysql -u {LOCAL_DB_USER} -p{LOCAL_DB_PASSWORD} {LOCAL_DB_NAME} < {DB_DUMP_REMOTE_FILE}"
        subprocess.run(db_restore_cmd, shell=True, check=True)
        print("Finished LOCAL DB restore.")
    except Exception as e:
        print(f"An error occurred during LOCAL DB restore: {e}")


def restore_remote_files():
    """
    Function to restore WordPress files on REMOTE server
    """
    print("Starting REMOTE files restore...")
    ssh = create_ssh_client(REMOTE_SERVER, REMOTE_USER, REMOTE_PASSWORD)
    if ssh is not None:
        files_restore_cmd = f"tar -xzvf {os.path.join(REMOTE_WP_PATH, FILES_ARCHIVE_LOCAL)} -C {REMOTE_WP_PATH}"
        ssh.exec_command(files_restore_cmd)
        ssh.close()
        print("Finished REMOTE files restore.")


def restore_local_files():
    """
    Function to restore WordPress files on LOCAL server
    """
    print("Starting LOCAL files restore...")
    try:
        files_restore_cmd = f"tar -xzvf {FILES_ARCHIVE_REMOTE} -C {LOCAL_WP_PATH}"
        subprocess.run(files_restore_cmd, shell=True, check=True)
        print("Finished LOCAL files restore.")
    except Exception as e:
        print(f"An error occurred during LOCAL files restore: {e}")


def restart_remote_apache():
    """
    Function to restart Apache on REMOTE server
    """
    print("Restarting Apache on REMOTE server...")
    ssh = create_ssh_client(REMOTE_SERVER, REMOTE_USER, REMOTE_PASSWORD)
    if ssh is not None:
        try:
            restart_cmd = "sudo systemctl restart apache2"
            stdin, stdout, stderr = ssh.exec_command(restart_cmd)
            stdin.write(REMOTE_PASSWORD + "\n")  # Enter sudo password
            stdin.flush()
            stdout.channel.recv_exit_status()  # Wait for command to finish
            ssh.close()
            print("Apache restarted on REMOTE server.")
        except Exception as e:
            print(f"An error occurred while restarting Apache on REMOTE: {e}")


def restart_local_apache():
    """
    Function to restart Apache on LOCAL server
    """
    print("Restarting Apache on LOCAL server...")
    try:
        restart_cmd = "systemctl restart apache2"
        subprocess.run(restart_cmd, shell=True, check=True)
        print("Apache restarted on LOCAL server.")
    except Exception as e:
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
    for url in urls:  # Corrected the syntax error
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
    # create_ssh_client()
    # create_sftp_client()

    # create_sftp_client_with_key()
    print("========== Process completed successfully ==========")
