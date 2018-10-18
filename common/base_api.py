import json
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

    type=testdata['type']
    try:
        bodydata=testdata['body']
    except:
        bodydata={}

    try:
        verify=testdata['verify']
    except:
        verify=False


    #files参数如何传
    if type=='data':
        body=bodydata
    elif type=='json':
        body=json.dumps(bodydata)
    else:
        body=bodydata

    #使用prepared与未使用的prepared的差别

    req=requests.Request(method=method,
                         url=url,
                         params=param,
                         headers=headers,
                         data=body,
                         verify=verify)
    prepped=req.prepare()
    prepped=s.prepare_request(req)
    resp=s.send(prepped,
                timeout=30)


    #对返回结果的操作
    res={}
    res["statuscode"]=str(resp.status_code)
    res["time"]=resp.elapsed.total_seconds()





if __name__=='__main__':
    s=requests.session()
    datas=({"a":1,"b":2},{"a":3,"b":2})
    for data in datas:
        send_requests(s,data)
