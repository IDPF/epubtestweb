export PYTHONPATH=${PYTHONPATH}:$PWD/../testsuite-site/
export DJANGO_SETTINGS_MODULE=testsuite.settings

python main.py $@
