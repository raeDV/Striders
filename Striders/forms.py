from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField, IntegerField, \
    FileField
from wtforms.fields import EmailField
from wtforms.validators import InputRequired, EqualTo, Length, Regexp, DataRequired, NumberRange


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
    pro_img_url = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG, JPG, and PNG images are allowed!')
    ])
    brand = StringField('Brand', validators=[InputRequired()])
    category = SelectField('Category', choices=[
        ('Boots', 'Boots'),
        ('Sandals', 'Sandals')
    ], validators=[InputRequired()])
    size_range = StringField('Size Range', validators=[InputRequired()])
    size_type = SelectField('Size Type', choices=[
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
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=10000)])
    model = StringField('Model', validators=[InputRequired()])
    type = SelectField('Type', choices=[
        ('New', 'New'),
        ('General', 'General'),
        ('Sale', 'Sale')
    ], validators=[InputRequired()])
    submit = SubmitField('Add Product')


class AddToCartForm(FlaskForm):
    size = SelectField('Select Size', choices=[('7', '7'), ('8', '8'), ('9', '9'), ('11', '11')],
                       validators=[DataRequired()], default=0)
    color = SelectField('Select Color', validators=[DataRequired()], default=0)
    quantity = IntegerField('Enter Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Add to Cart')
