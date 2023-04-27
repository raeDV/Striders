from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField
from wtforms.fields import EmailField
from wtforms.validators import InputRequired, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired(),
                                       Length(4, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must start with a letter and must have only letters, '
                                              'numbers, dots or underscores')])
    email = EmailField('Email', validators=[InputRequired()])
    phone = StringField('Phone number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(8)])
    confirmPassword = PasswordField('Confirm Password',
                                    validators=[InputRequired(),
                                                EqualTo('password',
                                                        message='Passwords must match.')])
    submit = SubmitField('Register')


class AddProductForm(FlaskForm):
    brand = StringField('Brand', validators=[InputRequired()])
    model = StringField('Model', validators=[InputRequired()])
    category = SelectField('Category', choices=[
        ('Boots', 'Boots'),
        ('Sandals', 'Sandals')
    ], validators=[InputRequired()])
    size_range = StringField('Model', validators=[InputRequired()])
    size_type = SelectField('Type', choices=[
        ('US Men', 'US Men'),
        ('US Women', 'US Women'),
        ('US Kids', 'US Kids')
    ], validators=[InputRequired()])
    colors = SelectField('Color', choices=[
        ('Blue', 'Blue'),
        ('Red', 'Red'),
        ('White', 'White')
    ], validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])