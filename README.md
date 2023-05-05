# ERP
## Description
This is the mini-ERP system similar to the SAP version of sales managment. It has the feature of login, customer management, order management and shipping management. We use Django framework(HTML/CSS/JavaScripts as front end, Python as backend, SQLite3 as the database).

## Environment Setting

To improve the cross-platform nature of the project and to make it easier for you to configure the environment, we use Django, a Python-based back-end framework, and SQLite, a zero-configuration lightweight database. with Python installed, simply run the command below is enough：

```
> pip install django
```

## Run the code

```
> python manage.py runserver
```

If the result displayed is similar to

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

July 27, 2021 - 13:34:45
Django version 3.2.5, using settings 'sd.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Then the running is correct.

Open your browser and type: `http://127.0.0.1:8000/` or `http://localhost:8000/` to access the website
