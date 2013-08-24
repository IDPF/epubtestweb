read -p "Are you sure? The DB will be erased. " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -rf ../testsuite-site/testsuite.db
    python ../testsuite-site/manage.py syncdb
    ./run.sh import ~/Projects/epub-testsuite/content/30
    # uncomment to add dummy data to the database
    #./run.sh dummy

    echo "Database re-initialized. Suggest using ./run.sh add-user and ./run.sh add-evaluation to add a user and a test evaluation."
fi


