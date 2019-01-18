# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from common import manage_province_city_district
from common import database
from common import prepare_data
from calculate import  calculate_price
import json

# Create your views here.

@csrf_exempt
def window(request):
    return render(request, "page/window.html")

@csrf_exempt
def finished_automobile_line(request):
    return render(request, "page/finished_automobile_line.html")

@csrf_exempt
def finished_automobile_price(request):
    return render(request, "page/finished_automobile_price.html")

@csrf_exempt
def distpicker_data_js(request):
    return render(request,"page/js/distpicker.data.js")

@csrf_exempt
def distpicker_js(request):
    return render(request,"page/js/distpicker.js")

@csrf_exempt
def main_js(request):
    return render(request,"page/js/main.js")

@csrf_exempt
def getDistance(request):
    data = request.POST
    senderProvince = data.get("senderProvince")
    senderCity = data.get("senderCity")
    senderDistrict = data.get("senderDistrict")
    recipientProvince = data.get("recipientProvince")
    recipientCity = data.get("recipientCity")
    recipientDistrict = data.get("recipientDistrict")
    environment = data.get("environment")
    if (environment == "205环境"):
        sessionId = "201811199INnDXmzMduEjiL"
    if (environment == "预发环境"):
        sessionId = "20181124or0qjhYfEFtlDtb"

    origin = manage_province_city_district.getLonAndLat(senderProvince, senderCity, senderDistrict)
    destination = manage_province_city_district.getLonAndLat(recipientProvince, recipientCity, recipientDistrict)
    agingInfo = prepare_data.getAgingConfigInfo(origin,destination,sessionId)
    distance = manage_province_city_district.getNavigationDistance(origin, destination,sessionId)
    result = {'distance':distance,'agingInfo':[ agingInfo['standardTime'] ,agingInfo['commonTime'] ,agingInfo['urgentTime'] ]}
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def calculateVehiclePrice(request):
	data = request.POST
	#从前端获取数据
	selectCalcuteWay = data.get('selectCalcuteWay')

	senderProvince = data.get('senderProvince')
	senderCity = data.get('senderCity')
	senderDistrict = data.get('senderDistrict')

	recipientProvince = data.get('recipientProvince')
	recipientCity = data.get('recipientCity')
	recipientDistrict = data.get('recipientDistrict')

	distance = data.get("distance")
	goodsName = data.get("goodsName")
	tonnage = data.get("tonnage")
	volume = data.get("volume")
	agingWay = data.get("agingWay")
	loadUnloadTemplate = data.get("loadUnloadTemplate")
	invoiceWay = data.get("invoiceWay")

	environment = data.get("environment")
	if (environment == "205环境") :
		sessionId = "201811199INnDXmzMduEjiL"
	if (environment == "预发环境"):
		sessionId = "20181124or0qjhYfEFtlDtb"


	# 根据省市区名称获取对应的编号，如：330002
	senderAddress = handleProvinceName(senderProvince) + '-' + handleCityName(senderCity,senderProvince) + '-' + senderDistrict
	print senderAddress
	senderAddressCode = database.getAddressCode(senderAddress,environment)
	start_province = senderAddressCode['provinceid']
	start_city = senderAddressCode['cityid']
	start_district = senderAddressCode['district']
	print "执行了"
	# 根据省市区名称获取对应的编号，如：330002
	recipientAddress = handleProvinceName(recipientProvince) + '-' + handleCityName(recipientCity,recipientProvince) + '-' + recipientDistrict
	print recipientAddress
	recipientAddressCode = database.getAddressCode(recipientAddress,environment)
	arrive_province = recipientAddressCode['provinceid']
	arrive_city = recipientAddressCode['cityid']
	arrive_district = recipientAddressCode['district']

	origin = manage_province_city_district.getLonAndLat(senderProvince,senderCity,senderDistrict)
	destination = manage_province_city_district.getLonAndLat(recipientProvince,recipientCity,recipientDistrict)
	result = calculate_price.getOneVehicleLinePrice(start_province,start_city,start_district,arrive_province,arrive_city,arrive_district,
						   tonnage,volume,goodsName,selectCalcuteWay,distance,loadUnloadTemplate,invoiceWay,agingWay,origin,destination,sessionId,environment)
	if (result != ''):
		return HttpResponse(result)
	else:
		return HttpResponse('')

