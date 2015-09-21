export PYTHONPATH=${PYTHONPATH}:$PWD/../testsuite-site/:$PWD/../
export DJANGO_SETTINGS_MODULE=testsuite.settings
../env/bin/python main.py $@
