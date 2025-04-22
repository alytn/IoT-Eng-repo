from flask import Flask
from views import views
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from database import db

app = Flask(__name__)
app.secret_key = "RaspberryPi for dessert"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=15)

#app.register_blueprint(views, url_prefix="/views") adds /views to url
app.register_blueprint(views)
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)