from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DBUser(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.Text())
    email = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.Text())
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<DBUser {}: {} {} >".format(self.username, self.email, self.phone)


class Product(db.Model):
    __tablename__ = 'products'
    pro_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    pro_img_url = db.Column(db.Text())
    pro_brand = db.Column(db.Text(), nullable=False)
    pro_category = db.Column(db.Text(), nullable=False)
    pro_size_range = db.Column(db.Text(), nullable=False)
    pro_size_type = db.Column(db.Text(), nullable=False)
    pro_colors = db.Column(db.Text(), nullable=False)
    pro_price = db.Column(db.Float(), nullable=False)
    pro_desc = db.Column(db.Text(), nullable=False)
    pro_model = db.Column(db.Text(), nullable=False)
    pro_type = db.Column(db.Text(), nullable=False)

    def __init__(self, pro_img_url, pro_brand, pro_category, pro_size_range, pro_size_type, pro_colors,
                 pro_price, pro_desc, pro_model, pro_type):
        self.pro_img_url = pro_img_url
        self.pro_brand = pro_brand
        self.pro_category = pro_category
        self.pro_size_range = pro_size_range
        self.pro_size_type = pro_size_type
        self.pro_colors = pro_colors
        self.pro_price = pro_price
        self.pro_desc = pro_desc
        self.pro_model = pro_model
        self.pro_type = pro_type

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {"id": self.id,
                "pro_img_url": self.pro_img_url,
                "pro_brand": self.pro_brand,
                "pro_model": self.pro_model,
                "pro_category": self.pro_category,
                "pro_size_range": self.pro_size_range,
                "pro_size_type": self.pro_size_type,
                "pro_colors": self.pro_colors,
                "pro_price": self.pro_price,
                "pro_type": self.pro_type,
                "pro_desc": self.pro_desc}


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    pro_id = db.Column(db.Integer, db.ForeignKey('products.pro_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, user_id, pro_id, quantity=1):
        self.user_id = user_id
        self.pro_id = pro_id
        self.quantity = quantity

    def update_quantity(self, quantity):
        self.quantity += quantity
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Filters:
    filter_sizes = {}
    filter_colors = {}
    filter_brands = {}
    filter_categories = {}
    sorters = {}
