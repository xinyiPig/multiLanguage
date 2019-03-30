from .. import admin
from flask import request, jsonify, session
from sqlalchemy import or_,desc
from app.exts import db
from app.models.Manager import  Manager
from app.models.Language import  Language
from app.models.Language import  Language
from app.models.Permission import  Permission
from app.models.Project import  Project
from app.util.crypto.crypto import CryptoUtil
from flask_wtf.csrf import generate_csrf
from app import csrf
from . import decorator 
import json


class ManagerClass():
    def __init__(self):
        pass

    def getManager(self, name, pageIndex, pageSize,manager_id):
        total = Manager.query.filter(Manager.name.contains(name),Manager.parent_id==manager_id).count()
        managerSet = Manager.query.filter(Manager.name.contains(name),Manager.parent_id==manager_id).order_by(
            desc(Manager.createtime)).slice((pageIndex-1)*pageSize, pageIndex*pageSize)
        managerList = []
        for l in managerSet:
            p_list = []
            for p in l.project:
                p_list.append({"id":p.id,"name":p.name})
            managerList.append({
                'id':l.id,
                'account':l.account,
                'name': l.name,
                'description': l.description,
                'createtime':l.createtime,
                'project':p_list
            })
        return jsonify({"code": 200, 'managerList': managerList,"total":total})

    def createManager(self, option):
        # tempL = {}
        # for o in option:
        #    tempL[o]=option[o]
        # print(Manager)
        parent = Manager.query.filter(Manager.id==option['manager_id']).first()
        ifManagerExist = Manager.query.filter( Manager.account == option["account"]).first()
        if ifManagerExist !=None:
            return jsonify({"code":500,"msg":"该账号已存在"})

        tempManager = {
            "account":option['account'],
            "name":option['name'],
            "description":option['description'],
            "parent_id":option["manager_id"],
            "password":option['password'],
            "language":parent.language
        }
        manager = Manager(**tempManager)
        db.session.add(manager)
        db.session.commit()
        return jsonify({"code":200})

    def editManager(self, option):
        # tempL = {}
        # for o in option:
        #    tempL[o]=option[o]
        # print(Manager)
        temp = Manager.query.filter(Manager.id==option['id']).first()
        ifManagerExist = Manager.query.filter( Manager.account == option["account"]).first()
        if ifManagerExist ==None:
            return jsonify({"code":500,"msg":"该管理员不存在,修改失败"})
        for o in option:
            if o=='id' or o=="manager_id":
                pass
            else:
                setattr(temp,o, option[o])
        db.session.commit()
        return jsonify({"code":200})

    def deleteManager(self, option):
        manager_list = Manager.query.filter(Manager.id.in_(option['ids'])).all()
        for m in manager_list:
            db.session.delete(m)
            db.session.commit()
        return jsonify({"code":200})
    
    def assignmentProject(self,option):
        assignment_manager = Manager.query.filter(Manager.id==option['assignment_id']).first()
        manager = Manager.query.filter(Manager.id==option['manager_id']).first()
        assignmentProjectIdList = option['assignmentProjectIdList']
        # 查出改管理员所有的项目
        project_set = Project.query.join(Project.m_manager).filter(Project.id.in_(assignmentProjectIdList)).all()
        # print(manager)
        print(project_set)
        assignment_manager.project=[]
        p_list = []
        for p in project_set:
            p_list.append(p)
        assignment_manager.project=p_list
        db.session.commit()
        return jsonify({"code":200})

    def getOwnPermission(self,option):
        manager = Manager.query.filter(Manager.id==option['manager_id']).first()
        permission_list = []
        for p in manager.permission:
            permission_list.append({'id':p.id,'name':p.name,'parent_id':p.parent_id})
        return jsonify({"code":200,'permissionList':permission_list})

    def getPermissionList(self,option):
        manager = Manager.query.filter(Manager.id==option['manager_id']).first()
        permission_list = []
        permission_set = Permission.query.filter().all()
        for p in permission_set:
            permission_list.append({'id':p.id,'name':p.name,'parent_id':p.parent_id})
        return jsonify({"code":200,'permissionList':permission_list})

    def assignmentPermission(self,option):
        assignment_manager = Manager.query.filter(Manager.id==option['assignment_id']).first()
        permission_list = option['permissionList']
        tempList = []
        for p in permission_list:
            temp = Permission.query.filter(Permission.id==p).first()
            tempList.append(temp)
        assignment_manager.permission=tempList
        return jsonify({"code":200})


