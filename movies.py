from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

users = {
    "admin": "admin123", "user": "user123"
}

tokens = {}
movies = []
bookings = []

# Login API WITH JWT TOKEN
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        token = jwt.encode({
            "username" : username,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=1)

        }, app.config['SECRET_KEY'], algorithm = 'HS256')

        return jsonify({"Message": "Login is successful", "Token": token}), 200
    else:
        return jsonify({'Error': "Invalid credentials"}), 401

# Middleware API
def authenticate_request():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'Error':'Token is missing'})
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithm = ['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return jsonify({'Error':'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'Error':'Invalid Token'}), 401


# POST MOVIES
@app.route('/api/movies', methods=['POST'])
def add_movie():
    auth_response = authenticate_request()  
    if isinstance(auth_response, dict): 
        data = request.get_json()  
        new_movie = {
            "id": len(movies) + 1, 
            "title": data.get("title"), 
            "year": data.get("year")
        }

        movies.append(new_movie)  
        return jsonify({"Message": "New movie added"}), 201
    return auth_response 

# GET MOVIES
@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

# UPDATE A MOVIE
@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movies(id):
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    data = request.get_json()
    for movie in movies:
        if movie['id'] == id:
            movie.update(data)
            return jsonify({'Message': 'Movie updated'})

    return jsonify({'Error': 'Movie not found'}), 404

# DELETE A MOVIE
@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return jsonify({'Message': 'Movie is deleted'})
    return jsonify({'Error': 'Movie not found'}), 404

# BOOK MOVIE TICKET
@app.route('/api/bookings', methods=['POST'])
def book_ticket():
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    data = request.get_json()
    id = data.get('movie_id')

    for movie in movies:
        if movie['id'] == id:
            booking = {
                "id": len(bookings) + 1,
                "title": "Dune 2",
                "year": 2024
            }
            bookings.append(booking)
            return jsonify({"Message": "Booking successful", "Booking Details": booking}), 201
    return jsonify({'Error': 'Movie not found'}), 404

# GET ALL BOOKINGS
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    user = request.headers.get('Authorization').split('-')[0]
    user_bookings = [booking for booking in bookings if booking['user'] == user]
    return jsonify(user_bookings), 200

# ERROR HANDLERS
@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({'Error': 'Bad request', 'Message': str(error)})

@app.errorhandler(401)
def handle_unauthorized(error):
    return jsonify({'Error': 'Unauthorized', 'Message': str(error)})

@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({'Error': 'Not found', 'Message': str(error)})

if __name__ == '__main__':
    app.run(debug=True)
