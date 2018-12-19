# -*- coding: utf8 -*-
import json
import xlrd,xlwt
from xlutils.copy import copy
import requests
import os,datetime,sys
default_encoding='utf8'
if sys.getdefaultencoding()!=default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# firstrowname=['case_id','checkname','method','url','params','headers','type','checkpoint','isPressTest','Pparams','result','statuscode','times','result']
BasicData=['case_id','checkname','method','url','params','type','checkpoint','isPressTest','Pparams','result']
NCData=['body','error','msg']
firstrowname=['case_id','checkname','method','url','params','headers','body','type','statuscode','checkpoint','isPressTest','Pparams','times','error','msg','result']


def send_requests(s,testdata):
    print testdata
    method=testdata['method'].upper()
    print method
    url=testdata['url']
    print url
    try:
        param=testdata['param']
    except:
        param=None
    try:
        header=testdata['headers']
        print "header:"+header
    except:
        headers={'token':""}
    try:
        type=testdata['type']
        print "type:"+type
    except:
        type=""
    try:
        bodydata=testdata['body']
        print "bodydata:"+bodydata
    except:
        bodydata={}

    try:
        verify=testdata['verify']
        print "verify:"+verify
    except:
        verify=False

    re_data=re_json=""
    # files参数如何传
    if type=='data':
        re_data=bodydata
    elif type=='json':
        re_json=json.dumps(bodydata)
    else:
        body=bodydata

    # 使用prepared与未使用的prepared的差别

    # req=requests.Request(method=method,
    #                      url=url,
    #                      params=param,
    #                      headers=headers,
    #                      data=body)
    # prepped=req.prepare()
    # prepped=s.prepare_request(req)
    # resp=s.send(prepped,
    #             timeout=30)
    resp=s.request(method=method,
                   url=url,
                   data=re_data,
                   timeout=30)
    headers={"Content-Type": "application/x-www-form-urlencoded"}
    # resp=s.post(url=url,data=param)
    #打印出请求url
    print u"请求链接："+resp.url
    print u"返回结果："
    print resp.text
    #对返回结果的操作
    res={}
    # res["id"]=testdata["case_id"]
    # res["row_num"]=testdata["rowNum"]
    res["method"]=method
    res["statuscode"]=resp.status_code
    res["times"]=resp.elapsed.total_seconds()
    # print "times:"+str(resp.elapsed.total_seconds())
    #是否需要转码
    res["body"]=res["msg"]=resp.content
    res["headers"]=resp.headers
    res["encoding"]=resp.encoding
    res["url"]=resp.url
    res["request"]=resp.request

    if res["statuscode"]!="200":
        res["error"]=res["msg"]
        res["result"]=False
    else:
        res["result"] = True
        res["error"] = ""

    res["reason"]=resp.reason
    res["cookie"]=resp.cookies
    # res["msg"]=resp.text
    res["text"]=(resp.content).encode("utf8").decode("utf8")
    # print "text:"+resp.text
    # print res["row_num"]
    return res

def write_result(result,filepath="result.xlsx"):
    if os.path.exists(filepath)==False:
        wb=xlwt.Workbook()
        sheet=wb.add_sheet("today")
        for i in range(0,len(firstrowname)-1):
            sheet.write(0,i,firstrowname[i])
        row_num=1
    else:
        rb=xlrd.open_workbook(filepath)
        table=rb.sheet_by_index(0)
        # row_num=table.nrows
        wb=copy(rb)
        sheet=wb.get_sheet(0)
        #获取表格列表使用nrows失败

    # row_num=result["row_num"]
    row_num=0
    for value in firstrowname:
        if value not in BasicData:
            if value in NCData:
                result[value]=result[value].encode("utf8").decode("utf8")
                sheet.write(row_num,firstrowname.index(value),result[value])
            else:
                sheet.write(row_num,firstrowname.index(value),str(result[value]))
    wb.save(filepath)
if __name__=='__main__':
    s=requests.session()

    data={'method': 'POST',
          'url':"http://api.m2c2017test.com/m2c.media/partner/media/mediaAdd",
          'body':{'isMultiple':"" ,
                    'recordId':"" ,
                    'industryType':"" ,
                    'regionName': '广东省 深圳市 宝安区',
                    'scienceType':"" ,
                   'time': '2018 - 12 - 17, 2021 - 12 - 17',
                    'mediaId': '18MD925778572E1844A2A00CF2888705700B',
                    'mediaName': 'eeeesfsfsd1',
                    'tagAddr': '广东省 深圳市 宝安区  ',
                    'longitude': 113.900655,
                    'latitude': 22.610526,
                    'detailAddr':"" ,
                    'chargeName': "",
                    'chargePhone': "",
                    'contactMan':"" ,
                    'contactPhone': "",
                    'isDivide': 1,
                    'cooperNo':"" ,
                    'dateStart': 2018-12-13,
                    'dateEnd': 2021-12-13,
                    'effectDate': 2018-12-13,
                    'sceneRole': 2,
                    'sceneCity': "",
                    'sceneMedia':"" ,
                    'sceneCityName': "",
                    'sceneMediaName':"" ,
                    'userId': 'HY27D554B9040B4899B6F792E81244E880',
                    'userNo': '13510010021',
                    'userName': '123',
                    'bdStaffId': "",
                    'storeImgUrl': "",
                    'licenseImgUrl':"" ,
                    'togetherImgUrl': "",
                    'refereeName':"" ,
                    'refereePhone':"",
                    'creatorAccNo': '13510010059',
                    'sceneLevel':"",
                    "partnerId":'18PA04788A3943FC41C380E4464F9D980A01'},
          'type':"data"
          }
    # response=s.request(method="OPTIONS",
    #                    url="http://api.m2c2017test.com/m2c.scm/dealer/app/goods/list",
    #                    params={"dealerId": "JXS1382A365F7D94350991D84AF23233FD7",
    #                "goodsStatus":"",
    #                "pageNum":"",
    #                "rows":""})
    # print response.url
    # print response.status_code
    res=send_requests(s,data)
    print res
    write_result(res)
