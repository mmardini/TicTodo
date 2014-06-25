TicTodo
=======

A simple todo app built using Flask and Backbone.js.

Run project
-----------
Running the project in a virtualenv is recommended. To run the app using Flask
development server, run the following command:

    python tictodo.py

Then access the app on:

    http://127.0.0.1:5000/

Run tests
---------
The project contains tests for most of its functionality. To run the tests:

    python tests.py

Backend code
------------
The project includes the following Python files:
* `tictodo.py`: This is where the main app and its routes live.
* `database.py`: A simple file that provides a SQLAlchemy session and a
    function to generate a SQLite database file.
* `models.py`: Includes `Task` and `User` classes.
* `authentication_api.py`: All authentication logic lives here. The project
    uses Werkzeug's security functions to store hashed passwords. This file
    also includes a handy `requires_auth` decorator.
* `tasks_api.py`: App routes call the functions of this file to return
    responses to API calls.
* `tests.py`: For unit testing.

Frontend code
-------------
* HTML Templates: The templates (`templates\`) use Jinja2 template inheritance
(`layout.html` is the basefile).

* CSS: The main CSS file is `static\css\main.css`. The project also includes
`normalize.css` to make the app look consistent across browsers.

* Javascript: Javascript files (`static\js\`) are organized in a simple to
understand way. `static\js\vendor` includes the libraries files, and the rest
of .js files are the Backbone app files.

API
---
* `/api/tasks/ (GET)`: Returns a response that has all tasks owned by the user.
* `/api/tasks/ (POST)`: Creates a new task and returns its id.
* `/api/tasks/<task_id> (PUT or PATCH)`: Updates the attributes of an
    individual task.
* `/api/tasks/order/ (PUT)`: This method is an optimized way to update the
    order of several tasks in one request, instead of using the previous method
    for each task individually. This is useful when the user re-orders some
    task and the order of several tasks needs to be updated as a result.

Dependencies
------------
I'm a fan of minimalism in software design, so although I could throw in a
dozen front-end and back-end libraries and use them in the project, what makes
more sense to me is using as few dependencies as possible.

The project uses the following dependencies:

####Front-end _(All needed files are included in `static\js\vendor\`)_:
* Backbone.js 1.1.2 and its dependencies (Underscore.js and jQuery).
* A customized build of jQuery UI 1.10.4 that includes sortable functionality
    only.

####Back-end:
* Flask 0.10.1 and its dependencies (Werkzeug and Jinja2).
* SQLAlchemy 0.9.4 with a SQLite database.

Having said that, some of the libraries that would have been useful if the
application was larger are:

####Front-end:
* require.js: For a more modular project.
* Foundation or Bootstrap: or another front-end framework.
* Handlebars or Mustache: For clean and compiled templates.

####Back-end:
* Flask Blueprints: Which would simplify large apps but would make small apps
    more complex.
* Flask-SQLAlchemy: I currently use SQLAlchemy directly. Using Flask-SQLAlchemy
    would make interacting with the database simpler.
* Flask-Login: I've coded my own authentication system. Using a library
    like Flask-Login would make user management easier.
