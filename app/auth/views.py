from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm
from ..const import ADMIN_USERNAME


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = ""
    user = User.query.filter_by(mobile=form.mobile.data).first()
    if user is not None and user.verify_password(form.password.data):
        login_user(user, form.remember_me.data)
        if user.username == ADMIN_USERNAME:
            return redirect(request.args.get('next') or 'admin')
        return redirect(request.args.get('next') or url_for('main.index'))
    if not user:
        msg = "check your username"
    else:
        msg = "check your password"
    flash(msg)
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('成功退出')
    return redirect(url_for('main.index'))


