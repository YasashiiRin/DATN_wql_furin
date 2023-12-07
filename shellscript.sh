#!/bin/bash

# Next we will check if venv is there or not
ls | grep "venv" > /dev/null 2>&1
if [ $? == 0 ]
then
  echo "Python vevn available"
  source venv/bin/activate
else
  virtualenv -p python3 venv
  source venv/bin/activate
  chmod -R 777 .
  pip3 install -r requirements.txt
  echo "Python venv has been installed with req.txt"
fi


# Next we will migrate the changes
python3 manage.py makemigrations
python3 manage.py migrate


# Next we will start the server
nohup python3 manage.py runserver 0.0.0.0:9000 > /dev/null 2>&1 &
