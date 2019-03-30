from app.exts import db
from datetime import datetime

# 语言
class Language(db.Model):
  __tablename__ = 'm_language'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  description = db.Column(db.String(255),nullable = True)
  name = db.Column(db.String(255),nullable = True)
  shortName = db.Column(db.String(255),nullable = True)
  createtime = db.Column(db.DateTime, default=datetime.now)
  # manager_id  = db.Column(db.Integer,db.ForeignKey('m_manager.id'))
  entry = db.relationship('Entry',backref='m_language',uselist=False)