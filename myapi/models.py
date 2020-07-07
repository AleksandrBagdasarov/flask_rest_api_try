from datetime import datetime
import re

from myapi import db, ma


########## FUNCTION RETURN STRING FOR URL ##########
def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


########## PRODUCT  MODELS ##########

# Product model
class Product(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    name =          db.Column(db.String(32, collation='NOCASE'))
    slug =          db.Column(db.String(140, collation='NOCASE'), unique=True)
    description =   db.Column(db.Text)
    created =       db.Column(db.DateTime, default=datetime.utcnow())
    price =         db.Column(db.Float)
    img =           db.relationship('Productimg', secondary='product_imgs', backref=db.backref('products', lazy='dynamic'))
    tags =          db.relationship('Tag', secondary='product_tags', backref=db.backref('products', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)
    
    def __repr__(self):
        return f"Product('Name: {self.name}','Date Created: {self.created}','Description: {self.description}')"

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'slug', 'description', 'created', 'price', 'img', 'tags')

# Product images
class Productimg(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    img =           db.Column(db.String(20), nullable=False, default='default_product.jpg')

# Product Img Schema
class ProductImgSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_id', 'img')


# Many to Many (Product - img)
product_imgs = db.Table('product_imgs',
                            db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                            db.Column('img_id', db.Integer, db.ForeignKey('productimg.id'))
                            )


# Many to Many (Product - Tag )
product_tags = db.Table('product_tags',
                            db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                            db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                            )

########## TAG MODELS ##########

# Tag model
class Tag(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    name =          db.Column(db.String(32, collation='NOCASE'))
    slug =          db.Column(db.String(140, collation='NOCASE'), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f"Tag('{self.id}','{self.name}')"

# Tag Schema
class TagSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'slug')


########## USER MODELS ##########

# User model
class User(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    admin =         db.Column(db.Boolean, default=False)
    mail =          db.Column(db.String(128), unique=True, nullable=False)
    password =      db.Column(db.String(128), nullable=False)
    created =       db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    img =           db.relationship('Userimg', secondary='user_imgs', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"User('ID: {self.id}', 'Is Admin: {self.admin}', 'Mail: {self.mail}', 'Date Created: {self.created}')"

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'admin', 'mail', 'password', 'created', 'img')

# User Images
class Userimg(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    img =           db.Column(db.String(20), nullable=False, default='default_user.jpg')

    def __repr__(self):
        return f"User('ID: {self.id}', 'IMG: {self.img}')"

# User img Schema
class UserImgSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'img')


# Many to Many ( User - Img )
user_imgs = db.Table('user_imgs',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('userimg_id', db.Integer, db.ForeignKey('userimg.id'))
                            )