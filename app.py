"""Flask Stack Simulator starter: complete TODOs during the live demo.
Before class, preview templates/index.html directly in the browser.
Running this file starts a status page, not the completed simulator.
"""
import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash
from stack_model import Stack

# TODO P1: Extend the imports with render_template, request, redirect,CHECKED

# url_for, session, and flash. Import secrets and the completed Stack class.
app = Flask(__name__)
# TODO P2: Set SECRET_KEY for the session and flash messages.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
# This lesson uses short fictional stack values on localhost.


@app.route('/')
def index():
    # TODO P3: Replace this temporary response with render_template.
    # Start by displaying the static index.html through Flask.
    # TODO P6: Restore stack values from session, reverse for display,
    # and pass items, size, popped, and highlight to the template.
    stack = Stack(session.get('items', []))
    return render_template(
        'index.html',
        items=list(reversed(stack.items)),
        size=stack.size(),
        popped=session.get('popped', []),
        highlight=request.args.get('peek') == '1',
        live=True,
    )


@app.route('/stack', methods=['POST'])
def operate():
    # TODO P4: Read action and value from request.form. Strip the value.
    # TODO P7: Restore the Stack and removed-item history from session.
    # TODO P8: Implement Push, Pop, Peek, and Clear with feedback.
    # Push accepts 1-24 characters and at most 20 current items.
    # Pop and Peek must handle an empty stack. Clear resets both lists.
    # Keep only the 20 most recently removed values.
    # TODO P9: Reassign session values, then redirect to the index route.
    # Use a peek flag when highlighting the top item.
    action = request.form.get('action', '')
    value = request.form.get('value', '').strip()
    stack = Stack(session.get('items', []))
    popped = list(session.get('popped', []))
    highlight = False

    if action == 'push':
        if not value or len(value) > 24:
            flash('Enter 1 to 24 characters.', 'error')
        elif stack.size() >= 20:
            flash('limit: 20 items', 'error')
        else:
            stack.push(value)
            flash(f'Pushed: {value}', 'success')
    elif action == 'pop':
        removed = stack.pop()
        if removed is None:
            flash('Stack is empty.', 'error')
        else:
            popped.insert(0, removed)
            popped = popped[:20]
            flash(f'Popped: {removed}', 'success')
    elif action == 'peek':
        top = stack.peek()
        flash(
            'Stack is empty.' if top is None else f'Top: {top}',
            'error' if top is None else 'success',
        )
        highlight = top is not None
    elif action == 'clear':
        stack.clear()
        popped.clear()
        flash('Stack and deleted history cleared.', 'success')
    else:
        flash('Unknown Operation', 'error')

    session['items'] = stack.items
    session['popped'] = popped
    return redirect(url_for('index', peek='1') if highlight else url_for('index'))


@app.route('/contact')
def contact():
    # TODO P5: Render contact.html as a placeholder landing page.
    # A validated contact form belongs to a later lesson.
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()  # Local development only. Stop with Ctrl+C.
