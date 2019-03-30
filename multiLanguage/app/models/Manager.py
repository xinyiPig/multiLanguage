from app.exts import db
from datetime import datetime
class Manager(db.Model):
  __tablename__ = 'm_manager'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  account = db.Column(db.String(255),nullable = True)
  name = db.Column(db.String(255),nullable = True)
  description = db.Column(db.String(255),nullable = True)
  password = db.Column(db.String(255),nullable = True)
  createtime = db.Column(db.DateTime, default=datetime.now)
  parent_id = db.Column(db.Integer,nullable=True)
  # permission = db.relationship('permission',backref='m_manager')
  project = db.relationship('Project',secondary='manager_project',backref='m_manager')
  permission = db.relationship('Permission',secondary='manager_permission',backref='m_manager')
  language = db.relationship('Language',secondary='manager_language',backref=db.backref('m_manager',lazy='dynamic'))


manager_project = db.Table(
    'manager_project',
    # 第一个参数为表名称，第二个参数是 metadata，这俩个是必须的
    # 'project_language', db.Model.Base.metadata,
    # 对于辅助表，一般存储要关联的俩个表的 id，并设置为外键
    db.Column('project_id', db.Integer, db.ForeignKey('m_project.id')),
    db.Column('manager_id',db.Integer, db.ForeignKey('m_manager.id')),
)
manager_language = db.Table(
    'manager_language',
    # 第一个参数为表名称，第二个参数是 metadata，这俩个是必须的
    # 'project_language', db.Model.Base.metadata,
    # 对于辅助表，一般存储要关联的俩个表的 id，并设置为外键
    db.Column('language_id', db.Integer, db.ForeignKey('m_language.id')),
    db.Column('manager_id',db.Integer, db.ForeignKey('m_manager.id')),
)
manager_permission = db.Table(
    'manager_permission',
    # 第一个参数为表名称，第二个参数是 metadata，这俩个是必须的
    # 'project_language', db.Model.Base.metadata,
    # 对于辅助表，一般存储要关联的俩个表的 id，并设置为外键
    db.Column('permission_id', db.Integer, db.ForeignKey('m_permission.id')),
    db.Column('manager_id',db.Integer, db.ForeignKey('m_manager.id')),
)
