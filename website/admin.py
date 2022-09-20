import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash
from .models import User, Products, Orders, Contact, Support, Roles
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import random
from . import db
from .forms import AdminNewProduct

admin = Blueprint('admin', __name__)


@admin.route("/", methods=["GET", "POST"])
@login_required
def admin_panel():
    if current_user.roles_id != 1:
        return redirect(url_for('views.home'))
    else:
        data = []
        user_count = data.append(User.query.count())
        product_count = data.append(Products.query.count())
        orders_count = data.append(Orders.query.count())
        contact_count = data.append(Contact.query.count())
        support_count = data.append(Support.query.count())
        return render_template("admin/adminpanel.html", user=current_user, data=data)


@admin.route("/new/product", methods=["GET", "POST"])
@login_required
def new_product():
    if current_user.roles_id != 1:
        return redirect(url_for('views.home'))
    else:
        form = AdminNewProduct()
        if form.validate_on_submit():
            f = form.picture.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(f.filename)
            picture_fn = random_hex + f_ext
            f.save(os.path.join(admin.root_path, 'static/pictures', picture_fn))
            product = Products(name=form.name.data, description=form.description.data,
                               price=form.price.data, quantity=form.quantity.data, image_file=picture_fn)
            db.session.add(product)
            db.session.commit()
            flash('You Product has been added!', 'success')
            return redirect(url_for('admin.admin_panel'))
        return render_template("admin/admin_new_product.html", user=current_user, form=form)


@admin.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.roles_id != 1:
        return redirect(url_for('views.home'))
    else:
        users = User.query.all()
        return render_template("admin/adminusers.html", user=current_user, users=users)


@admin.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    if current_user.roles_id != 1:
        return redirect(url_for('views.home'))
    else:
        products = Products.query.all()
        return render_template("admin/adminproducts.html", user=current_user, products=products)


@admin.route('/setup', methods=['GET', 'POST'])
def setup():
    text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
    roles = ["superadmin", "admin", "moderator", "supporter", "community", "vendor", "user"]

    # set the roles
    for role in roles:
        new_role = Roles(role=role)
        db.session.add(new_role)
        db.session.commit()

    # make admin
    new_admin = User(username="admin", password=generate_password_hash("admin", method='sha256'), roles_id=1)
    db.session.add(new_admin)
    db.session.commit()

    # make random products and user 
    for i in range(0,35):
        new_user = User(username="TestUser" + str(i),roles_id=7, description=text, password=generate_password_hash("test", method='sha256'))
        db.session.add(new_user)
        db.session.commit()
    print("User end")
    for i in range(0, 35):
        product = Products(name="Product " + str(i), description=text, price=200, quantity=50, image_file='default.png', vendor_id=random.randrange(1, 35))
        db.session.add(product)
        db.session.commit() 
    return "<p>all right</p>"