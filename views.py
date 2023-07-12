from flask import abort, request, redirect, render_template, session, url_for
from random import randint
from app import app, db
from models import Users, Books, Purchases

random_value = randint(1, 1000)
users = []
books = []


@app.get('/')
def links():
    return render_template('tasks/main_page.html'), 200


@app.route('/users', methods=['GET'])
def users_list(count=5):
    params = request.values.items()
    for key, value in params:
        count = int(value)
    query = db.select(Users.user).order_by(Users.user).limit(count)
    users = db.session.execute(query).scalars()
    return render_template('tasks/users.html', users=users)


@app.route('/books', methods=['GET'])
def books_list():
    params = request.values.items()
    for key, value in params:
        count = int(value)
    if not params:
        for key, value in params:
            count = int(value)
        query = db.select(Books.book).order_by(Books.book).limit(count)
        books = db.session.execute(query).scalars()

    else:
        query = db.select(Books.book).order_by(Books.book)
        books = db.session.execute(query).scalars()
    return render_template('tasks/books.html', books=books), 200


@app.get('/users/<user_id>')
def user_details(user_id):
    if int(user_id) % 2:
        abort(404, 'Not Found')
    query = db.select(Users.user)
    user = db.session.execute(query).scalars().fetchall()
    return render_template('tasks/user_id.html', user=user[int(user_id) - 1]), 200


@app.get('/books/<book_id>')
def transform_name(book_id):
    query = db.select(Books.book)
    books = db.session.execute(query).fetchall()
    if book_id > len(books):
        abort(404, 'Not Found')
    return render_template('tasks/book_id.html', book=books[int(book_id) - 1]), 200


@app.get('/purchases')
def purchases():
    query_book = db.select(Purchases.purchased_book)
    query_owner = db.select(Purchases.owner)
    purchased_books = db.session.execute(query_book).fetchall()
    owners = db.session.execute(query_owner).fetchall()
    return render_template('tasks/purchases.html', owners=owners, books=purchased_books)


@app.get('/purchases/<purchase_id>')
def owner_info(purchase_id):
    query_book = db.select(Purchases.purchased_book)
    query_owner = db.select(Purchases.owner)
    purchased_books = db.session.execute(query_book).fetchall()
    owners = db.session.execute(query_owner).fetchall()
    if int(purchase_id) > len(owners):
        abort(404)
    return render_template('tasks/purchases_id.html',
                           owner=owners[int(purchase_id) - 1],
                           book=purchased_books[int(purchase_id) - 1])


@app.get('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))


@app.route('/params', methods=['GET'])
def table():
    query_params = request.values.items()
    return render_template('tasks/params.html', dict=query_params), 200


@app.route('/application', methods=['GET', 'POST'])
def add_elements():
    if request.method == 'GET':
        return render_template('tasks/application.html')
    elif request.method == 'POST':
        user = str(request.form['user'])
        book = str(request.form['book'])
        new_user = Users(user=user)
        new_book = Books(book=book)
        db.session.add(new_user)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/users')


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