
rm ../../epubtestweb-db/testsuite.db
./manage.py syncdb
cd ../scripts
./runmain.sh copy-users
./runmain.sh import ~/Projects/epub-testsuite/content/30 categories.yaml
cd ../testsuite-site
./manage.py runserver