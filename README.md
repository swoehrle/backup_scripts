# Edit crontap with local user
``crontab -e``

paste something like:

``09 17 * * * /usr/bin/python3 /home/swoehrle/code/backup_scripts/daily_update_gpu2.py >> /var/log/daily_update_gpu2.log 2>&1``
