export PYTHONPATH=${PYTHONPATH}:$PWD/../testsuite-site/:$PWD/../
export DJANGO_SETTINGS_MODULE=testsuite.settings
../epubtestenv/bin/python main.py $@
