# NAS

WS 2: 139.6.160.151
Max storage: 12 TB (< 14 TB GPU2)

WS 1: 139.6.160.72
Max storage: 12.33 TB (for GPU-Workstation < 20 TB GPU1)

Checkpoints: 139.6.160.149
Max storage: 5.19 TB !?

# Known issues

## WS 1: Datadisk2

Sadly, Datadisk 2 is not reachable anymore. It looks like it is in a panic state, which might be difficult to recover. More information, logs and analysis can be found under ws-1    /mnt/datadisk/sharedPrograms/logs/ - especially important:
-rw-rw-r-- 1 sven sven 3,6K Sep 22 15:22 ai_analysis_diagnosis.txt
-rw-rw-r-- 1 sven sven  455 Sep 22 15:21 diagnosis_short.txt
-rw-rw-r-- 1 sven sven  71K Sep 22 15:16 diagnostics.txt

## Storage (all WS)

All three NAS stations do not provide enough storage for the respective workstations to be backed up. 
I am not familiar with the checkpoints but it doesn't look like it should be able to save the respective checkpoints as well. But I am not quite sure here. 

## WS 2: rsync unavailable - ftp script needs doublechecking

Additionally for Workstation 2 or the respective NAS station, rsync could not be activated by Simon. Thus an FTP script has been written. It needs to be ensured that it actually works as expected though. It throws some awkward error messages. This however only makes sense if there is enough storage to actually save the data, because it could also be linked to storage issues. 

# Edit crontap with local user
``crontab -e``

paste something like:

``09 17 * * * /usr/bin/python3 /home/swoehrle/code/backup_scripts/daily_update_gpu2.py >> /var/log/daily_update_gpu2.log 2>&1``
