#!/usr/bin/python3

"""List States and State"""

from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def state_list():
    """States List"""
    states = storage.all('State').values()
    return render_template(
        "9-states.html",
        states=states,
        condition="states_list")


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """State by ID"""
    all_states = storage.all('State')
    key = "State.{}".format(id)
    try:
        state = all_states[key]
        return render_template(
            '9-states.html',
            state=state,
            condition="state_id")
    except BaseException:
        return render_template('9-states.html', condition="not_found")


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
