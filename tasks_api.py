from flask import Response, json

from sqlalchemy.orm import class_mapper

from database import db_session
from models import Task


def tasks_get(owner):
    """Returns a JSON response that has all tasks owned by the user.

    Args:
        owner (int): The id of the User who owns the tasks.

    Returns:
        Response.  A response that has all tasks the user owns.
    """
    tasks = Task.query.filter(Task.owner == owner)
    result = [serialize(task) for task in tasks]
    return json_response(result)


def tasks_post(text, order, owner):
    """Creates a new Task in the database and returns its id.

    Args:
        text (str): The text of the task.
        order (int): The zero-based order of the task.
        owner (int): The id of the User who owns the task.

    Returns:
        Response.  A response that has id of the created task.
    """
    t = Task(text, order, owner)
    db_session.add(t)
    db_session.commit()

    return json_response({"id": t.id})


def task_put(id, owner, text=None, order=None, done=None):
    """Updates a task and returns the status of the update operation.

    Args:
        id (int): The id of the Task which will be updated.
        owner (int): The id of the User who owns the task.
        text (str): The text of the task. Can be None if we don't want to
            update it.
        order (int): The zero-based order of the task. Can be None if we don't
            want to update it.
        done (bool): A boolean that indicates if the task is done or not. Can
            be None if we don't want to update it.

    Returns:
        Response.  The status code of the response:
            204 -- The task has been updated successfully.
            403 -- The user isn't authorized to update the task.
    """
    task = Task.query.get(id)
    if owner == task.owner:
        # We can't just do "if text" because an empty text is a False boolean.
        if text is not None:
            task.text = text
        # Likewise, 0 order is a False boolean.
        if order is not None:
            task.order = order
        # Also, we want to update "done" no matter what boolean value it has,
        # if it has one.
        if done is not None:
            task.done = done
        db_session.commit()

        return Response(status=204)  # No Content
    else:
        return Response(status=403)  # Forbidden


def json_response(data):
    """Serializes an object to JSON and returns the JSON in a Response.

    Args:
        data (object): The data structure to serialize.

    Returns:
        Response.  The response has the appropriate MIME Type for JSON.
    """
    return Response(json.dumps(data), mimetype='application/json')


def serialize(task):
    """Transforms attirbutes of a Task instance (except owner) into a
    dictionary which can be dumped to JSON.

    Args:
        task (Task): The Task instance to serialize its attirbutes.

    Returns:
        dict. The dictionary has columns names as keys and instance attirbutes
            as values.
    """
    # First we get names of all Task class columns.
    columns = [c.key for c in class_mapper(task.__class__).columns
               if c.key != "owner"]
    # Then we return a dictionary of the columns names along with their
    # respective values for this particular instance of Task.
    return dict((c, getattr(task, c)) for c in columns)
