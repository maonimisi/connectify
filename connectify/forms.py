from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from connectify.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Exist')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    about_me = StringField('About Me', validators=[DataRequired(), Length(min=25, max=100)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class PitchForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    introduction = TextAreaField('Introduction', validators=[DataRequired()])
    problem_statement = TextAreaField('Problem Statement', validators=[DataRequired()])
    solution = TextAreaField('Solution', validators=[DataRequired()])
    unique_selling_proposition = TextAreaField('Unique Selling Proposition', validators=[DataRequired()])
    market_analysis = TextAreaField('Market Analysis', validators=[DataRequired()])
    target_audience = TextAreaField('Target Audience', validators=[DataRequired()])
    financial_projection = TextAreaField('Financial Analysis', validators=[DataRequired()])
    risk_assessment = TextAreaField('Risk Assessment', validators=[DataRequired()])
    conclusion = TextAreaField('Conclusion', validators=[DataRequired()])
    submit = SubmitField('Pitch your idea today')