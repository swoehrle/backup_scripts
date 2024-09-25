import os
import subprocess
import datetime


###Options
path = f'/mnt/datadisk/sharedPrograms/femoz_db_bak/'

def create_filename():
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    filename = f"femoz_db_{date_string}.bak"
    return filename
    

def delete_old_files(directory_path):
    current_date = datetime.datetime.now().date()
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            if (current_date - file_date).days > 60 and file_date.day not in [1, 8, 15, 22, 29]:
            	if not "readme.txt" in file_path:
                   os.remove(file_path)
            if (current_date - file_date).days > 180 and file_date.day not in [1, 15]:
                if not "readme.txt" in file_path:
                   os.remove(file_path)


#cleanup
delete_old_files(path)
delete_old_files(path + 'logs/')

file_n = create_filename()

#use subprocess to make a backup from the remote DB Server
#command = ['/usr/bin/pg_dumpall', '--file', f'{path}{file_n}', '--host', '139.6.160.28', '--port', '5432', '--username', 'femoz',  f'>> {path}logs/{file_n[:-4]}.log', '2>&1']
#subprocess.call(command)
command = f'/usr/bin/pg_dumpall --file {path}{file_n} --host "139.6.160.28" --port "5432" --username "femoz" >> {path}logs/{file_n[:-4]}.log 2>&1'
subprocess.call(command, shell=True)


