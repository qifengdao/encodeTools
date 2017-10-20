# -*- coding:utf-8-*-
'''
Created on 2017年4月18日

@author: zhoulongliu
'''
import sys,codecs,os
import ConfigParser
from Crypto.Cipher import AES
from pyDes import *
import md5
from binascii import b2a_hex, a2b_hex


def get_pwd(password):
        length = 16
        max_length = 32
        count = len(password)
        if count < length:
            add = (length - count)
            text = password + ('\0' * add)
        elif count > length and count < max_length:
            add = (max_length - count)
            text = password + ('\0' * add)
        else:
            print "aes 密码长度1到32个字符"
            sys.exit(-1)
        return text
    
def encrypt_aes(key, mode, text):
        cryptor = AES.new(key,mode,b'0000000000000000')
        #这里密钥key 长度必须为16（AES-128）,
        #24（AES-192）,或者32 （AES-256）Bytes 长度
        #目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext)
     
    #解密后，去掉补足的空格用strip() 去掉
def decrypt_aes(key, mode, text):
        cryptor = AES.new(key, mode, b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
    
    
if __name__ == '__main__':
    print 'start!'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    config = ConfigParser.ConfigParser()
    flag = 0
    if not os.path.exists('conf.ini'):
        print '确实conf.ini配置文件'
        flag = 1
    config.read("conf.ini")
    if not config.has_option("global", "input") :
        print '缺少input参数'
        flag = 1
    if not config.has_option("global", "output") :
        print '缺少output参数'
        flag = 1
    if not config.has_option("global", "password") :
        print '缺少password参数'
        flag = 1
    if not config.has_option("global", "type"):
        print '缺少type参数'
        flag = 1
    if not config.has_option("global", "code") :
        print '缺少code参数'
        flag = 1
        
    while True and flag == 1:
        hello = raw_input('输入任意非空字符结束:')
        if hello != '':
            sys.exit(-1)
    
    input = config.get("global", "input");
    output = config.get("global", "output");
    password = config.get("global", "password")
    type = config.get("global", "type")
    code = config.get("global", "code")
    if type not in ('md5','des-de','des','aes','aes-de'): 
        flag = 1
        print 'type 必须值为md5或者des，aes,des-de,es-de'
    while True and flag == 1:
        hello = raw_input('输入任意非空字符结束:')
        if hello != '':
            sys.exit(-1)
            
    wf = codecs.open(output, 'w', code)
    if type == 'md5' :
        with open(input, 'r') as fd:
            for line in fd:
                m = md5.new()
                m.update(line.strip())
                wf.write(m.hexdigest() + '\n')
    if type == 'des' :
        KEY = password    #密钥
        IV = password     #偏转向量
        # 使用DES对称加密算法的CBC模式加密
        with open(input, 'r') as fd:
            for line in fd:
                k = des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
                d = k.encrypt(line.strip())
                wf.write(b2a_hex(d)+"\n")
                
    if type == 'des-de' :
        KEY = password    #密钥
        IV = password     #偏转向量
        # 使用DES对称加密算法的CBC模式加密
        with open(input, 'r') as fd:
            for line in fd:
                k = des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
                d = k.decrypt(a2b_hex(line.strip()))
                wf.write(d+"\n")
    if type == 'aes':
        password = get_pwd(password)
        with open(input, 'r') as fd:
            for line in fd:
                d = encrypt_aes(password, AES.MODE_CBC, line.strip())
                wf.write(b2a_hex(d)+"\n")
    if type == 'aes-de' :
        password = get_pwd(password)
        with open(input, 'r') as fd:
            for line in fd:
                d = decrypt_aes(password, AES.MODE_CBC, a2b_hex(line.strip()))
                wf.write(d+"\n")
    print 'finish!'
    wf.close()