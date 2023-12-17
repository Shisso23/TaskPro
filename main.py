from flask import Flask, request, jsonify
from flask_cors import CORS
from models.user import db
from flask_bcrypt import Bcrypt
from businesslogic import userLogic

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:DavidEbula1999@localhost:3306/taskpro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BCRYPT_LOG_ROUNDS'] = 12

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        data['password'] = hashed_password

        # Extract information from the request and store user
        user_data = userLogic.extractAndStoreUser(data)

        return jsonify({'user': user_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
