from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class posts(db.Model):
    Srno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80), nullable=False)
    Content = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=False)
    Slug = db.Column(db.String(25), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about.html")
def about():
    return render_template('about.html')

@app.route("/poster/<string:post_slug>", methods=(['GET']))
def post_route(post_slug):
    post= posts.query.filter_by(Slug=post_slug).first()
    return render_template('post.html' ,post=post)


@app.route("/contact.html", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


app.run(debug=True)

