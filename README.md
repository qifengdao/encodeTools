# encodeTools
支持aes,des,md5加批量解密的工具

目前支持 md5加密（不可逆），des 和aes加密解密（可逆），运行方式：

1，直接将encode.exe和conf.ini放到相同目录下
2，按需要修改conf.ini各参数的值（见下面说明）
3，双击执行encode.exe执行，查看output输出结果。


# conf.ini配置说明
[global]

input=D:\phone.txt 

output=D:\rs_des.txt

password=2017

code=UTF-8

type=des


# 必填参数介绍：
input 需加密或解密的源文件路径（文本格式，每行一条为需加密或者解密数据）

output 加密或者解密后的结果文件存储位置

password 加密或者解密密码（des,des-de情况下需要为8个字符；aes,aes-de情况下不大于32个字符；md5时随便填不会用到）

code 结果文件编码形式，如UTF-8

type  解密加密类型（md5:标识md5加密；des:标识des加密； aes:标识aes加密； des-de:标识des解密；aes-de:标识是aes解密）
