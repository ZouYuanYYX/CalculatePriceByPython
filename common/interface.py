# -*- coding:UTF-8 -*-
__author__ = 'joy'
import requests
import json
#接口调用
def getInterface(url):
	response = requests.get(url)
	jsonData = json.loads(response.text)
	return jsonData

def postInterface(url,params):
	r = requests.post(url,data=params)
	print(r.text)
	return r.text