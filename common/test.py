#coding=utf-8
import requests
import json

url = 'https://api.douban.com/v2/movie/search'
params=dict(q=u'刘德华')
r = requests.get(url, params=params)
print 'Search Params:\n', json.dumps(params, ensure_ascii=False)
print 'Search Response:\n', json.dumps(r.json(), ensure_ascii=False, indent=4)
