
# Getting Started with Adopt Animals WebApp

## Introduction

Please download Python 3.8.3 and on your PC (If you have it, please skip it).

## Usage

1. Open your terminal and Go to your directory.
```bash
$ cd your_directory_name
```

2. Clone the project with the following command.
```bash
$ git clone https://github.com/toma1031/adoptanimals.git
$ cd adoptanimals
```

3. Do following command at terminal for installing library.
```bash
$ pip install -r requirements.txt
```

4. Install MySQL.
```bash
$ brew install mysql
```

5. Start MySQL.
```bash
$ mysql.server start
Starting MySQL
. SUCCESS!
```

6. Create Database.
```bash
$ mysql -u root
mysql> create database adopt_animals;
```

7. Install mysqlclient.
```
$ pip install mysqlclient
```

8. Do migartion.
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

9. In the project directory, you can run.
```bash
$ python manage.py runserver  
```

5. Runs the app in the development mode.\
Open http://127.0.0.1:8000/ to view it in your browser.

