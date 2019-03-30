# 多语言管理平台系统

1.buleprint 是蓝图，用来划分模块；在对应的模块里边初始化蓝图，引入视图router.py文件，然后到app __init__.py去注册蓝图即可在router.py中如下使用route
例如：@errorMsg.route('/): 这就是代表了host:port/errorMsg/