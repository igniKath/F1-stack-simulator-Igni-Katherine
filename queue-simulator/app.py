
"""Flask Queue Simulator - Week 13"""

import os
import secrets

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from queue_model import Queue

app = Flask(__name__)

# Secret key for Flask sessions and flash messages
app.config['SECRET_KEY'] = (
    os.environ.get('SECRET_KEY') or secrets.token_hex(32)
)


@app.route('/')
def index():
    # Restore queue items and removed items from the session
    queue = Queue()
    queue.items = list(session.get('items', []))
    queue.removed = list(session.get('removed', []))

    return render_template(
        'index.html',
        items=queue.items,
        size=queue.size(),
        removed=queue.removed,
        highlight=request.args.get('peek') == '1',
        live=True,
    )


@app.route('/queue', methods=['POST'])
def operate():
    # Get the submitted action and value
    action = request.form.get('action', '')
    value = request.form.get('value', '').strip()

    # Restore the Queue from the session
    queue = Queue()
    queue.items = list(session.get('items', []))
    queue.removed = list(session.get('removed', []))

    highlight = False

    # ENQUEUE: Add an item to the rear
    if action == 'enqueue':
        if not value or len(value) > 24:
            flash('Enter 1 to 24 characters.', 'error')

        elif queue.size() >= 20:
            flash('Limit: 20 items.', 'error')

        else:
            queue.enqueue(value)
            flash(f'Enqueued: {value}', 'success')

    # DEQUEUE: Remove the front item
    elif action == 'dequeue':
        removed = queue.dequeue()

        if removed is None:
            flash('Queue is empty. Nothing to dequeue.', 'error')
        else:
            flash(f'Dequeued: {removed}', 'success')

    # PEEK: View the front item without removing it
    elif action == 'peek':
        front = queue.peek()

        if front is None:
            flash('Queue is empty. Nothing to peek.', 'error')
        else:
            flash(f'Front: {front}', 'success')
            highlight = True

    # CLEAR: Remove all queue items and removed history
    elif action == 'clear':
        queue.clear()
        flash('Queue and removed items cleared.', 'success')

    else:
        flash('Unknown operation.', 'error')

    # Save the updated Queue in the session
    session['items'] = queue.items
    session['removed'] = queue.removed

    # Return to the main page
    if highlight:
        return redirect(url_for('index', peek='1'))

    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
