import firebase_admin
from firebase_admin import credentials, db
from model.firebase_config import firebase_db, storage_bucket
import uuid
import bcrypt
import base64

class UserModel:
    def __init__(self):
        pass

    def register_user(self, username, password, email, role):
        try:
            uid = str(uuid.uuid4())  # Generar un UID único
              # Verifica si el rol es nulo o vacío y establece "standard" por defecto
            if not role:
                role = "Estándar"
            # Generar un salt y hashear la contraseña
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            # Convertir el hash a una cadena de texto usando base64 urlsafe
            hashed_password_str = base64.urlsafe_b64encode(hashed_password).decode('utf-8')

            firebase_db.child('users').child(uid).set({
                'uid': uid,
                'name': username,
                'email': email,
                'password': hashed_password_str,
                'role': role
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
                    uid =  user['uid']
                    name =  user['name']
                    email = user['email']
                    role = user['role']
                    image = user['image']
                    # Decodificar el hash de la contraseña usando base64 urlsafe
                    stored_hash = base64.urlsafe_b64decode(user['password'])
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        return uid, role, name, email, password, image
            return None
        except Exception as e:
            print(f"Error verifying user: {e}")
            return None

    def get_users(self):
        users = firebase_db.child('users').get()
        return users if users else {}

    def get_user_data(self, user_key):
        return firebase_db.child('users').child(user_key).get()

    def get_users_count(self):
        users = firebase_db.child('users').get()
        return len(users) if users else 0

    def update_user(self, uid, name, email, role, password):
        try:
            # Generar un salt y hashear la contraseña
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            # Convertir el hash a una cadena de texto usando base64 urlsafe
            hashed_password_str = base64.urlsafe_b64encode(hashed_password).decode('utf-8')

            firebase_db.child('users').child(uid).update({
                'name': name,
                'email': email,
                'role': role,
                'password': hashed_password_str
            })
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, uid):
        try:
            firebase_db.child('users').child(uid).delete()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def update_profile(self, uid, name, email, role, password, image):
        try:
            # Generar un salt y hashear la contraseña
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            # Convertir el hash a una cadena de texto usando base64 urlsafe
            hashed_password_str = base64.urlsafe_b64encode(hashed_password).decode('utf-8')

             # Generar un UID único para la imagen y crear un blob en Firebase Storage
            image_uid = str(uuid.uuid4())
            blob = storage_bucket.blob(f'images/profile/{image_uid}')

            # Subir la imagen a Firebase Storage
            blob.upload_from_filename(image)

            # Construir la URL pública de la imagen manualmente
            bucket_name = storage_bucket.name
            image_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/images%2Fprofile%2F{image_uid}?alt=media"

            firebase_db.child('users').child(uid).update({
                'name': name,
                'email': email,
                'role': role,
                'password': hashed_password_str,
                'image': image_url
            })
            return True , "Cuenta actualizada exitosamente."
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
