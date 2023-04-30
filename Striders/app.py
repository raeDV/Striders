import os

import bcrypt
from flask import Flask, session, redirect, render_template, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from models import DBUser, Filters, Cart, Product, db
from forms import LoginForm, RegisterForm, AddProductForm, AddToCartForm

app = Flask(__name__)
app.secret_key = 'striders'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///striders.sqlite'
db.init_app(app)


def get_filters(gender):
    filters = Filters
    # size
    size_grp = Product.query.group_by(Product.pro_size_range).filter(Product.pro_size_type == gender)
    filters.filter_sizes = []
    for size_entry in size_grp:
        size_entry = size_entry.pro_size_range.split(' - ')
        for size in size_entry:
            size.strip()
            size = float(size)
            if size not in filters.filter_sizes:
                filters.filter_sizes.append(size)
    size_list_builder = []
    for s in range(int(min(filters.filter_sizes)*2), int(max(filters.filter_sizes)*2)+1):
        size_list_builder.append(s/2)
    filters.filter_sizes = sorted(size_list_builder)
    # color
    filters.filter_colors = []
    color_grp = Product.query.group_by(Product.pro_colors).filter(Product.pro_size_type == gender)
    for color_entry in color_grp:
        color_entry = color_entry.pro_colors.split(',')
        for color in color_entry:
            color = color.rstrip()
            color = color.lstrip()
            if color not in filters.filter_colors:
                filters.filter_colors.append(color)
    filters.filter_colors = sorted(filters.filter_colors)
    # brand
    filters.filter_brands = []
    brand_grp = Product.query.group_by(Product.pro_brand).filter(Product.pro_size_type == gender)
    for brand in brand_grp:
        brand = brand.pro_brand
        brand = brand.rstrip()
        brand = brand.lstrip()
        brand = brand.lower()
        brand = brand.title()
        if brand not in filters.filter_brands:
            filters.filter_brands.append(brand)
    # category
    filters.filter_categories = []
    cat_grp = Product.query.group_by(Product.pro_category).filter(Product.pro_size_type == gender)
    for cat in cat_grp:
        cat = cat.pro_category
        cat = cat.rstrip()
        cat = cat.lstrip()
        cat = cat.lower()
        cat = cat.title()
        if cat not in filters.filter_categories:
            filters.filter_categories.append(cat)
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
            # flash('Logged in successfully.')

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
    return render_template('men.html', products=products, filters=get_filters('US Men'))


@app.route('/women')
def women():
    products = Product.query.all()
    return render_template('women.html', products=products, filters=get_filters('US Women'))


@app.route('/kids')
def kids():
    print(Filters.filter_sizes)
    products = Product.query.all()
    return render_template('kids.html', products=products, filters=get_filters('US Kids'))


@app.route('/<int:pro_id>', methods=["GET"])
def getproduct(pro_id):
    form = AddToCartForm()
    item = Product.query.get(pro_id)
    sizes_range = item.pro_size_range.split(' - ')
    sizes = []
    sizes_range[0] = float(sizes_range[0])
    sizes_range[1] = float(sizes_range[1])
    for s in range(int(sizes_range[0]*2), int(sizes_range[1]*2)+1):
        sizes.append(s/2)
    return render_template('product.html', item=item, form=form, sizes=sizes)


@app.route('/add_to_cart/<int:pro_id>', methods=["POST", "GET"])
def add_to_cart(pro_id):
    form = AddToCartForm()
    if current_user.is_authenticated:
        user_id = current_user.id
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        cart_item = None
        for item in cart_items:
            if item.pro_id == pro_id:
                if item.color == form.color.data and item.size == form.size.data:
                    cart_item = item
                    break
                elif item.color is None and item.size is None:
                    item.color = form.color.data
                    item.size = form.size.data
                    item.save_to_db()
                    cart_item = item
                    break
        if cart_item:
            num = form.quantity.data
            cart_item.quantity += num
            cart_item.save_to_db()
        else:
            num = form.quantity.data
            cart = Cart(pro_id=pro_id, user_id=user_id, quantity=num, color=form.color.data, size=form.size.data)
            cart.save_to_db()
    else:
        flash('You need to log in to add items to your cart', category='danger')
        return redirect('/login')

    # Store the form data in Flask's session
    session['form'] = form.data

    return redirect(url_for('cart'))


@app.route("/cart")
@login_required
def cart():
    user_id = current_user.id
    products = []
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    final_total = 0
    for item in cart_items:
        product = Product.query.get(item.pro_id)
        print(item.color)
        colors_list = product.pro_colors.split(', ')
        color_index = colors_list.index(item.color)
        image_url = product.pro_img_url.split(', ')[color_index]
        print(image_url)
        new_product = Product(pro_img_url=product.pro_img_url, pro_brand=product.pro_brand,
                              pro_category=product.pro_category, pro_model=product.pro_model, pro_type=product.pro_type,
                              pro_size_range=product.pro_size_range, pro_size_type=product.pro_size_type,
                              pro_colors=product.pro_colors, pro_price=product.pro_price, pro_desc=product.pro_desc)
        new_product.id = item.id
        new_product.size = item.size
        new_product.image_url = image_url
        new_product.color = item.color
        new_product.quantity = item.quantity
        new_product.pro_id = item.pro_id
        final_total += new_product.pro_price * new_product.quantity
        products.append(new_product)
    return render_template('cart.html', cart=products, final_total=final_total)


@app.route('/cart/<int:item_id>/remove', methods=["POST", "GET"])
def remove_from_cart(item_id):
    cart_item = Cart.query.get(item_id)
    if not cart_item:
        return redirect(url_for('cart'))
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


@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        if form.pro_img_url.data:
            filename = secure_filename(form.pro_img_url.data.filename)
            form.pro_img_url.data.save(os.path.join(app.root_path, 'static/img', filename))
            img_url = filename
        else:
            img_url = None
        new_product = Product(
            pro_img_url=img_url,
            pro_brand=form.pro_brand.data,
            pro_category=form.pro_category.data,
            pro_size_range=form.pro_size_range.data,
            pro_size_type=form.pro_size_type.data,
            pro_colors=form.pro_colors.data,
            pro_price=form.pro_price.data,
            pro_desc=form.pro_desc.data,
            pro_model=form.pro_model.data,
            pro_type=form.pro_type.data
        )

        # add the new product to the database
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully.')
        return redirect('/add-product')

    return render_template('add_product.html', form=form)


if __name__ == '__main__':
    app.run()
