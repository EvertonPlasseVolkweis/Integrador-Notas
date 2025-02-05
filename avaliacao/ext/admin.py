from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla
from flask_simplelogin import login_required
from werkzeug.security import generate_password_hash

from avaliacao.ext.database import db
from avaliacao.models import Usuario

# Proteger o admin com login via Monkey 
#######################################
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)
admin = Admin()
has_been_run = False

class UserAdmin(sqla.ModelView):
    column_list = ['username']
    can_edit = False

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)


def init_app(app):
    global has_been_run
    if not has_been_run:
        admin.name = app.config.TITLE
        admin.template_mode = "bootstrap3"
        admin.init_app(app)
        admin.add_view(UserAdmin(Usuario, db.session))
        has_been_run = True