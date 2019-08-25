rm -rf ./venv
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt 
wsk api get smAPI -f -i > api_conf.json

locust -f load_test.py



