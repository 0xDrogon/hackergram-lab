from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['SECRET_KEY'] = '\xa6Y\xa7?5\xd3\xb75\x02B\x85\x87s\x02\xbf\x03\xdc\xef\xad\xbc\x15\xb1\x1d\xcc'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'hackergram'
app.config['MYSQL_PASSWORD'] = 'hackergrampass'
app.config['MYSQL_DB'] = 'hackergramdb'
app.config['photos_folder'] = './static/photos/'
app.config['MAX_CONTENT_PATH'] = 102400

mysql = MySQL(app)

@app.context_processor
def inject():
    return {'photos_folder' : app.config['photos_folder']}

from models import *
from views import * 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)