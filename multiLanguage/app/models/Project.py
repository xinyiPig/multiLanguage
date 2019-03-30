from app.exts import db
from datetime import datetime
from app.models import Entry
from sqlalchemy import Table
# 项目
class Project(db.Model):
  __tablename__ = 'm_project'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255),nullable = True)
  description = db.Column(db.String(255),nullable = True)
  secretId = db.Column(db.String(255),nullable=True,unique=True)
  createtime = db.Column(db.DateTime, default=datetime.now)
  # manager_id  = db.Column(db.Integer,db.ForeignKey('m_manager.id'))
  entry = db.relationship('Entry', backref='m_project',uselist=False)
  entryPendingAmount = db.Column(db.String(255),nullable=True)
  language = db.relationship('Language',secondary='project_language',backref='m_project')

project_language = db.Table(
    'project_language',
    # 第一个参数为表名称，第二个参数是 metadata，这俩个是必须的
    # 'project_language', db.Model.Base.metadata,
    # 对于辅助表，一般存储要关联的俩个表的 id，并设置为外键
    db.Column('project_id', db.Integer, db.ForeignKey('m_project.id')),
    db.Column('language_id',db.Integer, db.ForeignKey('m_language.id'))
)
