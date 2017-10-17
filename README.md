## Django app data import
Management commands to import data from different sources

### Setup
- Create virtual enviroment with python3
    - mkdir venv
    - cd venv
    - virtualenv -p python3 .
    more details here: https://virtualenv.pypa.io/en/stable/

- start virtual enviroment
    - source venv/bin/activate
- install requirements
    - pip install requirements.txt

### import data
- import data from url
    - run command: python manage.py import_from_url

- import data from local json file
    - run command: python manage.py import_from_json_file
    
- import data from local csv file
    - run command: python manage.py import_from_csv