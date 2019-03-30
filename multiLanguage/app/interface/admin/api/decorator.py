from functools import wraps
from flask import Flask,request,session,jsonify,g
from ....models.Permission import Permission
# 需要经过权限校验的视图类别


def getAllPermissionList():
    tempList = []
    permission_set = Permission.query.filter().all()
    for p in permission_set:
        tempList.append(p.endpoint)
    return tempList

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        userPointList = session.get('userPointList')
        needCheckPointList = session.get('needCheckPointList')
        endpoint = request.endpoint
        # 判断用户是否已经登录
        if userPointList ==None:
            return jsonify({'code':"601","msg":"请先登录"})
        if needCheckPointList==None:
            needCheckPointList = getAllPermissionList()
            session['needCheckPointList'] = needCheckPointList
    
        # 如果当前的视图需要检查权限，就要判断用户的权限中是否有这个视图的访问权限
        if endpoint in needCheckPointList:
            if endpoint in session.get('userPointList'):
                return func(*args,**kwargs)
            else:
                return jsonify({"code":403,"msg":"权限不足，无法访问"})
        else:
            return func(*args,**kwargs)

        # print((request.url))
        # 获取用户的权限列表
        # username  = request.args.get("username")
        # if username and username == "angle":
        # else:
        #     return "请先登录"
    return wrapper