managerInstance =ManagerClass()


@admin.route('/manager/getManager', methods=['POST'])
@decorator.login_required
def getManager():
    postData = json.loads(request.get_data().decode('utf-8'))
    result = managerInstance.getManager(postData['name'], int(
        postData['pageIndex']), int(postData['pageSize']),postData['manager_id'])
    return result

@admin.route('/manager/createManager', methods=['POST'])
@decorator.login_required

def createManager():
    # loads 将json字符串转为dict
    postData = request.get_json()
    cyu = CryptoUtil()
    decryObj = cyu.decrypt(postData['data'])
    data = eval(str(decryObj, encoding="gbk"))
    data['manager_id'] = int(data['manager_id'])
    result = managerInstance.createManager(data)
    return result

@admin.route('/manager/editManager', methods=['POST'])
@decorator.login_required

def editManager():
    # loads 将json字符串转为dict
    postData = request.get_json()
    cyu = CryptoUtil()
    decryObj = cyu.decrypt(postData['data'])
    data = eval(str(decryObj, encoding="gbk"))
    data['manager_id'] = int(data['manager_id'])
    data['id'] = int(data['id'])
    result = managerInstance.editManager((data))
    return result

@admin.route('/manager/deleteManager', methods=['POST'])
@decorator.login_required

def deleteManager():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # postData['ids'] = int(postData['ids'])
    result = managerInstance.deleteManager((postData))
    return result

@admin.route('/manager/assignmentPermission', methods=['POST'])
@decorator.login_required

def assignmentPermission():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # 被分配项目的管理员的id
    postData['assignment_id'] = int(postData['assignment_id'])
    # postData['ids'] = int(postData['ids'])
    result = managerInstance.assignmentPermission((postData))
    return result

@admin.route('/manager/assignmentProject', methods=['POST'])
@decorator.login_required

def assignmentProject():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # 被分配项目的管理员的id
    postData['assignment_id'] = int(postData['assignment_id'])
    # postData['ids'] = int(postData['ids'])
    result = managerInstance.assignmentProject((postData))
    return result


@admin.route('/manager/getPermissionList', methods=['POST'])

def getPermissionList():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # 被分配项目的管理员的id
    # postData['assignment_id'] = int(postData['assignment_id'])
    # postData['ids'] = int(postData['ids'])
    result = managerInstance.getPermissionList((postData))
    return result

@admin.route('/manager/getOwnPermission', methods=['POST'])
def getOwnPermission():
    # loads 将json字符串转为dict
    postData = json.loads(request.get_data().decode('utf-8'))
    postData['manager_id'] = int(postData['manager_id'])
    # 被分配项目的管理员的id
    # postData['assignment_id'] = int(postData['assignment_id'])
    # postData['ids'] = int(postData['ids'])
    result = managerInstance.getOwnPermission((postData))
    return result


@admin.route('/manager/login', methods=['POST'])
@csrf.exempt
def adminlogin():
    postData = request.get_json()
    cyu = CryptoUtil()
    decryObj = cyu.decrypt(postData['data'])
    managerObj = eval(str(decryObj, encoding="gbk"))
    account = managerObj['account']
    password = managerObj['password']
    ifManagerExist = Manager.query.filter(
        Manager.account == account, Manager.password == password).first()
    result = {}
    if ifManagerExist == None:
        result = {'code': 0, 'msg': '账号或密码错误'}
    else:
        result = {'code': 200, 'msg': '', 'manager_id': ifManagerExist.id,"csrfToken":generate_csrf()}
        session['manager_id'] = ifManagerExist.id
        userPointList = []
        for p in ifManagerExist.permission:
            userPointList.append(p.endpoint)
        session['userPointList'] = userPointList
    return json.dumps(result, ensure_ascii=False)
    # pass

@admin.route('/manager/create_rsa_key', methods=['POST'])
def create_rsa_key():
    postData = request.get_json()
    account = postData['account']
    password = postData['password']
    ifManagerExist = Manager.query.filter(
        Manager.account == account, Manager.password == password).first()
    if ifManagerExist ==None:
        result = {'code': 500, 'msg': '账号或密码错误'}
    else:
        cyu = CryptoUtil()
        public_key = cyu.create_rsa_key()
        result = jsonify({"code":200,"public_key":bytes.decode(public_key)})
    return result
    # pass

