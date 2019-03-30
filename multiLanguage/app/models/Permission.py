from app.exts import db
from datetime import datetime

# 权限
class Permission(db.Model):
  __tablename__ = 'm_permission'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255),nullable = True)
  parent_id=db.Column(db.Integer,nullable = True)
  endpoint=db.Column(db.String(255),nullable = True)
  # manager = db.relationship('Manager',backref='m_permission',uselist=False)
  # manager_id  = db.Column(db.Integer,db.ForeignKey('m_manager.id'))