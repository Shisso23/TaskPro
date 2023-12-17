from models.user import User, db


# Custom exception for registration errors
class RegistrationError(Exception):
    pass


# Logic for user registration
def extractAndStoreUser(data):
    try:
        # Check if the email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            raise RegistrationError('Email already exists')

        # Check if all required fields are present in the request
        required_fields = ['username', 'password', 'phone_number', 'userType', 'first_name', 'last_name', 'email']
        if not all(field in data for field in required_fields):
            raise RegistrationError('Missing required fields')

        username = data['username']
        password = data["password"]
        phone_number = data['phone_number']
        userType = data['userType']
        first_name = data["first_name"]
        last_name = data['last_name']
        email = data['email']

        # Create a new user
        new_user = User(username=username, password=password, phone_number=phone_number, userType=userType,
                        first_name=first_name, last_name=last_name, email=email)
        db.session.add(new_user)
        db.session.commit()

        # Create a user dictionary
        user_data = {
            'username': new_user.username,
            'phone_number': new_user.phone_number,
            'user_type': new_user.userType,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
        }
        return user_data

    except RegistrationError as e:
        raise e

    except Exception as e:
        raise RegistrationError(str(e))
