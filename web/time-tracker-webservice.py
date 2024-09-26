## time-tracker-webservice solution
import flask
import pprint

app = flask.Flask(__name__)

tasks = [
    {
        'id': 1,
        'name': u'fixing bug #1',
        'time_spent': 20  # in mins
    },
    {
        'id': 2,
        'name': u'customer support',
        'time_spent': 30
    }
]

# find the task from the list, None if not found
def find_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

@app.route('/')
def index():
    ret_value = {'status': 'ok'}
    return flask.jsonify(ret_value)

## ----------- list all tasks --------
@app.route('/tasks/', methods=['GET'])
@app.route('/tasks/list', methods=['GET'])
def get_tasks_list():
    ret_value = {'status': 'ok', 'tasks': tasks}
    if app.debug:
        print("get_tasks_list: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
    return flask.jsonify(ret_value)
## ----------- end: list all tasks --------

## ----------- get ONE task --------
@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    ret_value = {}
    task = find_task(task_id)
    if task:
        ret_value['status'] = 'ok'
        ret_value['task'] = task
    else:
        ret_value['status'] = 'error'
        ret_value['description'] = 'no task with id {}'.format(task_id)
        # flask.abort(404)

    if app.debug:
        print("get_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
    return flask.jsonify(ret_value)
## ----------- end: get ONE task --------

## ----------- create new task --------
@app.route('/task/new', methods=['POST'])
def create_task():
    ret_value = {}
    if not flask.request.json or not 'name' in flask.request.json:
        ret_value['status'] = 'error'
        ret_value['description'] = "need 'name' for task"
    else:  # create a new task
        name = flask.request.json['name']
        task = {
            'id': tasks[-1]['id'] + 1 if tasks else 1,  # Increment last task id or start at 1
            'name': name,
            'time_spent': 0  # Default time spent is 0
        }

        tasks.append(task)

        ret_value['status'] = 'ok'
        ret_value['task'] = task

    if app.debug:
        print("create_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
    return flask.jsonify(ret_value)
## ----------- end: create new task --------

## ----------- update a task --------
@app.route('/task/update/<int:task_id>', methods=['PUT', 'POST'])
def update_task(task_id):
    ret_value = {}
    task = find_task(task_id)
    if not task:
        ret_value['status'] = 'error'
        ret_value['description'] = 'no task with id {}'.format(task_id)
        if app.debug:
            print("update_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
        return flask.jsonify(ret_value)
        # flask.abort(404)
    if not flask.request.json:
        ret_value['status'] = 'error'
        ret_value['description'] = 'missing parameters'
        if app.debug:
            print("update_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
        return flask.jsonify(ret_value)

    if not 'time' in flask.request.json:
        ret_value['status'] = 'error'
        ret_value['description'] = "missing 'time'"
        if app.debug:
            print("update_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
        return flask.jsonify(ret_value)

    # now update the task
    time = flask.request.json['time']
    task['time_spent'] += int(time)

    ret_value['status'] = 'ok'
    ret_value['task'] = task
    if app.debug:
        print("update_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
    return flask.jsonify(ret_value)
## ----------- end : update a task --------

## ----------- delete a task --------
@app.route('/task/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        ret_value = {'status': 'error',
                     'description': 'no task with id {}'.format(task_id)}
        if app.debug:
            print("delete_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
        return flask.jsonify(ret_value)
        # flask.abort(404)

    tasks.remove(task)
    ret_value = {'status': 'ok',
                 'description': 'removed task id {}'.format(task_id)}
    if app.debug:
        print("delete_task: Returning \n{}".format(pprint.pformat(ret_value, indent=4)))
    return flask.jsonify(ret_value)
## ----------- end : delete a task --------

if __name__ == '__main__':
    app.run(debug=True)
