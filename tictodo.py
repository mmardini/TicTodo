from flask import Flask, request, session, redirect, url_for, \
    render_template, Response

from database import db_session
from models import Task
from tasks_api import tasks_get, tasks_post, task_put
from authentication_api import register_user, check_account, requires_auth


app = Flask(__name__)
app.secret_key = 'tic53rh_0&6!7$6k8z5h0ue9o@+qay7a91zp2487omy*ddxjup)4dtodo'


# Remove database sessions at the end of the request or when the application
# shuts down.
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# ============================== API ROUTES ===================================
@app.route('/api/tasks/', methods=['GET', 'POST'])
@requires_auth
def tasks():
    if request.method == 'GET':
        return tasks_get(session['user_id'])
    elif request.method == 'POST':
        return tasks_post(request.json.get('text'), request.json.get('order'),
                          session['user_id'])


@app.route('/api/tasks/<task_id>', methods=['PUT', 'PATCH'])
@requires_auth
def task(task_id):
    if request.method == 'PUT' or request.method == 'PATCH':
        return task_put(task_id, session['user_id'], request.json.get('text'),
                        request.json.get('order'), request.json.get('done'))


@app.route('/api/tasks/order/', methods=['PUT'])
def update_order():
    try:
        for item in request.form:
            task_id = int(item)
            task_query = Task.query.filter(Task.id == task_id)
            if task_query.count() == 1:
                task_query[0].order = int(request.form[item])
                db_session.commit()

        return Response(status=204)  # No Content
    except ValueError:
        return Response(status=400)  # Bad Request
# =============================================================================


# ======================== AUTHENTICATION ROUTES ==============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = check_account(request.form['username'],
                                request.form['password'])
        if user_id == -1:
            error = 'Invalid username and/or password.'
        else:
            session['logged_in'] = True
            session['user_id'] = user_id
            return redirect(url_for('app_page'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if register_user(request.form['username'], request.form['password']):
            return redirect(url_for('login'))
        else:
            error = 'Username already registered.'
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
# =============================================================================


# ======================== USER INTERFACE ROUTES ==============================
@app.route('/')
def app_page():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
# =============================================================================

if __name__ == '__main__':
    app.run()
