from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DBUser(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.Text(), primary_key=True)
    email = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.Text())
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<DBUser {}: {} {} >".format(self.username, self.email, self.phone)


class Products(db.Model):
    __tablename__ = 'products'
    brand = db.Column(db.Text(), primary_key=True)
    model = db.Column(db.Text(), nullable=False)
    category = db.Column(db.Text())
    size_range = db.Column(db.Text(), nullable=False)
    size_type = db.Column(db.Text())
    colors = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    def __repr__(self):
        return f"<Products {self.brand}: {self.model} {self.category} {self.size_range} {self.size_type} {self.colors} {self.price}>"


class Filters:
    filter_sizes = {}
    filter_colors = {}
    filter_brands = {}
    filter_categories = {}
    sorters = {}
