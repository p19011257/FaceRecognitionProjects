from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
mysql = MySQL()

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER='website/imagesAttendance/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # upload image folder
    app.config['SECRET_KEY'] = 'chunyee518'
    app.config['MAX_CONTENT_LENGTH']=16*1024*1024
    app.config['MYSQL_HOST'] = 'localhost' #database settings
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'users_db'


    mysql.init_app(app)





    from .views import views
    from .auth import auth
    from .test import test

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(test, url_prefix='/')

    return app