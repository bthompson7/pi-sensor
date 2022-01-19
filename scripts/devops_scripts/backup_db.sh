#!/bin/bash

echo "Backing up database"

user="pi"
password="password"
host="localhost"
db_name="temps"
backup_dir="/home/pi/Desktop/python/database/temps_db.sql"

mysqldump --lock-tables --user=$user --password=$password --host=$host $db_name > $backup_dir

echo "Attempting to commit database changes to github"
cd /home/pi/Desktop/python

internet_is_up=false

#check to make sure the internet is up by pinging google.com then checking the response
while [ "$internet_is_up" = false ]
do
        if ping google.com | grep -q 'PING google.com';
           then
                echo "Internet is up. Pushing database changes"
                internet_is_up=true
		git pull --no-edit
		git add $backup_dir
		git commit -m "Nightly automatic database backup"
		git push
           else
                echo "Unable to ping trying again in 5 minutes."
                sleep 5m #sleep for 5 minutes and try again
        fi
done

