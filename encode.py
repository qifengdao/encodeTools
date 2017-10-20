# -*- coding:utf-8-*-
'''
Created on 2017��4��18��

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
            print "aes ���볤��1��32���ַ�"
            sys.exit(-1)
        return text
    
def encrypt_aes(key, mode, text):
        cryptor = AES.new(key,mode,b'0000000000000000')
        #������Կkey ���ȱ���Ϊ16��AES-128��,
        #24��AES-192��,����32 ��AES-256��Bytes ����
        #ĿǰAES-128 �㹻Ŀǰʹ��
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
        #��ΪAES����ʱ��õ����ַ�����һ����ascii�ַ����ģ�������ն˻��߱���ʱ����ܴ�������
        #��������ͳһ�Ѽ��ܺ���ַ���ת��Ϊ16�����ַ���
        return b2a_hex(ciphertext)
     
    #���ܺ�ȥ������Ŀո���strip() ȥ��
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
        print 'ȷʵconf.ini�����ļ�'
        flag = 1
    config.read("conf.ini")
    if not config.has_option("global", "input") :
        print 'ȱ��input����'
        flag = 1
    if not config.has_option("global", "output") :
        print 'ȱ��output����'
        flag = 1
    if not config.has_option("global", "password") :
        print 'ȱ��password����'
        flag = 1
    if not config.has_option("global", "type"):
        print 'ȱ��type����'
        flag = 1
    if not config.has_option("global", "code") :
        print 'ȱ��code����'
        flag = 1
        
    while True and flag == 1:
        hello = raw_input('��������ǿ��ַ�����:')
        if hello != '':
            sys.exit(-1)
    
    input = config.get("global", "input");
    output = config.get("global", "output");
    password = config.get("global", "password")
    type = config.get("global", "type")
    code = config.get("global", "code")
    if type not in ('md5','des-de','des','aes','aes-de'): 
        flag = 1
        print 'type ����ֵΪmd5����des��aes,des-de,es-de'
    while True and flag == 1:
        hello = raw_input('��������ǿ��ַ�����:')
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
        KEY = password    #��Կ
        IV = password     #ƫת����
        # ʹ��DES�ԳƼ����㷨��CBCģʽ����
        with open(input, 'r') as fd:
            for line in fd:
                k = des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
                d = k.encrypt(line.strip())
                wf.write(b2a_hex(d)+"\n")
                
    if type == 'des-de' :
        KEY = password    #��Կ
        IV = password     #ƫת����
        # ʹ��DES�ԳƼ����㷨��CBCģʽ����
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