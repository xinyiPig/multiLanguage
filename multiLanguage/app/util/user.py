import urllib.request
import json


class ab_User():
    def __init__(self):
        self.appId = 'wxff3cfebbdcbcd135'
        self.appScrect = 'b9774614f15c56e6e42884ff84ee5168'

    def getOpenId(self, code):
        getUrl = ' https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
            self.appId, self.appScrect, code)
        urlResp = urllib.request.urlopen(getUrl)
        urlResp = json.loads(urlResp.read().decode('utf-8'))
        return urlResp
    

    def getUserInfo(self, access_token, openId):
        getUrl = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
           access_token, openId)
        urlResp = urllib.request.urlopen(getUrl)
        urlResp = json.loads(urlResp.read().decode('utf-8'))
        return urlResp

    def getWage(self,id):
        pass

