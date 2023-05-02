from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField, IntegerField, MultipleFileField
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
    pro_img_url = MultipleFileField('Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG, JPG, and PNG images are allowed!')
    ])
    pro_brand = StringField('Brand', validators=[InputRequired()])
    pro_category = StringField('Category', validators=[InputRequired()])
    pro_size_range = StringField('Size Range', validators=[InputRequired()])
    pro_size_type = SelectField('Size Type', choices=[
        ('US Men', 'US Men'),
        ('US Women', 'US Women'),
        ('US Kids', 'US Kids')
    ], validators=[DataRequired()])
    pro_colors = StringField('Color', validators=[InputRequired()])
    pro_price = FloatField('Price', validators=[InputRequired()])
    pro_desc = TextAreaField('Description', validators=[InputRequired(), Length(max=10000)])
    pro_model = StringField('Model', validators=[InputRequired()])
    pro_type = SelectField('Type', choices=[
        ('New', 'New'),
        ('General', 'General'),
        ('Sale', 'Sale')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Product')


class AddToCartForm(FlaskForm):
    size = SelectField('Select Size', validators=[DataRequired()], default=0)
    color = SelectField('Select Color', validators=[DataRequired()], default=0)
    quantity = IntegerField('Enter Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Add to Cart')


class FilterForm(FlaskForm):
    brand = SelectField('Select Brand', validators=[DataRequired()], default='')
    color = SelectField('Select Color', validators=[DataRequired()], default='')
    category = SelectField('Select Category', validators=[DataRequired()], default='')
    sort = SelectField('Sort By', validators=[DataRequired()], default='Best Sellers')
