from .. import admin
from app.models.Project import Project
from app.models.Language import Language
from app.models.Manager import Manager
from app.models.Entry import Entry
from flask import request, jsonify, session
from sqlalchemy import or_, desc
from app.exts import db
from . import decorator 
import uuid
import json


class ProjectClass():
    def __init__(self):
        pass

    def createSecretId(self):
        return str(uuid.uuid1())

    def getProjects(self, name, pageIndex, pageSize, manager_id):
        project_set = Project.query.join(Project.m_manager).filter(Project.name.contains(
            name),Manager.id==manager_id )
        total = project_set.count()
        projectSet = project_set.order_by(desc(Project.createtime)).slice((pageIndex-1)*pageSize, pageIndex*pageSize)
        projectList = []
        for p in projectSet:
            # print(p.language)
            lang_list = []
            for l in p.language:
              entryPendingAmount = Entry.query.filter(Entry.language_id==l.id,Entry.result=='').count()
              lang_list.append({'name':l.name,"id":l.id,'entryPendingAmount':entryPendingAmount})

            projectList.append({
                'id':p.id,
                'name': p.name,
                'description': p.description,
                'language': lang_list,
                'secretId': p.secretId,
                'entryPendingAmount': p.entryPendingAmount,
                'createtime': p.createtime
            })
        return jsonify({"code": 200, 'projectList': projectList, "total": total})

    def createProject(self, option):
        msg = []
        lang_list = []
        manager = Manager.query.filter(Manager.id==option['manager_id']).first()
        for l in option['language']:
          temL = Language.query.filter(Language.id == l).first()
          if temL != None:
           lang_list.append(temL)
          else:
            msg.append('id为'+str(l)+'的语言不存在')

        tempProject = {}
        tempProject['name']= option['name']
        tempProject['description'] = option['description']
        tempProject['m_manager'] = [manager]
        tempProject['language'] = lang_list
        tempProject['entryPendingAmount'] = 0
        tempProject['secretId'] = self.createSecretId()
        project = Project(**tempProject)
        db.session.add(project)
        db.session.commit()
        return jsonify({"code":200,"msg":'.'.join(msg)})

    def editProject(self, option):
      temp = Project.query.filter(Project.id==option['id']).first()
      for o in option:
          if o=='id' or o=='manager_id':
              pass
          else:
              setattr(temp,o, option[o])
      db.session.commit()
      return jsonify({"code":200})

    def deleteProject(self, option):
        project_list = Project.query.filter(Project.id.in_(option['ids'])).all()
        for p in project_list:
            Entry.query.filter(Entry.project_id==p.id).delete(synchronize_session=False)
            db.session.delete(p)
            db.session.commit()
        return jsonify({"code":200})

projectInstance = ProjectClass()


@admin.route('/project/getProjects', methods=['POST'])
def getProjects():
    postData = json.loads(request.get_data().decode('utf-8'))
    result = projectInstance.getProjects(postData['name'], int(
        postData['pageIndex']), int(postData['pageSize']),postData['manager_id'])
    return result

@admin.route('/project/createProject', methods=['POST'])
def createProject():
    postData = json.loads(request.get_data().decode('utf-8'))
    result = projectInstance.createProject(postData)
    return result

@admin.route('/project/editProject', methods=['POST'])
def editProject():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    postData['id'] = int(postData['id'])
    result = projectInstance.editProject((postData))
    return result

@admin.route('/project/deleteProject', methods=['POST'])
def deleteProject():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # postData['id'] = int(postData['id'])
    result = projectInstance.deleteProject((postData))
    return result
