read -p "Are you sure? The DB will be erased. " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -rf ../../epubtestweb-db/testsuite.db
    python ../testsuite-site/manage.py syncdb
    ./run.sh import ~/Projects/epub-testsuite/content/30
    # uncomment to add dummy data to the database
    #./runmain.sh dummy

    echo "Database re-initialized with testsuite data."
    read -p "Add sample user and evaluation data? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        ./runmain.sh add-user test test test
        ./runmain.sh add-rs
    fi
fi


