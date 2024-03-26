import os
import secrets
from PIL import Image
from connectify import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from connectify.forms import RegistrationForm, LoginForm, UpdateAccountForm, PitchForm
from connectify.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.first_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login Successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('home'))
        else:
            flash(f'Login Unsucessful! Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Account Updated Successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='profile/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Post(title=form.title.data, author=current_user, introduction=form.introduction.data, problem_statement=form.problem_statement.data, solution=form.solution.data,  market_analysis=form.market_analysis.data, financial_projection=form.financial_projection.data)
        db.session.add(pitch)
        db.session.commit()
        flash('Your pitch has been created!', 'success')
        return redirect(url_for('business'))
    return render_template('pitch.html', title='Pitch', legend='Begin Here', form=form)


@app.route('/business', methods=['GET', 'POST'])
def business():
        posts = Post.query.all()
        return render_template('business.html', title='Business', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PitchForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.introduction = form.introduction.data
        post.problem_statement = form.problem_statement.data
        post.solution = form.solution.data
        post.market_analysis = form.market_analysis.data
        post.financial_projection = form.financial_projection.data
        db.session.commit()
        flash('Pitch has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.introduction.data = post.introduction
        form.problem_statement.data = post.problem_statement
        form.solution.data = post.solution
        form.market_analysis.data = post.market_analysis
        form.financial_projection.data = post.financial_projection
    return render_template('pitch.html', title='Edit Pitch', legend='Edit Pitch', form=form)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your pitch has been deleted!', 'success')
    return redirect(url_for('home'))

