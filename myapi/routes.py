
from datetime import datetime
import jwt
from flask import jsonify, request
from functools import wraps

from myapi import app, bcrypt, db
from myapi.models import Product, Productimg, ProductSchema
from myapi.models import Tag, TagSchema
from myapi.models import User, Userimg, UserSchema

# custom decorator to login required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


########## PRODUCT ##########
# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a product
@app.route('/product', methods=['POST'])
@token_required
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  img = Productimg.query.get(1).img

  new_product = Product(name, description, price, img)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']

  product.name = name
  product.description = description
  product.price = price

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

########## TAG ##########
# Init schema
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

#Create Tag
@app.route('/tag', methods=['POST'])
def add_tag():
  name = request.json['name']

  new_tag = Tag(name)

  db.session.add(new_tag)
  db.session.commit()

  return tag_schema.jsonify(new_tag)

# Get all Tags
@app.route('/tag', methods=['GET'])
def get_all_tags():
  all_tags = Tag.query.all()
  result = tags_schema.dump(all_tags)
  return jsonify(result)

# Get Tag by id
@app.route('/tag/<id>', methods=['GET'])
def get_one_tag(id):
  tag = Tag.query.get(id)
  return tag_schema.jsonify(tag)

# Update a Tag
@app.route('/tag/<id>', methods=['PUT'])
def update_tag(id):
  tag = Tag.query.get(id)

  name = request.json['name']

  tag.name = name

  db.session.commit()

  return tag_schema.jsonify(tag)


# Delete Tag by id
@app.route('/tag/<id>', methods=['DELETE'])
def delete_tag(id):
  tag = Tag.query.get(id)
  db.session.delete(tag)
  db.session.commit()

  return tag_schema.jsonify(tag)

########## USERS ##########
# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a User
@app.route('/user', methods=['POST'])
def add_user():
  admin = request.json['admin']
  mail = request.json['mail']
  password = bcrypt.generate_password_hash(request.json['password']).decode('UTF-8')

  new_user = User(admin=admin, mail=mail, password=password)

  db.session.add(new_user)

  default_img = Userimg.query.get(1).users
  
  default_img.append(User.query.filter(User.mail==mail).first())

  #User.query.filter(User.mail==mail).first().img = Userimg.query.get(1).img
  db.session.commit()

  return user_schema.jsonify(new_user)


# Upload User Img
@app.route('/user/image', methods=['POST'])
def upload_user_img():
  return ''

# Get All Users
@app.route('/user', methods=['GET'])
def get_all_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)

  return jsonify(result)

# Get User by id
@app.route('/user/<id>', methods=['GET'])
def get_one_user(id):
  one_user = User.query.get(id)

  return users_schema.jsonify(one_user)


# Update a User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
  user = User.query.get(id)

  name = request.json['name']
  password = bcrypt.generate_password_hash(request.json['password']).decode('UTF-8')

  user.name = name
  user.password = password

  db.session.commit()

  return user_schema.jsonify(user)


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})