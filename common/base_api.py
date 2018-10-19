#coding=utf-8
import json
import xlrd
import requests

def send_requests(s,testdata):
    method=testdata['method']
    url=testdata['url']
    try:
        param=testdata['param']
    except:
        param=None

    name='eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiJKV1Q6ODdlZGI3ZTMtNzAzMi00NmY0LTgzMDEtOThhMjkxMWEzYWVkIiwiaWF0IjoxNTM5ODQzMjU4LCJzdWIiOiJ7XCJjcmVhdGVUaW1lXCI6XCIyMDE3LTA3LTEwIDA5OjU5OjMyXCIsXCJlbWFpbFwiOlwiYWRtaW5AbTJjLmNvbVwiLFwibmFtZVwiOlwibXR4MTIxNVwiLFwibm90ZVwiOlwibm90ZVwiLFwicGVybWlzc2lvbktleVwiOlwiSldUOlNZU1RFTTpQRVJNSVNTSU9OOjc5ZjQ5MzU2MDEzODQwZDU5YmI2MDEzM2EwMDBjZDU0XCIsXCJyb2xlSWRcIjpcIjFcIixcInJvbGVOYW1lXCI6XCLotoXnuqfnrqHnkIblkZhcIixcInRlbE5vXCI6XCIxMzgyODc0OTc1NVwiLFwidXBkYXRlVGltZVwiOlwiMjAxOC0xMC0xOCAxNDoxNDoxN1wiLFwidXNlcklkXCI6XCI2YzcxMWU4ZTNmMDUxMjM0NTBkODMwYjk0YzcwNGNjYTc5OWZcIixcInVzZXJOYW1lXCI6XCJtdHgxMjE1XCIsXCJ1c2VyTm9cIjpcIjFcIixcInVzZXJTdGF0dXNcIjpcIk5PUk1BTFwifSIsImV4cCI6MTUzOTkyOTY1OH0.dAtjzKq0qTqViqbi3-X7616tox6HocHINOVQultV28D6-ztcBXTlOszhhcpfYcPML26U9ZUISo1vLVulnVTVAMaKnPeRrw7GJGIAffHbJ-hsmtxFTLq4TLXEP-zty4OCQ80CFOKtzX0I9BPVWnYkmBX0Ig-Os0QeeXoa-wFU5ww'
    try:
        header=testdata['headers']
    except:
        headers={'token':name}
    try:
        type=testdata['type']
    except:
        type=""
    try:
        bodydata=testdata['body']
    except:
        bodydata={}

    # try:
    #     verify=testdata['verify']
    # except:
    #     verify=False


    #files参数如何传
    if type=='data':
        body=bodydata
    elif type=='json':
        body=json.dumps(bodydata)
    else:
        body=bodydata

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
    #对返回结果的操作
    res={}
    res["statuscode"]=str(resp.status_code)
    res["time"]=resp.elapsed.total_seconds()
    #是否需要转码
    res["context"]=resp.content
    res["header"]=resp.headers
    res["encoding"]=resp.encoding
    res["url"]=resp.url
    res["request"]=resp.request
    if res["statuscode"]!="200":
        res["error"]=res["context"]
    else:
        res["error"]=""

    res["reason"]=resp.reason
    res["cookie"]=resp.cookies
    res["text"]=resp.text
    return res

def write_result(results,filepath="result.xlsx"):
    wb=xlrd.open_workbook(filepath)
    sheet0=wb.get_sheet(0)
    for result in results:
        row_num=result["row_num"]
        #写入结果
        sheet0.write(row_num,0,result["id"])
        sheet0.write(row_num,1,result["url"])
        sheet0.write(row_num,2,result["statuscode"])



if __name__=='__main__':
    s=requests.session()
    params={"ie": "utf-8",
            "newi": 1,
            "mod": 1,
            "isbd": 1,
            "isid": "9968179c0004987a",
            "wd": "requests",
            "rsv_spt": 1,
            "rsv_iqid": "0x9a3acd6a0004efbc",
            "issp": 1,
            "f": 3,
            "rsv_bp": 1,
            "rsv_idx": 2,
            "ie": "utf-8",
            "rqlang": "cn",
            "tn": "baiduhome_pg",
            "rsv_enter": 0,
            "oq": "requests",
            "rsv_t": "464619kWUtIBOVkBZ3t35Vh04PwL+HpjW1cOUN3JUuEyZ3jJYDdThDloB7mVTZh4LHdp",
            "rsv_pq": "9968179c0004987a",
            "prefixsug": "requests",
            "rsp": 0,
            "bs": "requests",
            "rsv_sid": "1458_21122_18559_26350_20929",
            "_ss": 1,
            "clist": "6cdb785551fd62c4	2dfe1d6b086f751d",
            "hsug":"",
           "f4s": 1,
            "csor": 8,
            "_cr1": 35958}
    data={'method': 'get',
          'url':"https://www.baidu.com/s",
          'param':{"wd": u"接口测试自动化"}
          }
    send_requests(s,data)
