from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory list of books (replace with a database for persistence)
books = []

class Book:
  def __init__(self, id, book_name, author, publisher):
    self.id = id
    self.book_name = book_name
    self.author = author
    self.publisher = publisher

# Generate a unique ID for new books
def generate_id():
  if not books:
    return 1
  return books[-1].id + 1

# Create a new book
@app.route('/books/create', methods=['POST'])
def create_book():
  data = request.get_json()
  if not data or not data.get('book_name') or not data.get('author') or not data.get('publisher'):
    return jsonify({'error': 'Missing required fields'}), 400
  new_book = Book(generate_id(), data['book_name'], data['author'], data['publisher'])
  books.append(new_book)
  return jsonify({'message': 'Book created successfully', 'book': new_book.__dict__}), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
  return jsonify({'books': [book.__dict__ for book in books]})

# Get a book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
  book = [book for book in books if book.id == book_id]
  if not book:
    return jsonify({'error': 'Book not found'}), 404
  return jsonify({'book': book[0].__dict__})

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
  data = request.get_json()
  if not data:
    return jsonify({'error': 'Missing data'}), 400
  book_index = [i for i, book in enumerate(books) if book.id == book_id]
  if not book_index:
    return jsonify({'error': 'Book not found'}), 404
  updated_book = Book(book_id, data.get('book_name', books[book_index[0]].book_name), 
                      data.get('author', books[book_index[0]].author), 
                      data.get('publisher', books[book_index[0]].publisher))
  books[book_index[0]] = updated_book
  return jsonify({'message': 'Book updated successfully', 'book': updated_book.__dict__})

# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
  book_index = [i for i, book in enumerate(books) if book.id == book_id]
  if not book_index:
    return jsonify({'error': 'Book not found'}), 404
  del books[book_index[0]]
  return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
  app.run(debug=True)