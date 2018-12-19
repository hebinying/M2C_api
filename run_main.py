#coding=gbk
import unittest
import os
import HTMLTestRunner
import datetime,logging
from email import Utils
import smtplib
import re
import xml.dom.minidom
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

curpath=os.path.dirname(os.path.realpath(__file__))
print curpath
report_path=os.path.join(curpath,"report")
if not os.path.exists(report_path):os.mkdir(report_path)

case_path=os.path.join(curpath,"testcase")

print case_path
def add_case(casepath=case_path,rule="test*.py"):
    discover=unittest.defaultTestLoader.discover(casepath,
                                                 pattern=rule)
    print discover
    return discover


def run_case(all_case,reportpath=report_path):
    now=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print now
    htmlreport=reportpath+r"\result"+now+".html"
    print "测试报告生成地址：%s" %htmlreport
    fp=file(htmlreport,"wb")
    runner=HTMLTestRunner.HTMLTestRunner(stream=fp,
                                         verbosity=1,
                                         title=u"api测试报告"+datetime.datetime.now().strftime("%Y%m%d"),
                                         description=u"用例执行情况")
    runner.run(all_case)
    fp.close()

# emailConf= r".\config/email_cofig.xml"
emailConf =ROOT( r"config/email_cofig.xml")

#移除生成的报告文件
def removefile(filepath=r'./report',name='.html'):
    filepath=ROOT(filepath)
    print "获取删除报告路径："+filepath
    dirs=os.listdir(filepath)

    for dir in dirs:
        if os.path.splitext(dir)[1]==name:
            file=filepath+'/'+dir
            print "开始删除文件:"+file
            os.remove(file)
            print "删除文件:" + file+"成功"

