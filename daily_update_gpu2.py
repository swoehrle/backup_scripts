# Add these imports
from ftplib import FTP_TLS
import ssl
import os
import time
from datetime import datetime


# FTP server details
ftp_host = "139.6.160.151"
ftp_user = "GPU2"
ftp_password = "gd&h2fDF14"

# Directories to backup
dirs_to_backup = ['/mnt/datadisk/', '/mnt/datadisk2/']



# Add error handling and retry logic
def upload_with_retry(ftp, command, file, max_retries=3):
    for attempt in range(max_retries):
        try:
            ftp.storbinary(command, file)
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1} for {command}")
                continue
            else:
                raise e


def create_remote_dirs(ftp, remote_path):
    """Create remote directories recursively"""
    print(f"Attempting to create: {remote_path}")
    dirs = remote_path.split('/')
    for i in range(len(dirs)):
        try:
            dir_path = '/'.join(dirs[:i+1])
            if dir_path and not dir_path.isspace():
                try:
                    ftp.cwd('/')  # Go to root directory
                    for part in dirs[:i+1]:
                        if part:
                            try:
                                ftp.cwd(part)
                            except:
                                print(f"Creating directory: {part}")
                                ftp.mkd(part)
                                ftp.cwd(part)
                except Exception as e:
                    print(f"Error creating/navigating directory {dir_path}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error for {dir_path}: {str(e)}")

def directory_exists(ftp, path):
    """Check if a directory exists on the FTP server"""
    try:
        original_dir = ftp.pwd()
        ftp.cwd(path)
        ftp.cwd(original_dir)
        return True
    except:
        return False
    

import os
import time
from datetime import datetime

def get_remote_file_mtime(ftp, remote_path):
    try:
        # Get the modification time of the remote file
        mod_time = ftp.voidcmd(f"MDTM {remote_path}")[4:].strip()
        return datetime.strptime(mod_time, "%Y%m%d%H%M%S").timestamp()
    except:
        # If the file doesn't exist or there's an error, return 0
        return 0

def upload_directory(ftp, local_dir, remote_dir, overwrite=False):
    for root, dirs, files in os.walk(local_dir):
        print('Progress', root, dirs)
        for i, filename in enumerate(files):
            if not i % 1000:
                print('     ', i, filename)
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_dir)
            remote_path = os.path.join(remote_dir, relative_path).replace('\\', '/')
            
            # Get local file modification time
            local_mtime = os.path.getmtime(local_path)
            
            # Get remote file modification time
            remote_mtime = get_remote_file_mtime(ftp, remote_path)
            
            # Check if local file is newer
            if local_mtime > remote_mtime:
                # Create remote directories if they don't exist
                remote_dirname = os.path.dirname(remote_path)
                if not directory_exists(ftp, remote_dirname):
                    create_remote_dirs(ftp, remote_dirname)
                
                # Upload the file
                with open(local_path, 'rb') as file:
                    try:
                        ftp.cwd('/')  # Go to root directory
                        ftp.cwd(os.path.dirname(remote_path))  # Navigate to the directory
                        upload_with_retry(ftp, f'STOR {os.path.basename(remote_path)}', file)
                        # print(f"Uploaded: {remote_path}")
                    except Exception as e:
                        if "200 Type set to I" in str(e):
                            pass
                        else:
                            print(f"Error uploading {remote_path}: {str(e)}")
            else:
                pass
                # print(f"Skipping {remote_path}: Local file is not newer than remote file")


def check_ftp_cwd(ftp):
    try:
        current_dir = ftp.pwd()
        print(f"Current FTP working directory: {current_dir}")
    except Exception as e:
        print(f"Error getting current FTP directory: {str(e)}")


def file_exists(ftp, path):
    try:
        ftp.size(path)
        return True
    except:
        return False
    
def list_directory(ftp, directory):
    print(f"Contents of {directory}:")
    try:
        files = ftp.nlst(directory)
        for f in files:
            print(f"  {f}")
    except Exception as e:
        print(f"Error listing {directory}: {str(e)}")

# Replace the FTP connection with FTPS (FTP over TLS)
# ftp = FTP(ftp_host)
ftp = FTP_TLS(ftp_host)
ftp.auth()
ftp.prot_p()  # Set up secure data connection

# # In the main part of the script:
# ftp = FTP(ftp_host)
ftp.login(user=ftp_user, passwd=ftp_password)

print("Initial FTP state:")
check_ftp_cwd(ftp)
list_directory(ftp, "/")
list_directory(ftp, "/IIMGPU2")

for backup_dir in dirs_to_backup:
    remote_dir = f"/GPU2{backup_dir}".replace('//', '/')
    print(f"Processing backup for: {backup_dir}")
    print(f"Remote directory: {remote_dir}")
    upload_directory(ftp, backup_dir, remote_dir, overwrite=False)
    check_ftp_cwd(ftp)  # Check current directory after each backup

ftp.quit()
