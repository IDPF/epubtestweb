#backup
echo "Backing up current database"
now=$(date +"%Y_%m_%d")
mv ../../epubtestweb-db/testsuite.db ../../epubtestweb-db/testsuite.db.$now
#create new
echo "Creating new database"
python ../testsuite-site/manage.py syncdb
echo "Done"