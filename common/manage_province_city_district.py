# -*- coding:UTF-8 -*-
__author__ = 'joy'
#用来处理省市区，比如获取经纬度，获取省市区编码等

import interface
import json

#获取经纬度接口,参数为：省市区
def getLonAndLat(province,city,district) :
	address = province+city+district
	print address
	url = "http://restapi.amap.com/v3/geocode/geo?parameters&key=42486373c418f95081859373652dc281&address="+address
	#response = json.loads(interface.getInterface(url))
	response = interface.getInterface(url)
	geocodesList = response['geocodes']
	geocodes = geocodesList[0]
	location = geocodes['location']
	#需要将经纬度返回，用逗号分隔
	print location
	return location


#origin为出发地经纬度，destination为目的地经纬度,
# 获取两个经纬度间的导航距离
def getNavigationDistance(origin,destination,sessionId):
	url = "http://crm.redlion56.com/gwcrm/crm/web/common/getNavigationDistanceByAMAP.do?sessionId="+sessionId
	params = {'origin':origin,'destination':destination}
	response = json.loads(interface.postInterface(url,params))
	#如果写死的sessionId过期了，就后台登陆后调用
	if (response['success'] == False) :
		sessionId = xiaoerLogin()
		url = "http://crm.redlion56.com/gwcrm/crm/web/common/getNavigationDistanceByAMAP.do?sessionId="+sessionId
		response = json.loads(interface.postInterface(url, params))
		return response['body']
	return response['body']



#登陆小二
def xiaoerLogin():
	url = "http://crm.redlion56.com/gwlogin/user/login.do?account=15925917320&passwd=6dc05f6e44ffe78f1810383b3c9f9fa9&roleRefer=1"
	response = json.loads(interface.getInterface(url))
	return response['newSessionId']


#getLonAndLat('浙江省','杭州市','江干区')

