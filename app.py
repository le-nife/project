from flask import Flask,flash, render_template,request, redirect,url_for,session
from registerforms import RegisterForm, LoginForm, AddBlogForm
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
app = Flask(__name__)
app.secret_key="twenty"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    blogs=db.relationship("Blog", backref='author', lazy=True, cascade='all,delete-orphan')
    
    def __init_(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(1000))
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    def __init__(self, title, content, image, user_id):
        self.title=title
        self.content=content
        self.image=image
        self.user_id=user_id


@app.route("/")
def home():
    blogs = Blog.query.all()
    print("Blogs", Blog)
    return render_template("home.html", blogs = blogs)

@app.route("/blogs")
@login_required
def blogs():
    blogs=Blog.query.all()
    return render_template("blogs.html",user=current_user,  blog= current_user.blogs)

@app.route("/add-blog", methods = ['GET','POST'])
@login_required
def addblog():
    Blogform = AddBlogForm()
    if request.method == 'POST':
        blog_title = Blogform.title.data
        blog_content = Blogform.content.data
        blog_image = Blogform.image.data
        filename = blog_image.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        blog_image.save(filepath)
        new_blog = Blog(title=blog_title, content=blog_content, image =filename, user_id=current_user.id)
        db.session.add(new_blog)
        db.session.commit()
        # print("added.")
        flash("Blog added successfully","success")
        return redirect(url_for("blogs"))
    return render_template("add-blog.html", form = Blogform)

@app.route("/view/<blogname>")
@login_required
def viewblog(blogname):
    blog=Blog.query.filter_by(title=blogname).first()
    return render_template("view-blog.html", blog=blog)

@app.route("/delete/<id>")
def deleteblog(id):
    blog=Blog.query.get(id)
    if blog:
        db.session.delete(blog)
        db.session.commit()
        flash("blog deleted successfully","success")
    return redirect(url_for("blogs"))


@app.route("/Register", methods = ['GET', 'POST'])
def register():
    registerform = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = registerform.username.data
        email= registerform.email.data
        password = registerform.password.data
        confirm = registerform.confirm_password.data
        
        session['username'] = username
        session['email']= email
        
        if not username or not email or not password:
            flash('All fields are required', 'danger')
        elif password != confirm:
            flash('Passwords do not match', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Username not available', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
        else:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            print(hashed_pw)
            user = User(username=username, email=email, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('Bingo', 'success')
            return redirect(url_for('login'))
        
    return render_template("register.html", form=registerform)

@app.route("/Login", methods = ['GET', 'POST'])
def login():
    loginform = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email= loginform.email.data
        password = loginform.password.data
        remember = loginform.remember_me.data
        user=User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('logged in successfully', 'success')
            return redirect(url_for('blogs'))
        else:
            flash("login failed. Check the email and password", "danger")
            
    return render_template('login.html', form = loginform)
    
    
@app.route("/logout")
@login_required
def logout():
    session.pop("username",None)
    logout_user()
    flash('you have been logged out', 'flash')
    return redirect (url_for("login"))


@app.route("/update/<id>", methods = ['GET', 'POST'])
def updateblog(id):
    blog=Blog.query.get(id)
    if request.method == 'POST':
        blog_title = Blogform.title.data
        blog_content = Blogform.content.data
        blog_image = Blogform.image.data
        file = request.files['Blog_image']
        if file and file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            blog.image = filename 

        db.session.commit()
        flash("user updated successfully","success")
        return redirect(url_for("blogs"))
    else:
        return render_template("updateblogs.html", blog=blog)
with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug= True)