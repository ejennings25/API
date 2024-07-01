from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# added error handling using try-except block and jsonify
@app.errorhandler(Exception)
def handle_exception(error):
    message = str(error)  # Capture the error message
    return jsonify({'error': message}), 500  # Return JSON with error details



# set the Book model with appropriate data types and constraint
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(80), primary_key=True)
    publisher = db.Column(db.String(80), primary_key=True)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
    
# write crud for # id # book_name # author # publisher

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}

        output.append(book_data)

    return {"books": output}

@app.route('/books/<id>')
def get_books(id):
    books = Book.query.get_or_404(id)
    return {'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "Deleted"}

    
