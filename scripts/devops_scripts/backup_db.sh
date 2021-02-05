#!/bin/bash

echo "Backing up database"

user="pi"
password="password"
host="localhost"
db_name="temps"
backup_dir="/home/pi/Desktop/python/database/temps_db.sql"

mysqldump --lock-tables --user=$user --password=$password --host=$host $db_name > $backup_dir

echo "Commiting to github"
cd /home/pi/Desktop/python

#you must have an ssh key otherwise this will fail
git add $backup_dir
git commit -m "Database backup "
git push

