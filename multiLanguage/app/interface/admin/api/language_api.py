from .. import admin
from flask import request, jsonify, session
from sqlalchemy import or_,desc
from app.exts import db
from app.models.Language import  Language
from app.models.Entry import  Entry
from app.models.Manager import  Manager
from app.models.Project import  Project
from . import decorator 

import json


class LanguageClass():
    def __init__(self):
        pass

    def getLanguage(self, name, pageIndex, pageSize,manager_id):
       
        lang_set = Language.query.join(Language.m_manager).filter(Language.name.contains(name),Manager.id==manager_id)
        total = lang_set.count()
        languageSet = lang_set.order_by(desc(Language.createtime)).slice((pageIndex-1)*pageSize, pageIndex*pageSize)
        languageList = []
        for l in languageSet:
            languageList.append({
                'id':l.id,
                'name': l.name,
                'description': l.description,
                'shortName': l.shortName,
                'createtime':l.createtime
            })
        return jsonify({"code": 200, 'languageList': languageList,"total":total})

    def createLanguage(self, option):
        # tempL = {}
        # for o in option:
        #    tempL[o]=option[o]
        # print(Language)
        manager = Manager.query.filter(Manager.id==option['manager_id']).first()
        tempL = {
            "name":option['name'],
            "shortName":option['shortName'],
            "description":option['description'],
            "m_manager":[manager]
        }
        language = Language(**tempL)
        db.session.add(language)
        db.session.commit()
        return jsonify({"code":200})

    def editLanguage(self, option):
        # tempL = {}
        # for o in option:
        #    tempL[o]=option[o]
        # print(Language)
        temp = Language.query.filter(Language.id==option['id']).first()
        for o in option:
            if o=='id':
                pass
            else:
                setattr(temp,o, option[o])
        db.session.commit()
        return jsonify({"code":200})

    def deleteLanguage(self, option):
        lang_list = Language.query.filter(Language.id.in_(option['ids'])).all()
        for l in lang_list:
            entryList = Entry.query.filter(Entry.language_id==l.id).all()
            for e in entryList:
                if e.result=='':
                    project = Project.query.filter(Project.id==e.project_id).first()
                    project.entryPendingAmount = int(project.entryPendingAmount)-1
                else:
                    db.session.delete(e)
            db.session.delete(l)
            db.session.commit()
        return jsonify({"code":200})


languageInstance =LanguageClass()


@admin.route('/language/getLanguage', methods=['POST'])
@decorator.login_required

def getLanguage():
    postData = json.loads(request.get_data().decode('utf-8'))
    result = languageInstance.getLanguage(postData['name'], int(
        postData['pageIndex']), int(postData['pageSize']),postData['manager_id'])
    return result

@admin.route('/language/createLanguage', methods=['POST'])
@decorator.login_required

def createLanguage():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    result = languageInstance.createLanguage((postData))
    return result

@admin.route('/language/editLanguage', methods=['POST'])
@decorator.login_required

def editLanguage():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    postData['id'] = int(postData['id'])
    result = languageInstance.editLanguage((postData))
    return result

@admin.route('/language/deleteLanguage', methods=['POST'])
@decorator.login_required

def deleteLanguage():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # postData['ids'] = int(postData['ids'])
    result = languageInstance.deleteLanguage((postData))
    return result