class CommEmail:

    def __init__(self):
        print "init"
        self.sIp = ""
        self.sPort = ""
        self.sUser = ""
        self.sPassword = ""
        self.fEmailServerConfFile = ""
        self.fEmailTemplateFile = ""
        self.sEmailOwner = ""
        self.dEmailTo = []
        self.dEmailCC = []
        self.dattach = []
        self.sSubject = ""
        self.emComment = []
        self.tDate = Utils.formatdate(localtime=1)
        # logging.basicConfig(level=logging.DEBUG,
        #                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        #                     datefmt='%a, %d %b %Y %H:%M:%S',
        #                     filename='Email.log',
        #                     filemode='a')

        # from conf-profile to set email-server  configure
        self.fEmailServerConfFile=emailConf
        print "邮件配置路径："+self.fEmailServerConfFile
        try:
            print "邮件信息初始化"
            xmlFeed = xml.dom.minidom.parse(self.fEmailServerConfFile)
            xmlEmaiSMTP = xmlFeed.getElementsByTagName('smtp')
            xmlEmailFrom = xmlFeed.getElementsByTagName('From')
            xmlEmaiTos = xmlFeed.getElementsByTagName('To')
            # xmlEmaiCCs = xmlFeed.getElementsByTagName('CC')
            xmlEmailSubject = xmlFeed.getElementsByTagName('Subject')
            xmlEmailComments = xmlFeed.getElementsByTagName('comment')
            xmlEmailattachs = xmlFeed.getElementsByTagName('attach')
            print "邮件信息初始化1"
            # only one smtp-tag
            for smtpConf in xmlEmaiSMTP:
                self.sIp = smtpConf.getAttribute("ip")
                self.sPort = smtpConf.getAttribute("port")
                self.sUser = smtpConf.getAttribute("user")
                self.sPassword = smtpConf.getAttribute("password")

            print "邮件信息初始化2"
            # To
            for To in xmlEmaiTos:
                print "邮件信息初始化4"
                print To
                file = To.getAttribute("file")
                print file
                f=open((ROOT(file)).decode('utf-8'),'r')
                s=f.readlines()
                for i in s:
                    print i
                    self.dEmailTo.append(i.split('\n')[0])
            # CC
            # for cc in xmlEmaiCCs:
            # self.dEmailCC.append(cc.getAttribute("address"))

            # From & Subject
            self.sEmailOwner = xmlEmailFrom[0].getAttribute("address")
            self.sSubject = xmlEmailSubject[0].getAttribute("title")
            print "邮件信息初始化3"
            # self.emComment = open(xmlEmailComments[0].getAttribute("file")).read()
            # comment邮件内容
            for comment in xmlEmailComments:
                print comment
                cfile = ROOT(comment.getAttribute("file"))
                print cfile
                dirs=os.listdir(cfile)
                for dir in dirs:
                    # pattern=re.compile(r".*result+(.*?)+html")
                    #取文件名
                    text=os.path.splitext(dir)[1]
                    if text==".html":
                        # 邮件内容
                        print dir
                        #comment邮件内容
                        self.emComment.append(open(cfile+'/'+dir).read())
                        #添加报告
                        self.dattach.append(cfile+'/'+dir)
            print self.emComment
            print self.dattach
            logging.info(
                "smtp conf ====> ip: " + self.sIp + " " + "port: " + self.sPort + " " + "user: " + self.sUser + " password: " + self.sPassword)
            logging.info("init end")
        except:
            logging.warning("ERROR: EmailServerConfFile is ERROR !!!")
            logging.warning("exit(1) from __init__")
            print "fail"
            exit(1)

    # email comment & sendmail
    def sendHtmlEmail(self):
        msg = MIMEMultipart()
        #msg["Subject"] = self.sSubject+str(time.strftime("%Y-%m-%d",time.localtime((int(time.time()*1000))/1000)))
        msg["Subject"]=self.sSubject+str(datetime.datetime.now().strftime("%Y-%m-%d"))
        msg["From"] = self.sEmailOwner
        msg["To"] = ";".join(self.dEmailTo)
        msg["CC"] = ";".join(self.dEmailCC)
        msg["Date"] = self.tDate

        # email comment
        for comment in self.emComment:
            emailComment=MIMEText(comment, _subtype="html", _charset='utf-8')
            msg.attach(emailComment)
        #emailComment = MIMEText(self.emComment, _subtype="html", _charset='base64')
        # add eamil attach
        print "ssss"
        for attach in self.dattach:
            #t = MIMEBase('application', 'octet-stream')
            print attach
            t = MIMEBase('html', 'utf-8')
            t.set_payload(open(attach, 'rb').read())
            #encoders.encode_base64(t)
            #邮件的文件名标题不能太长，否则会添加失败
            t.add_header('Content-Disposition', 'attachment;filename="%s"' % os.path.basename(attach))
            #t.add_header('Content-Disposition', 'attachment;filename="discover.html"')
            msg.attach(t)

        try:
            #msg.attach(emailComment)
            emailHandle = smtplib.SMTP_SSL()
            emailHandle.set_debuglevel(1)
            emailHandle.connect('smtp.exmail.qq.com', int(self.sPort))
            emailHandle.login(self.sUser, self.sPassword)
            #发送邮件
            emailHandle.sendmail(msg["From"], msg["To"].split(';'), msg.as_string())

            emailHandle.quit()
            emailHandle.close()
            logging.info("Email for test was send")
        except:
            logging.warning("Error")
            exit(1)

if __name__=="__main__":
    formater='%(asctime)s %(process)d:%(pathname)s %(filename)s[line:%(lineno)d]  %(module)s %(funcName)s %(levelname)s %(message)s'
    logname=curpath+"./Report/log"+datetime.datetime.now().strftime("%Y%m%d")+".log"
    infoLogname=curpath+"./Report/infolog"+datetime.datetime.now().strftime("%Y%m%d")+".log"
    errorLogname=curpath+"./Report/errorlog"+datetime.datetime.now().strftime("%Y%m%d")+".log"
    logging.basicConfig(level=logging.NOTSET,
                        format=formater,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=logname,
                        filemode='a')
    cases=add_case()
    print "cases"
    print cases
    run_case(cases)
    # semail=CommEmail()
    # semail.sendHtmlEmail()
    # removefile()
