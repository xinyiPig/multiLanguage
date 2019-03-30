from .. import admin
from flask import request, jsonify, session
from sqlalchemy import or_, desc
from app.exts import db
from app.models.Entry import Entry
from app.models.Project import Project
from . import decorator 

import json


class EntryClass():
    def __init__(self):
        pass

    def getEntry(self, option):
        # type 就是查询词条的方式，0 是把id,描述，结果都查一下
        condition =( Entry.project_id.contains(option['project_id']),
                    Entry.language_id.contains(option['language_id']))
        
        # if option['type'] == '0':
        #     condition =(
        #         Entry.project_id.contains(option['project_id']),
        #         Entry.language_id.contains(option['language_id']),
        #         or_(Entry.name.contains(option['name']),
        #         Entry.result.contains(option['name']),
        #         Entry.description.contains(option['name']))
        #         )
        #1 -ID
        if option['type']=="1":
            condition = condition+(Entry.name.contains(option['name']),)
        #2-描述
        if option['type'] == "2":
            condition = condition+(
                Entry.description.contains(option['name']),)
        #3-result
        if option['type'] == "3":
            condition = condition+(
                Entry.result.contains(option['name']),)
          # 0 就是全部 1 是已翻译
        if option['resultType'] == '1':
            condition = condition+(Entry.result!='',)
        # 2 待翻译
        if option['resultType'] == '2':
            condition =condition+ (Entry.result=='',)
            
        if option['startTime'] !="":
            condition = condition+(Entry.createtime > option['startTime'])
        f_set=Entry.query.filter(*condition)
        total = f_set.count()
        pageIndex = option['pageIndex']
        pageSize = option['pageSize']
        entrySet = f_set.order_by(desc(Entry.createtime)).slice(
            (pageIndex-1)*pageSize, pageIndex*pageSize)
        entryList = []
        for l in entrySet:
            entryList.append({
                'id':l.id,
                'name': l.name,
                'description': l.description,
                'result': l.result,
                'language':l.m_language.name,
                'language_id':l.m_language.id,
                'createtime': l.createtime
            })
        return jsonify({"code": 200, 'entryList': entryList, "total": total})

    def createEntry(self, option):
        # tempL = {}
        # for o in option:
        #    tempL[o]=option[o]
        # print(Entry)
        project = Project.query.filter(
            Project.id == option['project_id']).first()
        del option['manager_id']
        for l in project.language:
            option['language_id'] = l.id
            entry = Entry(**option)
            db.session.add(entry)
            db.session.commit()
        # 项目中待翻译词条数，新建的时候就开始计数
        project.entryPendingAmount = int(
            project.entryPendingAmount)+len(project.language)
        db.session.commit()
        return jsonify({"code": 200})

    def editEntry(self, option):
        # tempL = {}
        # for o in option:
        #    tempL[o]=option[o]
        # print(Entry)
        temp = Entry.query.filter(Entry.id == option['id']).first()
        print(temp.result)
        oldResult = temp.result
    
        for o in option:
            if o == 'id' or o == 'manager_id':
                pass
            else:
                setattr(temp, o, option[o])

        project = Project.query.filter(Project.id==temp.m_project.id).first()
        #如果原来没翻译结果，编辑以后有了，
        if oldResult=='' and temp.result!='':
            project.entryPendingAmount = int(project.entryPendingAmount)-1
        if oldResult!="" and temp.result=="":
            project.entryPendingAmount = int(project.entryPendingAmount)+1
        db.session.commit()
        return jsonify({"code": 200})
    
    def deleteEntry(self,option):
        print(option['ids'])
        entryList = Entry.query.filter(Entry.id.in_(option['ids'])).all()
        project = None
        print(entryList)
        for e in entryList:
            oldResult = e.result
            if project ==None:
                #这些词条的同属一个项目，查一次就行
                project = Project.query.filter(Project.id==e.m_project.id).first()
            #如果原来没翻译结果，
            if oldResult=='':
                project.entryPendingAmount = int(project.entryPendingAmount)-1
            db.session.delete(e)
            db.session.commit()
        return jsonify({"code": 200})


entryInstance = EntryClass()


@admin.route('/entry/getEntry', methods=['POST'])
@decorator.login_required
def getEntry():
    postData = json.loads(request.get_data().decode('utf-8'))
    result = entryInstance.getEntry(postData)
    return result


@admin.route('/entry/createEntry', methods=['POST'])
@decorator.login_required

def createEntry():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # postData['language_id'] = int(postData['language_id'])
    postData['project_id'] = int(postData['project_id'])
    result = entryInstance.createEntry((postData))
    return result


@admin.route('/entry/editEntry', methods=['POST'])
@decorator.login_required

def editEntry():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    postData['id'] = int(postData['id'])
    result = entryInstance.editEntry((postData))
    return result

@admin.route('/entry/deleteEntry', methods=['POST'])
@decorator.login_required
def deleteEntry():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    postData['ids'] = (postData['ids'])
    result = entryInstance.deleteEntry((postData))
    return result
