from flask import Flask, jsonify
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy


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
    name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(80), primary_key=True)
    publisher = db.Column(db.String(80), primary_key=True)

    def __repr__(self):
        return f"{self.name} - {self.author} - {self.publisher}"
    
# write crud for # id # book_name # author # publisher

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'name': book.name, 'author': book.author, 'publisher': book.publisher}

        output.append(book_data)

    return {"books": output}