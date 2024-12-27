import sys
from cx_Freeze import setup, Executable

# Dependencias adicionales que puedas tener
build_exe_options = {
    "packages": ["PyQt5", "requests"],
    "include_files": ["image/icon.png", "view/","image/","model/","controller/","design/","connect.json"],  # Archivos adicionales que tu aplicación necesita (imágenes, vistas, etc.)
    "excludes": [],
    "include_msvcr": True  # Incluye MSVC runtime
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Para ocultar la consola en la versión con GUI en Windows

# Configuración para generar el ejecutable
setup(
    name="EmprendeSoft",
    version="1.0",
    description="Software para pymes",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.pyw", base=base, icon="image/icon.ico")]  # Reemplaza main.pyw con el nombre de tu script principal
)
