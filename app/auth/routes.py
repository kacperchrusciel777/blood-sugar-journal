from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import bp
from .forms import RegistrationForm, LoginForm
from ..models import User
from .. import db

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Rejestracja przebiegła pomyślnie. Możesz się teraz zalogować.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nieprawidłowy email lub hasło.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany.', 'info')
    return redirect(url_for('main.index'))
