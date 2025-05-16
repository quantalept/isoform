# Quantalept Python-FastAPI Project Template

A reusable,  production-ready FastAPI project template. Clone this repo, install dependencies, and start building APIs in minutes!

---

##  Project Structure

fastapi-template/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   └── users.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/
│   │   └── config.py
│   ├── crud/
│   │   └── user.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── service/
│   │   └── user.py
│   ├── utils/
│   │   └── hash.py
│   └── main.py
├── tests/
│   └── test_users.py
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt

##  Setup Instructions

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/yourusername/python-fastapi-template.git
cd python-fastapi-template 
```


### 🔹 2. Create and Activate Virtual Environment

``` bash
python3 -m venv venv
source venv/bin/activate
```
### 🔹 3. Install Dependencies

``` bash
pip install -r requirements.txt  
```

Install dependencies you need using the below command 
``` bash
pip install dependency-you-need another-dependency 
```
and freeze them to requirements.txt using 

``` bash
pip freeze > requirements.txt
```

### 🔹 4. Run the Application
``` bash

uvicorn app.main:app --reload
```

Visit: http://localhost:8000 and modify your code accordingly

###  Auto API Docs

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

###  Environment Variables
To keep secrets like passwords and API keys safe, use a .env file to store them instead of hardcoding into your source code. This approach enhances security and flexibility.


import os
PROJECT_NAME: str = os.getenv("PROJECT_NAME")
usually he values of database url and other such things will be stored here 

This keeps your credentials safe and configurable across environments.)

### Git Ignore

A .gitignore file tells Git which files or folders to ignore in version control. This typically includes:

Environment-specific files like .env

Local dev artifacts like venv/, __pycache__/, and *.log

IDE settings (.vscode/, .idea/)

OS-specific files (.DS_Store, Thumbs.db)

###  Setting  up database

 Start PostgreSQL with Docker using docker run 

``` bash
 docker run --name fastapi-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=fastapi_db -p 5432:5432 -d postgres
```
OR
 Edit the docker-compose.yml file and then run 
 ``` bash
    docker-compose up -d
 ```

 Im using 5555 port as i already using 5432 use 5432 as that is default

 Ensure the correct database URL including exact password user and dbname is set in the .env file 

 Test once the db is created and accessible using dbeaver

###  using alembic for migrations
 Alembic helps us in easy migration of tables whose structure we modify in the models.
 Once you create a new table inside the python file under models directory update the alembic/env.py by importing that specific model
 After each change you made in database model ensure you run the following 
```bash
 alembic revision --autogenerate -m "Your reference message"

 alembic  upgrade head 
 ```
 This will apply the changes in db.Ensure these were made using dbeaver 
 
