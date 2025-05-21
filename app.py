from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB and table if not exists
def init_db():
    with sqlite3.connect('library.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL
            )
        ''')
init_db()

@app.route('/')
def index():
    with sqlite3.connect('library.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        with sqlite3.connect('library.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
            conn.commit()
        return redirect('/')
    return render_template('add_book.html')

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    with sqlite3.connect('library.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)