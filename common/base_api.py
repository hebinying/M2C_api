#coding=utf-8
import json
import xlrd,xlwt
import requests
import os,datetime

firstrowname={'id','method','url','params','headers','body','type','checkpoint','isPressTest','Pparams','statuscode','times','error','result','msg'}

def send_requests(s,testdata):
    method=testdata['method']
    url=testdata['url']
    try:
        param=testdata['param']
    except:
        param=None

    # name='eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiJKV1Q6ODdlZGI3ZTMtNzAzMi00NmY0LTgzMDEtOThhMjkxMWEzYWVkIiwiaWF0IjoxNTM5ODQzMjU4LCJzdWIiOiJ7XCJjcmVhdGVUaW1lXCI6XCIyMDE3LTA3LTEwIDA5OjU5OjMyXCIsXCJlbWFpbFwiOlwiYWRtaW5AbTJjLmNvbVwiLFwibmFtZVwiOlwibXR4MTIxNVwiLFwibm90ZVwiOlwibm90ZVwiLFwicGVybWlzc2lvbktleVwiOlwiSldUOlNZU1RFTTpQRVJNSVNTSU9OOjc5ZjQ5MzU2MDEzODQwZDU5YmI2MDEzM2EwMDBjZDU0XCIsXCJyb2xlSWRcIjpcIjFcIixcInJvbGVOYW1lXCI6XCLotoXnuqfnrqHnkIblkZhcIixcInRlbE5vXCI6XCIxMzgyODc0OTc1NVwiLFwidXBkYXRlVGltZVwiOlwiMjAxOC0xMC0xOCAxNDoxNDoxN1wiLFwidXNlcklkXCI6XCI2YzcxMWU4ZTNmMDUxMjM0NTBkODMwYjk0YzcwNGNjYTc5OWZcIixcInVzZXJOYW1lXCI6XCJtdHgxMjE1XCIsXCJ1c2VyTm9cIjpcIjFcIixcInVzZXJTdGF0dXNcIjpcIk5PUk1BTFwifSIsImV4cCI6MTUzOTkyOTY1OH0.dAtjzKq0qTqViqbi3-X7616tox6HocHINOVQultV28D6-ztcBXTlOszhhcpfYcPML26U9ZUISo1vLVulnVTVAMaKnPeRrw7GJGIAffHbJ-hsmtxFTLq4TLXEP-zty4OCQ80CFOKtzX0I9BPVWnYkmBX0Ig-Os0QeeXoa-wFU5ww'
    # try:
    #     header=testdata['headers']
    # except:
    #     headers={'token':name}
    # try:
    #     type=testdata['type']
    # except:
    #     type=""
    # try:
    #     bodydata=testdata['body']
    # except:
    #     bodydata={}

    # try:
    #     verify=testdata['verify']
    # except:
    #     verify=False


    #files参数如何传
    # if type=='data':
    #     body=bodydata
    # elif type=='json':
    #     body=json.dumps(bodydata)
    # else:
    #     body=bodydata

    #使用prepared与未使用的prepared的差别

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
                   params=param)
    print resp.url
    print resp.status_code
    #对返回结果的操作
    res={}
    res["statuscode"]=str(resp.status_code)
    res["times"]=resp.elapsed.total_seconds()
    #是否需要转码
    res["context"]=resp.content
    res["header"]=resp.headers
    res["encoding"]=resp.encoding
    res["url"]=resp.url
    res["request"]=resp.request
    res["row_num"]=1
    if res["statuscode"]!="200":
        res["error"]=res["context"]
    else:
        res["error"]=""

    res["reason"]=resp.reason
    res["cookie"]=resp.cookies
    res["text"]=resp.text
    print s
    print "here"
    return res

def write_result(result,filepath="result.xlsx"):
    if os.path.exists(filepath)==False:
        wb=xlwt.Workbook()
        sheet=wb.add_sheet("createtoday")
    else:
        wb=xlrd.open_workbook(filepath)
        sheet=wb.get_sheet(0)

    row_num=result["row_num"]
    # 写入结果
    # sheet0.write(row_num,0,result["id"])
    sheet.write(row_num, 1, result["url"])
    sheet.write(row_num, 2, result["statuscode"])
    sheet.write(row_num, 3, result["error"])
    sheet.write(row_num, 4, result["times"])
    # sheet.write(row_num, 5, result["msg"])

    # for result in results:
    #     print result["row_num"]
    #     row_num=1
    #     #写入结果
    #     # sheet0.write(row_num,0,result["id"])
    #     sheet.write(row_num,1,result["url"])
    #     sheet.write(row_num,2,result["statuscode"])
    #     sheet.write(row_num,3,result["error"])
    #     sheet.write(row_num,4,result["times"])
    #     sheet.write(row_num,5,result["msg"])
    wb.save( filepath)



if __name__=='__main__':
    s=requests.session()

    data={'method': 'OPTIONS',
          'url':"http://api.m2c2017test.com/m2c.scm/dealer/app/goods/list",
          'param':{"dealerId": "JXS1382A365F7D94350991D84AF23233FD7",
                   "goodsStatus":"",
                   "pageNum":"",
                   "rows":""}
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
