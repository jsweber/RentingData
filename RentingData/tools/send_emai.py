import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

def send_email(content='邮件内容', title='no data no life 爬虫运行通知'):
    my_sender='nodatanolife@qq.com'    # 发件人邮箱账号
    my_pass = 'deyqqpsuocwfdcgh'              # 当时申请smtp给的口令
    my_user=['951092973@qq.com']     # 收件人邮箱账号

    msg=MIMEText(content,'plain','utf-8')
    msg['Subject']=title # 邮件标题
    msg['From']=Header("发件人<scrapy>", 'utf-8')
    msg['To']=Header("收件人<管理员>", 'utf-8')

    try:
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_user, msg.as_string())
        server.quit()# 关闭连接
        return True
    except Exception as e:
        print('[email send failed]',e)
        return False

if __name__ == '__main__':
    if send_email('发送邮件', 'test main'):
        print('发送成功')
    else: 
        print('发送失败')
