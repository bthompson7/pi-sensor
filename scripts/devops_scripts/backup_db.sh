echo "Backing up database"

user="pi"
password="password"
host="localhost"
db_name="temps"
backup_dir="/home/pi/Desktop/python/database/temps_db.sql"

current_date=$(date)
mysqldump --lock-tables --user=$user --password=$password --host=$host $db_name > $backup_dir

echo "Commiting to github"

#you must have an ssh key otherwise this will fail
git add $backup_dir
git commit -m "Nightly database backup " $current_date
git push

