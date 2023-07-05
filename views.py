from flask import abort, request, redirect, render_template, session, url_for
import string
from random import randint, choice
from app import app

random_value = randint(1, 1000)
users = []
books = []


@app.get('/')
def links():
    return render_template('tasks/main_page.html'), 200


@app.route('/users', methods=['GET'])
def users_list(count=random_value):
    params = request.values.items()
    for key, value in params:
        count = int(value)
    k = 1
    while k <= count:
        users.append(''.join(choice(string.ascii_lowercase) for _ in range(randint(1, 8))))
        k += 1
    return render_template('tasks/users.html', users=users), 200


@app.route('/books', methods=['GET'])
def books_list(count=random_value):
    params = request.values.items()
    for key, value in params:
        count = int(value)
    k = 1
    while k <= count:
        books.append(''.join(choice(string.ascii_lowercase) for _ in range(randint(1, 8))))
        k += 1
    return render_template('tasks/books.html', books=books), 200


@app.get('/users/<user_id>')
def user_details(user_id):
    if int(user_id) % 2:
        abort(404, 'Not Found')
    return render_template('tasks/user_id.html', user=users[int(user_id) - 1]), 200


@app.get('/books/<book_name>')
def transform_name(book_name):
    lower_books = map(lambda word: word.lower(), books)
    if str(book_name) in lower_books:
        book_name = book_name.capitalize()
        return render_template('tasks/book_id.html', book=book_name), 200
    abort(404, 'There is no such book')


@app.get('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))


@app.route('/params', methods=['GET'])
def table():
    query_params = request.values.items()
    return render_template('tasks/params.html', dict=query_params), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('tasks/login.html')
    elif request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        if len(username) == 0 or len(password) == 0:
            abort(404, 'YOU HAVE NOT FILLED THE REQUIRED FIELDS')
        if len(password) >= 8 and len(username) >= 5:
            for symbol in password:
                if symbol.isupper():
                    for digit in password:
                        if digit.isdigit():
                            session['username'] = username
                            return redirect('/users')
                        else:
                            continue
                    return redirect('/login')
                else:
                    continue
            return redirect('/login')
        return redirect('/login')


@app.errorhandler(404)
def not_found_error(error):
    return '<h1>SOMETHING WENT WRONG</h1>', 404


@app.errorhandler(500)
def internal_server_error(error):
    return '<ul><li>Check the data</li><li>Maybe you have missed some info</li></ul>', 500


app.register_error_handler(404, not_found_error)
app.register_error_handler(500, internal_server_error)
