from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    pgp_key = TextAreaField('PGP-Key', validators=[DataRequired()])
    submit = SubmitField('Update')

class AdminNewProduct(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    picture = FileField('Product Picture', validators=[FileRequired() ,FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

class MakeNewReview(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=20)])
    text = TextAreaField('Review', validators=[DataRequired(), Length(min=3, max=250)])
    submit = SubmitField('Save')

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    text = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class BuyerContactForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    text = TextAreaField('Message', validators=[DataRequired()])
    picture = FileField('Picture/Screenshot', validators=[FileRequired() ,FileAllowed(['jpg', 'png'])])
    picture = FileField('Picture/Screenshot', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Send')

class SimpleButton(FlaskForm):
    submit = SubmitField('New Random Users')