def handleProvinceName(provinceName):
	if (str(provinceName).endswith('市')):
		provinceName = provinceName[:-1]
	return provinceName

#要将二级地址市去掉
def handleCityName(cityName,provinceName):
	if ((provinceName == "吉林省") or (provinceName == "安徽省")or (provinceName == "湖北省")or (provinceName == "广东省")) :
		city_name = cityName
	elif ((cityName == "唐山市") or (cityName == "北京市")or (cityName == "重庆市")or (cityName == "天津市") or (cityName == "包头市")
			or (cityName == "毕节市") or (cityName == "铜仁市") or (cityName == "延安市") or (cityName == "渭南市") or (cityName == "咸阳市")
			or (cityName == "宝鸡市")or (cityName == "铜川市")or (cityName == "西安市")or (cityName == "汉中市")or (cityName == "榆林市")
			or (cityName == "安康市")or (cityName == "商洛市")or (cityName == "西宁市")or (cityName == "海东市")or (cityName == "固原市")
			or (cityName == "中卫市")or (cityName == "乌鲁木齐市")or (cityName == "克拉玛依市")or (cityName == "吐鲁番市")or (cityName == "三沙市")
			or (cityName == "乌海市") or (cityName == "赤峰市") or (cityName == "通辽市")or (cityName == "许昌市")):
		city_name = cityName
	elif (str(cityName).endswith('市')):
		city_name = cityName[:-1]
	elif (str(cityName).endswith('市辖区')):
		city_name = cityName[:-3]
	return city_name


def test(senderProvince,senderCity,senderDistrict,recipientProvince,recipientCity,recipientDistrict,tonnage,
		 volume, goodsName, selectCalcuteWay, distance,loadUnloadTemplate, invoiceWay, agingWay,sessionId,environment		 ):
	# 根据省市区名称获取对应的编号，如：330002
	senderAddress = senderProvince + '-' + handleCityName(senderCity,senderProvince) + '-' + senderDistrict
	print senderAddress
	senderAddressCode = database.getAddressCode(senderAddress,environment)
	start_province = senderAddressCode['provinceid']
	start_city = senderAddressCode['cityid']
	start_district = senderAddressCode['district']

	# 根据省市区名称获取对应的编号，如：330002
	recipientAddress = recipientProvince + '-' + handleCityName(recipientCity,recipientProvince) + '-' + recipientDistrict
	print senderAddress
	recipientAddressCode = database.getAddressCode(recipientAddress,environment)
	arrive_province = recipientAddressCode['provinceid']
	arrive_city = recipientAddressCode['cityid']
	arrive_district = recipientAddressCode['district']

	origin = manage_province_city_district.getLonAndLat(senderProvince, senderCity, senderDistrict)
	destination = manage_province_city_district.getLonAndLat(recipientProvince, recipientCity, recipientDistrict)
	result = calculate_price.getOneVehicleLinePrice(start_province, start_city, start_district, arrive_province,
													arrive_city, arrive_district,
													tonnage, volume, goodsName, selectCalcuteWay, distance,
													loadUnloadTemplate, invoiceWay, agingWay, origin, destination,sessionId,environment)
	if (result != ''):
		print"结果：%s"%result
	else:
		print"暂无估价"

#test('浙江省','金华市','兰溪市','浙江省','金华市','义乌市','5',
#		 '0', '纺织类', '整车线路', '80.251','一装一卸', '无需发票','12-24','201811199INnDXmzMduEjiL',"预发环境" )

#test('浙江省','金华市','兰溪市','河北省','衡水市','景县','12',
#		 '30', '面粉', '整车价格', '1198.559','一装一卸', '无需发票','42-48' )


