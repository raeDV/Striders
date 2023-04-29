import os
import sqlite3

import bcrypt
from flask import Flask, session, redirect, render_template, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from forms import LoginForm, RegisterForm, AddProductForm, AddToCartForm

app = Flask(__name__)
app.secret_key = 'striders'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///striders.sqlite'
db = SQLAlchemy(app)

from models import DBUser, Filters, Cart, Product


def get_filters(gender):
    filters = Filters
    filters.filter_sizes = [5, 6, 7, 8]
    filters.filter_colors = ['Black', 'White']
    filters.filter_brands = ['brand A', 'brand B']
    filters.filter_categories = ['shoes', 'boots']
    filters.sorters = ['Best Sellers', 'Newest', 'Price High to Low', 'Price Low to High', 'Brand A-Z']
    return filters


class User(UserMixin):
    def __init__(self, username, email, phone, password=None):
        self.id = username
        self.email = email
        self.phone = phone
        self.password = password


# this is used by flask_login to get a user object for the current user
@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    # user could be None
    if user:
        # if not None, hide the password by setting it to None
        user.password = None
    return user


def find_user(username):
    res = DBUser.query.filter_by(username=username).first()
    if res:
        user = User(res.username, res.email, res.phone, res.password)
    else:
        user = None
    return user


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('home.html', products=products, username=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.username.data)
        # user could be None
        # passwords are kept in hashed form, using the bcrypt algorithm
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user)
            flash('Logged in successfully.')

            # check if the next page is set in the session by the @login_required decorator
            # if not set, it will default to '/'
            next_page = session.get('next', '/')
            # reset the next page to default '/'
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password!')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash(str(session))
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # check first if user already exists
        user = find_user(form.username.data)
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            user = DBUser(username=form.username.data, email=form.email.data, phone=form.phone.data,
                          password=password.decode())
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully.')
            return redirect('/login')
        else:
            flash('This username already exists, choose another one')
    return render_template('register.html', form=form)


@app.route('/men')
def men():
    products = Product.query.all()
    return render_template('men.html', products=products, filters=get_filters('men'))


@app.route('/women')
def women():
    products = Product.query.all()
    return render_template('women.html', products=products, filters=get_filters('women'))


@app.route('/kids')
def kids():
    print(Filters.filter_sizes)
    products = Product.query.all()
    return render_template('kids.html', products=products, filters=get_filters('kids'))


@app.route('/<int:pro_id>', methods=["GET"])
def getproduct(pro_id):
    form = AddToCartForm()
    item = Product.query.get(pro_id)
    return render_template('product.html', item=item, form=form)


@app.route('/add_to_cart/<int:pro_id>', methods=["POST", "GET"])
def add_to_cart(pro_id):
    form = AddToCartForm()
    if current_user.is_authenticated:
        user_id = current_user.id
        cart_item = Cart.query.filter_by(pro_id=pro_id, user_id=user_id).first()
        if cart_item:
            num = form.quantity.data
            cart_item.quantity += num
            cart_item.save_to_db()
        else:
            num = form.quantity.data
            cart = Cart(pro_id=pro_id, user_id=user_id, quantity=num)
            cart.save_to_db()
    else:
        flash('You need to log in to add items to your cart', category='danger')
        return redirect('/login')
    return redirect(url_for('cart'))


@app.route("/cart")
@login_required
def cart():
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    products = []
    final_total = 0
    for item in cart_items:
        product = Product.query.get(item.pro_id)
        product.quantity = item.quantity
        final_total += product.pro_price * product.quantity
        products.append(product)
    return render_template('cart.html', cart=products, final_total=final_total)


@app.route('/cart/<int:pro_id>/remove', methods=["POST", "GET"])
def remove_from_cart(pro_id):
    user_id = current_user.id
    cart_item = Cart.query.filter_by(pro_id=pro_id, user_id=user_id).first()

    if not cart_item:
        return redirect(url_for('cart'))

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save_to_db()
    else:
        cart_item.delete_from_db()

    return redirect(url_for('cart'))


@app.route('/cart/clear', methods=["POST", "GET"])
def clear_cart():
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    for cart_item in cart_items:
        cart_item.delete_from_db()

    return redirect(url_for('cart'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = RegisterForm(obj=current_user)
    user = find_user(form.username.data)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.phone = form.phone.data
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            if form.password.data:
                password_hash = bcrypt.hashpw(form.confirmPassword.data.encode(), bcrypt.gensalt())
                user.password = password_hash.decode()
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('home.html'))
    return render_template('account.html', form=form)


@app.route('/productdetail')
def product():
    return render_template('product.html')


@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        item = Product(
            pro_img_url=form.img_url.data,
            pro_brand=form.brand.data,
            pro_category=form.category.data,
            pro_size_range=form.size_range.data,
            pro_size_type=form.size_type.data,
            pro_colors=form.colors.data,
            pro_price=form.price.data,
            pro_desc=form.description.data,
            pro_model=form.model.data,
            pro_type=form.type.data
        )

        # add the new product to the database
        db.session.add(item)
        db.session.commit()

        flash('Product added successfully.')
        return redirect('/add-product')

    return render_template('add_product.html', form=form)


if __name__ == '__main__':
    app.run()
