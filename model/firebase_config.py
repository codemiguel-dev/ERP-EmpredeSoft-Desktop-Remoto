import firebase_admin
from firebase_admin import credentials, db, storage

# Ruta al archivo JSON de configuración de Firebase
cred = credentials.Certificate('connect.json')

# Inicialización de la aplicación Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://desktop-program-emprendesoft-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'desktop-program-emprendesoft.appspot.com'  # Reemplaza '<tu-bucket>' con el nombre de tu bucket de Storage
})

# Obtener una referencia a la base de datos en tiempo real de Firebase
firebase_db = db.reference()

# Obtener una referencia a Firebase Storage
storage_bucket = storage.bucket()
