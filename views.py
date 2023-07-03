from flask import abort, request, redirect
import string
from random import randint, choice
from app import app

random_value = randint(1, 1000)
users = []
books = []


@app.get('/')
def links():
    return f'''
    <h1>LINKS:</h1>
    <ul>
        <li>users: <a href=http://127.0.0.1:5000/users>http://127.0.0.1:5000/users</a></li>
        <li>books: <a href=http://127.0.0.1:5000/books>http://127.0.0.1:5000/books</a></li>
        <li>login: <a href=http://127.0.0.1:5000/login>http://127.0.0.1:5000/login</a></li>
        <li>params: <a href=http://127.0.0.1:5000/params>http://127.0.0.1:5000/params</a></li>
    </ul>
    <table>
        <tr>
            <th>endpoint</th>
            <th>link</th>
            <th>purpose</th>
        </tr>
    </table>
    '''


@app.route('/users', methods=['GET'])
def users_list(count=random_value):
    params = request.values.items()
    for key, value in params:
        count = int(value)
    k = 1
    while k <= count:
        users.append(''.join(choice(string.ascii_lowercase) for _ in range(randint(1, 8))))
        k += 1
    user_render = ''.join([
        f"<li>{user}</li>"
        for user in users
    ])
    response = f'''
    <h1>Users</h1
    <ul>
        {user_render}
    </ul>
    '''
    return response, 200


@app.route('/books', methods=['GET'])
def books_list(count=random_value):
    params = request.values.items()
    for key, value in params:
        count = int(value)
    k = 1
    while k <= count:
        books.append(''.join(choice(string.ascii_lowercase) for _ in range(randint(1, 8))))
        k += 1
    book_render = ''.join([
        f"<li>{book}</li>"
        for book in books
    ])
    response = f'''
    <h1>BOOKS</h1>
    <ul>
        {book_render}
    </ul>
    '''
    return response, 200


@app.get('/users/<user_id>')
def user_details(user_id):
    if int(user_id) % 2:
        abort(404, 'Not Found')
    response = f'''
    <h1>{users[int(user_id) - 1]}</h1>
    '''
    return response, 200


@app.get('/books/<book_name>')
def transform_name(book_name):
    lower_books = map(lambda word: word.lower(), books)
    if str(book_name) in lower_books:
        book_name = book_name.capitalize()
        response = f'''
        <h1>The name of the book is: {book_name}</h1>
        '''
        return response, 200
    abort(404, 'There is no such book')


@app.route('/params', methods=['GET'])
def table():
    query_params = request.values.items()
    table = f'''
    <table>
        <tr>
            <th>key</th>
            <th>value</th>
        </tr>
    </table>
    '''
    for key, value in query_params:
        response = f'''
        <table>
            <tr>
                <th>{key}</th>
                <th>{value}</th>
            </tr>
        </table>
        '''
        table += response
    return table, 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return f'''
        <form method="POST" action="/login">
            <label for="username">username:</label>
            <input name="username" id="username"><br><br>
            <label for="password">password:</label>
            <input name="password" id="password"><br><br>
            <input type="submit" value="Submit">
        </form>
        '''
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
