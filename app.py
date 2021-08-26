from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
app.config['SECRET_KEY']='thisissecretkey'

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))


class users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(40),nullable=False)


@app.route('/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        d=users.query.filter_by(email=email).first()
                
        if d:
            if d.password==password:
                login_user(d)
                return redirect('/home')
        else:
            return redirect('/')
    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        user=users(name=name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__=='__main__':
    app.run()

