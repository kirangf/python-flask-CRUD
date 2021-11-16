# CRUD operation using Python and Flask framework
CRUD operation using python and flask.

## Requirements
- Python3
- Mysql 5.7+

## Create Virtual Environment
Use a virtual environment to manage the dependencies for your project, both in development and in production.
```
python -m venv <environment_name>
```

## Activate Virtual Environment
Activate created virtual environment before start your project.
```
cd .\saenv\Scripts\activate
```

## Install Dependencies 
```
pip install -r requirements.txt
```
## Flask Configuration
To run the application, use the **flask** command or **python -m flask**. Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable:
```
$env:FLASK_APP="run.py"

```
To enable all development features, set the FLASK_ENV environment variable to development before calling flask run.
```
$env:FLASK_DEBUG="development"
```

## Run Application
```
python run.py
