import firebase_admin
from firebase_admin import credentials, db
from model.firebase_config import firebase_db
import uuid
import bcrypt
import base64

class ProviderModel:
    def __init__(self):
        pass

    def register_provider(self, name, bunisessocial, linksocial, address, email, phone):
        try:
            uid = str(uuid.uuid4())  # Generar un UID único
              # Verifica si el rol es nulo o vacío y establece "standard" por defecto

            firebase_db.child('provider').child(uid).set({
                'uid': uid,
                'name': name,
                'bunisessocial': bunisessocial,
                'linksocial': linksocial,
                'address': address,
                'email': email,
                'phone': phone
            })
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False

    def user_exists(self, username):
        try:
            users = firebase_db.child('users').get()
            if users is None:
                return False
            for uid, user in users.items():
                if user['name'] == username:
                    return True
            return False
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False

    def verify_user(self, username, password):
        try:
            users = firebase_db.child('users').get()
            if users is None:
                return None
            for uid, user in users.items():
                if user['name'] == username:
                    # Decodificar el hash de la contraseña usando base64 urlsafe
                    stored_hash = base64.urlsafe_b64decode(user['password'])
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        return user['role']
            return None
        except Exception as e:
            print(f"Error verifying user: {e}")
            return None

    def get_providers(self):
        providers = firebase_db.child('provider').get()
        return providers if providers else {}

    def get_user_data(self, user_key):
        return firebase_db.child('users').child(user_key).get()

    def get_users_count(self):
        users = firebase_db.child('users').get()
        return len(users) if users else 0

    def update_provider(self, uid, name, bunisessocial, linksocial, address, email, phone):
        try:
            firebase_db.child('provider').child(uid).update({
                'name': name,
                'bunisessocial': bunisessocial,
                'linksocial': linksocial,
                'address': address,
                'email': email,
                'phone': phone
            })
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def delete_provider(self, uid):
        try:
            firebase_db.child('provider').child(uid).delete()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
