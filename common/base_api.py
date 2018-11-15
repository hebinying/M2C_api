#coding=utf-8
import json
import xlrd,xlwt
from xlutils.copy import copy
import requests
import os,datetime

firstrowname=['id','method','url','params','headers','body','type','checkpoint','isPressTest','Pparams','statuscode','times','error','msg','result']

def send_requests(s,testdata):
    print testdata
    method=testdata['method']
    url=testdata['url']
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


    # files参数如何传
    if type=='data':
        body=bodydata
    elif type=='json':
        body=json.dumps(bodydata)
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
                   params=param,
                   timeout=30)

    #对返回结果的操作
    res={}
    res["id"]=testdata["case_id"]
    res["row_num"]=testdata["rowNum"]
    res["method"]=method
    res["statuscode"]=str(resp.status_code)
    res["times"]=resp.elapsed.total_seconds()
    # print "times:"+str(resp.elapsed.total_seconds())
    #是否需要转码
    res["msg"]=resp.content
    res["header"]=resp.headers
    res["encoding"]=resp.encoding
    res["url"]=resp.url
    res["request"]=resp.request
    if res["statuscode"]!="200":
        res["error"]=res["msg"]
        res["result"]=False
    else:
        res["error"]=""
        res["result"]=True

    res["reason"]=resp.reason
    res["cookie"]=resp.cookies
    res["msg"]=resp.text
    res["text"]=resp.text
    # print "text:"+resp.text
    # print res["row_num"]
    return res

def write_result(result,filepath="result.xlsx"):
    if os.path.exists(filepath)==False:
        wb=xlwt.Workbook()
        sheet=wb.add_sheet("createtoday")
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

    row_num=result["row_num"]
    # 写入结果
    sheet.write(row_num,0,result["id"])
    sheet.write(row_num,1,result["method"])
    sheet.write(row_num, 2, result["url"])
    sheet.write(row_num, 10, result["statuscode"])
    sheet.write(row_num, 12, result["error"])
    sheet.write(row_num, 11, result["times"])
    sheet.write(row_num, 13, result["msg"])
    sheet.write(row_num,14,result["result"])

    wb.save( filepath)



if __name__=='__main__':
    s=requests.session()

    data={'method': 'GET',
          'url':"http://api.m2c2017test.com/m2c.scm/dealer/app/goods/list",
          'param':{"dealerId": "JXS1382A365F7D94350991D84AF23233FD7",
                   "goodsStatus":"",
                   "pageNum":1,
                   "rows":10}
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
    write_result(res)
