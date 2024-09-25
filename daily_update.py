#only synchronise
import os
import subprocess

backup_dest = "rsync://rsync@139.6.160.72:/GPU-workstation/"
dirs_to_backup = ['/mnt/datadisk/', '/mnt/datadisk2/preprocessed/', '/mnt/datadisk2/AI4SusCo/']	
for backup_dir in dirs_to_backup:
    #v=verbose, -a=archive, --delete=mirror (delete files which have been deleted in backup_dir) -P=Progress bar
    #incremental backup is done with qnap snapshots
    subprocess.call(['rsync', '--password-file=/home/sven/rsync_pass', '-aPv', '--delete', "{}".format(backup_dir), "{}{}".format(backup_dest, backup_dir)])
