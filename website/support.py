from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Contact
from . import db
from .forms import ContactForm, BuyerContactForm

support = Blueprint('support', __name__)

@support.route('/buyersupport', methods=['GET', 'POST'])
@login_required
def buyersup():
    form = BuyerContactForm()
    if form.validate_on_submit():
        pass
    return render_template("support/buyersup.html", user=current_user, form=form)

@support.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_message = Contact(email=form.email.data, subject=form.subject.data, text=form.text.data)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sended successfully', category='success')  
        return redirect(url_for('views.home'))
    return render_template("support/contact.html", user=current_user, form=form)