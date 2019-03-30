# 本代码引入Pycryptodome基于Python3.50版本编译库
from binascii import unhexlify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64
# from Crypto.Hash import SHA1
# from Crypto.Signature import pkcs1_15

class CryptoUtil():
  def __init__(self):
    self.password='linghogn2019' #生成privateKey时用到,私钥解密用到

  def create_rsa_key(self):
      """
      创建RSA密钥,步骤说明：
      1、从 Crypto.PublicKey 包中导入 RSA，创建一个密码(此密码不是RSA秘钥对)
      2、生成 1024/2048 位的 RSA 密钥对(存储在私钥文件和公钥文件)
      3、调用 RSA 密钥实例的 exportKey 方法(传入"密码"、"使用的 PKCS 标准"、"加密方案"这三个参数)得到私钥。
      4、将私钥写入磁盘的文件。
      5、使用方法链调用 publickey 和 exportKey 方法生成公钥，写入磁盘上的文件。
      """
      key = RSA.generate(1024)
      encrypted_key = key.exportKey(passphrase=self.password, pkcs=8,protection="scryptAndAES128-CBC")
      # encrypted_key = key.exportKey(pkcs=1)
      print('encrypted_key:',encrypted_key)
      with open("my_private_rsa_key.pem", "wb") as f:
          f.write(encrypted_key)
      with open("my_rsa_public.pem", "wb") as f:
          f.write(key.publickey().exportKey())
      return key.publickey().exportKey()
  def encrypt(self,text):
      # 加载公钥用于加密
      recipient_key = RSA.import_key(
          open("my_rsa_public.pem").read()
      )
      
      cipher_rsa = PKCS1_v1_5.new(recipient_key)
      #使用base64编码保存数据方便查看，同样解密需要base64解码
      en_data = base64.b64encode(cipher_rsa.encrypt(text))
      #  en_data = (cipher_rsa.encrypt(b'{"username":"admin","password":"123123"}'))
      print("加密数据信息：",type(en_data),'\n',len(en_data),'\n',en_data)
      return en_data

  def decrypt(self,text):
  
      # 加载私钥用于解密
      encoded_key = open("my_private_rsa_key.pem").read()
      private_key = RSA.import_key(encoded_key,passphrase=self.password)
      cipher_rsa = PKCS1_v1_5.new(private_key)
      
      data = cipher_rsa.decrypt(base64.b64decode(text), None)
      #  data = cipher_rsa.decrypt((en_data), None)
      return data
       
  # def rsa_sign(message,password="123456"):
  #      #读取私钥信息用于加签
  #      private_key = RSA.importKey(open("my_private_rsa_key.pem").read(),passphrase=password)
  #      hash_obj = SHA1.new(message)
  #      # print(pkcs1_15.new(private_key).can_sign())  #check wheather object of pkcs1_15 can be signed
  #      #base64编码打印可视化
  #      signature = base64.b64encode(pkcs1_15.new(private_key).sign(hash_obj))
  #      return signature
  
  # def rsa_signverify(message,signature):
  #      #读取公钥信息用于验签
  #      public_key = RSA.importKey(open("my_rsa_public.pem").read())
  #      #message做“哈希”处理，RSA签名这么要求的
  #      hash_obj = SHA1.new(message)
  #      try:
  #          #因为签名被base64编码，所以这里先解码，再验签
  #          pkcs1_15.new(public_key).verify(hash_obj,base64.b64decode(signature))
  #          print('The signature is valid.')
  #          return True
  #      except (ValueError,TypeError):
  #          print('The signature is invalid.')
 
if __name__ == '__main__':
    # pass
    cyu = CryptoUtil()
    cyu.create_rsa_key()
    # encrypt_and_decrypt_test()
    # message = b'Luosu is a Middle-aged uncle.'
    # signature = rsa_sign(message)
    # print('signature:',signature)
    # print(rsa_signverify(message,signature))
