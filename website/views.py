from flask import Blueprint, render_template, request, flash,  url_for, redirect, abort
from flask_login import login_required, current_user
from .models import Products, Cart, UserRating, User
from . import db
from .forms import MakeNewReview
views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    products = Products.query.order_by(
        Products.name.desc()).paginate(page=page, per_page=9)
    return render_template("home.html", user=current_user, products=products)


@views.route("/product/<int:product_id>", methods=['GET', 'POST'])
@login_required
def product(product_id):
    form = MakeNewReview()
    products = Products.query.get_or_404(product_id)
    reviews = UserRating.query.filter_by(product=product_id).all()
    if form.validate_on_submit():
        new_review = UserRating(title=form.title.data, text=form.text.data,
                                user=current_user.username, product=product_id)
        db.session.add(new_review)
        db.session.commit()
        flash('Review created', category='success')
        return redirect(url_for('views.product', product_id=product_id))
    return render_template('product.html', user=current_user, products=products, reviews=reviews, form=form)


@views.route("/product/add/<int:product_id>")
@login_required
def addToCart(product_id):
    product = Products.query.filter_by(id=product_id).first()
    if product:
        new_cart = Cart(user=current_user.user_id, product=product_id)
        db.session.add(new_cart)
        db.session.commit()
        flash('Product added to Cart', category='success')
    else:
        abort(404, "Product {0} doesn't exist.".format(product_id))
    return redirect(url_for('views.home'))


@views.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    # test query
    products = Products.query.join(Cart).add_columns(Cart.id, Products.price, Products.name,
                                                     Products.id, Products.quantity, Cart.date).filter_by(user=current_user.user_id).all()
    subtotal = 0
    for product in products:
        subtotal += int(product.price)
    return render_template("cart.html", user=current_user, products=products, subtotal=subtotal)


@views.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user_profile = User.query.get_or_404(user_id)
    products = Products.query.filter_by(vendor_id=user_id).all()
    return render_template('profile.html', user=current_user, user_profile=user_profile, products=products)


@views.route('/profile/pgp_key/<int:user_id>', methods=['GET', 'POST'])
@login_required
def pgp_key(user_id):
    user_profile = User.query.get_or_404(user_id)
    return user_profile.pgp_key
