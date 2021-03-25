from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/login'
db = SQLAlchemy(app)



class Login(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/', methods=["GET","POST"])
def home():
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('passw')
        admin = Login(email=email, password=password)
        db.session.add(admin)
        db.session.commit()
    return render_template('Login.html')


if __name__ == '__main__':
   app.run(debug = True)