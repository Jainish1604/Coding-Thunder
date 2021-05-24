from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'Jl'
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:" "@localhost/coders"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class contacts(db.Model):
    Srno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email_address = db.Column(db.String(20), nullable=False)
    Phone_no = db.Column(db.String(12), nullable=False)
    Msg = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)


class Posts(db.Model):
    Srno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80), nullable=False)
    Content = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=False)
    Slug = db.Column(db.String(25), nullable=True)


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)


@app.route("/about.html")
def about():
    return render_template('about.html', params=params)


@app.route("/post/<string:post_slug>", methods=(['GET']))
def post_route(post_slug):
    post = Posts.query.filter_by(Slug=post_slug).first()
    return render_template('post.html', post=post, params=params)


@app.route("/login.html", methods=['GET', 'POST'])
def login():
    return render_template('login.html', params=params)


@app.route("/contact.html", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('massage')
        entry = contacts(Name=name,
                         Phone_no=phone,
                         Msg=message,
                         Date=datetime.now(),
                         Email_address=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if "user" in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template("Dashboard.html", params=params, posts=posts)

    if request.method == "POST":
        username = request.form.get("user")
        userpass = request.form.get("passw")
        if username == params['admin_user'] and userpass == params[
                'admin_password']:
            # set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template("Dashboard.html",
                                   params=params,
                                   posts=posts)
    else:
        return render_template("login.html", params=params)


@app.route("/edit/<string:Srno>", methods=['GET', 'POST'])
def Edit(Srno):
    if "user" in session and session['user'] == params['admin_user']:
        if request.method == "POST":
            E_title = request.form.get("title")
            E_content = request.form.get("content")
            E_slug = request.form.get("slug")
            if Srno == "0":
                post = Posts(Title=E_title,
                             Content=E_content,
                             Slug=E_slug,
                             Date=datetime.now())
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(Srno=Srno).first()
                post.title = E_title
                post.content = E_content
                post.slug = E_slug
                db.session.commit()
                return redirect('/edit/'+Srno)
        post = Posts.query.filter_by(Srno=Srno).first()
        return render_template("edit.html", params=params, post=post ,Srno=Srno)


app.run(debug=True)