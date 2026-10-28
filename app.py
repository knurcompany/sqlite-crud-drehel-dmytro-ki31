"""Дрегель Дмитро, група КІ-31. Простий облік прочитаних книг."""
from flask import Flask, abort, redirect, render_template, request, url_for
import database_connector as db

app = Flask(__name__)
STATUSES = ('Планую', 'Читаю', 'Прочитано')
db.create_db_table()


def read_form():
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    status = request.form.get('status', '')
    try:
        year = int(request.form.get('year', ''))
    except ValueError:
        raise ValueError('Рік має бути цілим числом.')
    if not title or not author:
        raise ValueError('Заповніть назву та автора.')
    if not 1 <= year <= 2100 or status not in STATUSES:
        raise ValueError('Перевірте рік та стан читання.')
    return title, author, year, status


@app.route('/')
def index():
    return render_template('index.html', items=db.get_all_items())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            data = read_form()
        except ValueError as error:
            return render_template('form.html', item=request.form, statuses=STATUSES,
                                   error=str(error)), 400
        db.insert_item(data)
        return redirect(url_for('index'))
    return render_template('form.html', item={}, statuses=STATUSES)


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = db.get_item_by_id(item_id)
    if item is None:
        abort(404)
    if request.method == 'POST':
        try:
            data = read_form()
        except ValueError as error:
            return render_template('form.html', item=request.form, statuses=STATUSES,
                                   error=str(error)), 400
        db.update_item(item_id, data)
        return redirect(url_for('index'))
    return render_template('form.html', item=item, statuses=STATUSES)


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    if not db.delete_item(item_id):
        abort(404)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5057)
