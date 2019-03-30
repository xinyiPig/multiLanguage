import urllib.request
import time
import json
import threading


class AccssToken():
  def __init__(self):
    self.appId = 'wxff3cfebbdcbcd135'
    self.appScrect = 'b9774614f15c56e6e42884ff84ee5168'
    self.__accessToken = ''
    self.__time = 0

  def get_accessToken(self):
      return self.__accessToken

  def __real_get_accessToken(self):
    while(True):
      try:
          postUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (self.appId, self.appScrect)
          urlResp = urllib.request.urlopen(postUrl)
          urlResp = json.loads(urlResp.read().decode('utf-8'))
          self.__accessToken = urlResp['access_token']
      except :
        pass
      print('定时获取获取accessToken'+self.__accessToken)
      # 从程序启动开始，就一直隔7000秒获取一次access_token
      time.sleep(240)

# 从程序启动开始，新开一条线程去启动获取access_token
  def loop_getAccessToken(self):
      t = threading.Thread(target=self.__real_get_accessToken,name='loop_getAccessToken')
      t.start()
      # t.end()
      # self.__real_get_accessToken()

