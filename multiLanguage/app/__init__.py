from flask import Flask,session
from flask_wtf.csrf import CSRFProtect,generate_csrf,CSRFError

from app.exts import db
# 数据库迁移
from flask_migrate import Migrate
from app.models import Entry,Language,Project,Manager
import app.config as config
app = Flask(__name__)
app.config.from_object(config)
# 数据库初始化
migrate = Migrate(app, db)
db.init_app(app)
# with app.app_context():
#     # pass
#     db.create_all()
# 利用Flask-Migrate 来更新orm的改动到数据表
# 终端依次输入 export FLASK_APP=main.py   flask db init    flask db migrate   flask db upgrade
# session['manager_id']=1
# csrfToken保护
csrf = CSRFProtect(app)
# csfr 检验
@app.errorhandler(CSRFError)
def csrf_error(reason):
    return jsonify({'code':"601","msg":"请先登录"})

from app.interface.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")