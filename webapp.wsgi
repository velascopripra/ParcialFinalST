import sys
import os

# Añadir el directorio del proyecto al path
sys.path.insert(0, '/var/www/webapp')

# Establecer la variable de entorno de configuración
os.environ['FLASK_ENV'] = 'production'

from web.views import app as application
