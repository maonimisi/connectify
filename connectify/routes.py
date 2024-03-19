from flask import render_template, url_for, flash, redirect
from connectify import app
from connectify.forms import RegistrationForm, LoginForm
from connectify.models import User, Post

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.first_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@example.com' and form.password.data == 'password':
            flash(f'Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsucessful! Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
