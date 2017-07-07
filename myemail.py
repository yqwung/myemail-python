#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 发送邮件，可以带附件，附件名可以是中文
# 注意邮箱密码不一定是注册密码，比如163邮箱，用第三方发送，不能用密码，要用163的授权码
# 邮件附件路径不对时，邮件将发送失败，不带附件时，要在代码中删除，附件部分

import os             # 导入os模块
import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

#-------------------------------------------------------------------------------------------------

print("发送邮件提示！")
print("-----------------------------------------------------------------")
print("| 邮箱类型 |   SMTP服务器     | SSH协议端口号 | 非SSH协议端口号 |")
print("-----------------------------------------------------------------")
print("|   163    |  smtp.163.com    |               |       25        |")
print("-----------------------------------------------------------------")
print("|   QQ     |  smtp.qq.com     |      465      |                 |")
print("-----------------------------------------------------------------")
print("| avctime  | smtp.ym.163.com  |               |       25        |")
print("-----------------------------------------------------------------")
print("\n")

#-------------------------------------------------------------------------------------------------

my_sender = input('发件人(form): ')                 # 发件人邮箱账号
my_pass = getpass.getpass('密  码(password): ')     # 发件人邮箱密码，或者授权码
my_server = input('服务器(SMTP server): ')          # 发件服务器
my_port = 25                         # 发件端口号，常用25或465 

my_user = input('收件人(to): ')      # 收件人邮箱账号

if( "@163.com" in my_sender):
	my_port = 25 
elif( "@qq.com" in my_sender):
	my_port = 465
elif( "@avctime.cn" in my_sender):
	my_port = 25

my_subject = 'Python发送邮件'        # 邮件标题，主题
my_text = 'Python email'             # 邮件内容
my_attachment = 'test.txt'           # 邮件附件   'D:\\work\\python\\test.txt'

#-------------------------------------------------------------------------------------------------

def mail():
	ret = True
	try:
		#msg = MIMEText(my_text, 'plain', 'utf-8')    # 创建文本邮件实例
		msg = MIMEMultipart()                               # 创建一个带附件邮件实例
		
		msg['From']=formataddr(["sender", my_sender])       # 括号里的对应发件人邮箱昵称、发件人邮箱账号		
		msg['To']=formataddr(["receiver", my_user])         # 括号里的对应收件人邮箱昵称、收件人邮箱账号		
		msg['Subject']=my_subject                           # 邮件的主题，也可以说是标题	
		
		msg.attach(MIMEText(my_text, 'plain', 'utf-8'))     # 邮件文本内容		
			
		basename = os.path.basename(my_attachment)          # 获取附件名（去掉附件的目录）
		att1 = MIMEText(open(my_attachment, 'rb').read(), 'base64', 'utf-8')  # 邮件附件
		att1["Content-Type"] = 'application/octet-stream'			
		att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', basename)) # filename为附件名
		msg.attach(att1)                                    # 邮件附件	
		
		if( "@163.com" in my_sender):
			server = smtplib.SMTP(my_server, my_port)       # 发件人邮箱中的SMTP服务器，端口号  # 注意，非SSL使用smtplib.SMTP()
		elif( "@qq.com" in my_sender):
			server = smtplib.SMTP_SSL(my_server, my_port)   # SSL使用smtplib.SMTP_SSL()
		elif( "@avctime.cn" in my_sender):
			server = smtplib.SMTP(my_server, my_port) 
		server.login(my_sender, my_pass)                    # 发件人邮箱账号、邮箱密码		
		server.sendmail(my_sender, [my_user,], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件		
		server.quit()  # 关闭连接		
	except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
		ret = False
	return ret

#-------------------------------------------------------------------------------------------------	

if __name__=='__main__':
	ret = mail()
	if ret:
		print("邮件发送成功")
	else:
		print("邮件发送失败")

	input("press enter to quit!")