from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models.models import db, User
from werkzeug.security import generate_password_hash
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "quiz_master"
db.init_app(app)

with app.app_context():
    db.create_all()

    admin_user = User.query.filter_by(role='admin').first()
    if not admin_user:

        hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')

        admin_user = User(email='admin@gmail.com', password=hashed_password, fullname='Admin', address='Admin', pin_code='123456', role='admin')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created")

from controllers.routes import *

if __name__ == "__main__":
    app.run(debug=True)