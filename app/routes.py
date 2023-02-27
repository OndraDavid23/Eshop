from datetime import timedelta
from ntpath import join
from urllib import response
from requests import request
from app import app, db, LoginManager
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import LoginForm, RegisterForm, PostForm
from app.models import User, Post, Category
from flask_login import current_user, login_fresh, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask import jsonify, request


@app.before_request
def make_session_permanent():
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes = 10)
    
@app.route("/api/user/<int:id>", methods = ["GET"])
def get_user(id):
    query = User.query.get_or_404(id)
    queryPosts = query.posts.all()
    query = query.to_dict()
    list = [post.to_dict() for post in queryPosts]
    query.update({"posts" : list})
    return jsonify(query) 

@app.route("/api/users", methods = ["GET"])
def get_users():
    data = User.to_collection_dict(User.query)

    return jsonify(data)

@app.route("/api/post/<int:id>", methods = ["GET"])
def get_post(id):
    return jsonify(Post.query.get_or_404(id).to_dict())

@app.route("/api/posts", methods = ["GET"])
def get_posts():
    data = Post.to_collection_dict(Post.query)
    print(data)
    return jsonify(data)

@app.route("/", methods = ["GET"])
def index():
    search = request.args.get("search")
    if search:
        posts = Post.query.join(Category).filter(Post.title.contains(search) | Post.body.contains(search) | Post.price.contains(search) | Category.name.contains(search))
        print(type(posts))
        for post in posts:
            print(post.postCat.name)
        if len(posts.all()) == 0:
            posts = Post.query.order_by(Post.date_added.desc())
    else:
        posts = Post.query.order_by(Post.date_added.desc())
    return render_template("index.html", posts = posts)


@app.route("/register", methods = ["POST", "GET"])
def register():
    form = RegisterForm()
    if current_user.is_anonymous:
        if form.validate_on_submit():
            print("form validated")
            user = User(username = form.username.data, email = form.email.data, mobile = form.mobile.data )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            print("user registered")
            return redirect(url_for("index"))
        return render_template("register.html", form = form)
    return redirect(url_for("index"))



@app.route("/login", methods = ["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("User doesnt exist or the password was incorect", "error")
            print("Bad user")
            return render_template("login.html", form = form)
            # return redirect(url_for("index"))

        login_user(user, remember = form.remember.data)
        print("user logged in") 
        print(current_user)
        next_page = request.args.get("next")
        if next_page is None or url_parse(next_page).netloc != "":
            flash("You have been logged in.", "succes")
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form = form)


@app.route("/new_post", methods = ["POST", "GET"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        print(form.category.data)
        post = Post(user_id = current_user.id, title = form.title.data, body = form.body.data, price = int(form.price.data), PSC = int(form.PSC.data), category_id = form.category.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("new_post.html", form = form)

@app.route("/logout", methods = ["POST", "GET"])
def logout():
    print("user logged out")
    logout_user()
    print(current_user)
    return redirect(url_for("index"))

@app.route("/post/<int:id>")
def post(id):
    print(id)
    post = Post.query.filter_by(id = id).first()
    print(post.id)
    return render_template("post.html", post = post)

@app.route("/user/<username>", methods = ["GET"])
@login_required
def user_profile(username):
    
    user_posts = Post.query.filter(Post.user_id == current_user.id)
    return render_template("user_profile.html", user_posts = user_posts)

@app.route("/delete/<id>", methods = ["POST"])
def delete(id):
    post = Post.query.filter_by(id = id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("user_profile", username = current_user.username))

# @app.route("/category", methods = ["GET", "POST"]):
# def category():
#     categories = Category.query.order_by