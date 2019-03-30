from app.exts import db
from datetime import datetime

# 词条
class Entry(db.Model):
  __tablename__ = 'm_entry'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255),nullable = True)
  description = db.Column(db.String(255),nullable = True)
  createtime = db.Column(db.DateTime, default=datetime.now)
  result = db.Column(db.String(255),nullable = True,default="")
  project_id  = db.Column(db.Integer,db.ForeignKey('m_project.id'))
  language_id  = db.Column(db.Integer,db.ForeignKey('m_language.id'))