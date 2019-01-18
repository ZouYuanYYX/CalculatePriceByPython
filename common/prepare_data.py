# -*- coding:UTF-8 -*-
__author__ = 'joy'
import interface
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#调用开发的接口，获取相关数据

#根据货物id获取车型信息
def getCarTypeByGoodsName(goodsTypeId,sessionId):
	url = "http://hz.redlion56.com/gwhz/goodsowner/app/stationOrder/getCarTypeByGoodsTypeId.do?sessionId="+sessionId+"&goodsTypeId=" + goodsTypeId
	r = interface.getInterface(url)['body']
	carTypeInfo = {'key': r['key'], 'value': r['value']}
	print carTypeInfo
	return carTypeInfo['key']


#根据运量获取车长
def getCarLengthByTonCube(ton,cube,sessionId):
	url = "http://hz.redlion56.com/gwhz/goodsowner/app/stationOrder/getCarLengthByTonCube.do?sessionId="+sessionId+"&ton=" + ton+"&cube="+cube
	r = interface.getInterface(url)['body']
	carLengthInfo = {'key': r['key'], 'value': r['value']}
	print carLengthInfo
	return carLengthInfo['key']


#根据出发地、目的地经纬度，获取时效信息,这里返回的数据给页面展示用
def getAgingConfigInfo(origin,destination,sessionId):
	url = "http://hz.redlion56.com/gwhz/goodsowner/app/stationOrder/getAgingConfigInfo.do?sessionId="+sessionId+"&origin="+origin+"&destination="+destination
	r = interface.getInterface(url)['body']
	agingInfo = {'standardTime':r['standardTime'].encode('utf-8'),'commonTime':r['commonTime'].encode('utf-8'),'urgentTime':r['urgentTime'].encode('utf-8'),'id':r['id']}
	print agingInfo
	return agingInfo

#origin = '121.46924,31.22986'
#destination = '101.803717,36.599745'
#getAgingConfigInfo(origin,destination)
