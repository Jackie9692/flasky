from flask_admin import expose, AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request, url_for, render_template

from flask_login import current_user
# from wtforms.fields import SelectField, StringField
# from wtforms.validators import DataRequired

from ..models import User, Loan_application
from ..const import ADMIN_USERNAME
from jinja2 import Markup
from .. import db, app


class ViewRequireLogin(ModelView):
    def is_accessible(self):
        return logged_in()

    def inaccessible_callback(self, name):
        return redirect('/admin')


class AdminLoginView(AdminIndexView):
    @expose('/')
    def index(self):
        if logged_in():
            return redirect('/admin/user/')
        return redirect(url_for("auth.login"))

    def is_visible(self):
        return not logged_in()


def logged_in():
    user = current_user._get_current_object()
    if user:
        if not hasattr(user, 'username'):
            return False
        return user.username == ADMIN_USERNAME
    else:
        return False


class UserView(ViewRequireLogin):
    can_view_details = True
    page_size = 10
    column_exclude_list = ['password_hash', 'address', 'loan_app']
    # column_list = ["id", 'address', 'loan_app']
    column_editable_list = ['withdraw_password']
    column_searchable_list = ['id', 'username', 'mobile']
    column_filters = ['username']
    column_display_pk = True
    column_display_all_relations = True


class LoanView(ViewRequireLogin):
    can_view_details = True
    page_size = 10
    # column_exclude_list = ['password_hash']
    column_editable_list = ['id', 'loan_amount', 'apply_status']
    column_searchable_list = ['id', 'mobile']
    # column_display_pk = True
    column_display_all_relations = True

    column_descriptions = dict(
        marriage_status="婚姻状况 0：未婚 1：已婚 2：离异",
        gender="性别 0：先生 1：女士",
        apply_status="审核状态 0：待审核 1：未通过 2：通过",
    )

    # form_overrides = dict(marriage_status=SelectField)
    # form_args = dict(
    #     marriage_status=dict(label='First Name', validators=[DataRequired()]))


    def show_image1(view, context, model, name):
        if not model.image1:
            return ''

        return Markup('<a href="%s" target="_blank"><img src="%s" width="100" height="100"/></a>' %
                      (url_for("static", filename="upload/" + str(model.image1)),
                       url_for("static", filename="upload/" + str(model.image1))))

    def show_image2(view, context, model, name):
        if not model.image2:
            return ''

        return Markup('<a href="%s" target="_blank"><img src="%s" width="100" height="100"/></a>' %
                      (url_for("static", filename="upload/" + str(model.image2)),
                       url_for("static", filename="upload/" + str(model.image2))))

    def show_image3(view, context, model, name):
        if not model.image1:
            return ''

        return Markup('<a href="%s" target="_blank"><img src="%s" width="100" height="100"/></a>' %
                      (url_for("static", filename="upload/" + str(model.image3)),
                       url_for("static", filename="upload/" + str(model.image3))))

    def show_image4(view, context, model, name):
        if not model.image1:
            return ''

        return Markup('<a href="%s" target="_blank"><img src="%s" width="100" height="100"/></a>' %
                      (url_for("static", filename="upload/" + str(model.image4)),
                       url_for("static", filename="upload/" + str(model.image4))))

    column_formatters = {
        'image1': show_image1,
        'image2': show_image2,
        'image3': show_image3,
        'image4': show_image4,
    }

# # Create administrative views
admin = Admin(
    app,
    name="Easy Loan",
    template_mode='bootstrap3',
    base_template='admin/admin_base.html',
    index_view=AdminLoginView(
        name='Admin',
    )
)

admin.add_view(UserView(User, db.session))
admin.add_view(LoanView(Loan_application, db.session))
