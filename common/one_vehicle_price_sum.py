# -*- coding:UTF-8 -*-
__author__ = 'joy'
#整车总价计算,数量和方都按实际输入的来计算
#运输里程:transport_mileage
#吨位：tonnage
#基础运价：basicPrice_stop
import sys
import database
import prepare_data

reload(sys)
sys.setdefaultencoding('utf8')

#根据输入的运量获取基础价、吨运价系数、放运价系数
def getVehicleSumPrice(tonnage,cube,start_province, start_city, start_district, arrive_province, arrive_city, arrive_district,goodsName,distance,
					   selectCalcuteWay, sessionId, environment,unloadWay, agingWay, origin, destination):
	goodsTypeId = database.getGoodsTypeId(goodsName,environment)
	list = database.getOneVehicleRelationData(start_province, start_city, start_district, arrive_province, arrive_city, arrive_district,
							  goodsTypeId,selectCalcuteWay,distance,"获取基础价信息",environment)
	#车长
	carLengthInfo = prepare_data.getCarLengthByTonCube(tonnage,cube,sessionId)
	#车型
	carTypeInfo = prepare_data.getCarTypeByGoodsName(goodsTypeId,sessionId)

	#取基础价数据，车型车长都有则取对应系数，再考虑不限对应车长，最后考虑不限不限
	result = get_freight_rate_and_cube_rate(list, carLengthInfo, carTypeInfo)
	#基础价、吨运价系数、方运价系数
	basicPrice = result['basicPrice']
	freight_rate = result['freight_rate']
	cube_rate = result['cube_rate']
	flag = 0
	#当货品类型下面没有对应车型车长，也没有不限不限，则去商品不限里取数
	if (freight_rate == '' or cube_rate == ''):
		listAnything = database.getOneVehicleRelationData(start_province, start_city, start_district, arrive_province,
												  arrive_city, arrive_district,'0', selectCalcuteWay, distance, "获取基础价信息", environment)
		result = get_freight_rate_and_cube_rate(listAnything, carLengthInfo, carTypeInfo)
		# 基础价、吨运价系数、方运价系数
		basicPrice = result['basicPrice']
		freight_rate = result['freight_rate']
		cube_rate = result['cube_rate']
		#该标表示从商品不限处取的数据
		flag = 1
	#总价
	sumPrice = calculateSumPrice(basicPrice, tonnage, distance, freight_rate, cube, cube_rate, selectCalcuteWay,goodsTypeId,environment,flag)
	# 总价*优惠模板
	aPrice = getPreferentialTemplatePrice(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,goodsName,environment,sumPrice,selectCalcuteWay, distance,flag)
	# 总价*优惠模板*时效系数
	bPrice = getAgingPrice(origin, destination, sessionId,environment,agingWay,aPrice)
	#总价*优惠模板*时效系数+装卸模板
	cPrice = getLoadUnloadTemplatePrice(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,goodsTypeId, selectCalcuteWay, distance,environment,unloadWay,bPrice,flag)

	print "freight_rate:%s"%freight_rate
	print "flag:%s"%flag
	print "sumPrice:%s"%sumPrice
	print "sumPrice*youhui:%s" % aPrice
	print "sumPrice*youhui*aging:%s" % bPrice
	print "sumPrice*youhui*aging+load_unload:%s" % cPrice

	return cPrice

#总价*优惠模板
#flag表示从商品不限处获取优惠模板数据
def getPreferentialTemplatePrice(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,goodsName,environment,sumPrice,selectCalcuteWay, distance,flag):
	# 获取优惠模板数据
	goodsTypeId = database.getGoodsTypeId(goodsName, environment)
	if (flag == 1):
		preferentialTemplateData = database.getOneVehicleRelationData(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,
																	  '0', selectCalcuteWay, distance,"获取优惠模板信息", environment)
	else:
		preferentialTemplateData = database.getOneVehicleRelationData(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,
																  goodsTypeId, selectCalcuteWay, distance, "获取优惠模板信息",environment)
	'''总价*优惠模板'''
	if (preferentialTemplateData.__len__() > 0):
		aPrice = float(sumPrice) * float(preferentialTemplateData[0]['price_coefficient']) - (
			float(preferentialTemplateData[0]['total_price_preferential'])) / 100 - (
					 float(preferentialTemplateData[0]['other_preferential'])) / 100 + (
					 float(preferentialTemplateData[0]['add_price'])) / 100
	else:
		aPrice = sumPrice
	return 	aPrice

#总价*优惠模板*时效系数
#flag表示从商品不限处获取优惠模板数据
def getAgingPrice(origin, destination, sessionId,environment,agingWay,aPrice):
	# 获取时效系数
	agingInfoId = prepare_data.getAgingConfigInfo(origin, destination, sessionId)['id']
	agingInfo = database.getAgingConfigInfo(agingInfoId, environment)
	print agingInfo
	if (agingWay == agingInfo['urgent_time']):
		agingValue = agingInfo['urgent_coefficient']
	elif (agingWay == agingInfo['common_time']):
		agingValue = agingInfo['common_coefficient']
	elif (agingWay == agingInfo['standard_time']):
		agingValue = agingInfo['standard_coefficient']
	'''总价*优惠模板*时效系数'''
	bPrice = aPrice * float(agingValue)
	return bPrice

#总价*优惠模板*时效系数+装卸模板
def getLoadUnloadTemplatePrice(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,
																goodsTypeId, selectCalcuteWay, distance,environment,unloadWay,bPrice,flag):
	# 获取装卸模板数据
	if (flag == 1):
		loadUnloadTemplateData = database.getOneVehicleRelationData(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,
																	'0', selectCalcuteWay, distance, "获取装卸模板信息",environment)
	else:
		loadUnloadTemplateData = database.getOneVehicleRelationData(start_province, start_city, start_district,arrive_province, arrive_city, arrive_district,
																goodsTypeId, selectCalcuteWay, distance, "获取装卸模板信息",environment)

	if (loadUnloadTemplateData.__len__() > 0):
		'''总价*优惠模板*时效系数+装卸费'''
		if (unloadWay == "一装一卸"):
			cPrice = bPrice + float(loadUnloadTemplateData[0]['one_load_one_unload']) / 100
		elif (unloadWay == "一装二卸"):
			cPrice = bPrice + float(loadUnloadTemplateData[0]['one_load_two_unload']) / 100
		elif (unloadWay == "一装三卸"):
			cPrice = bPrice + float(loadUnloadTemplateData[0]['one_load_three_unload']) / 100
		elif (unloadWay == "二装一卸"):
			cPrice = bPrice + float(loadUnloadTemplateData[0]['two_load_one_unload']) / 100
		elif (unloadWay == "二装二卸"):
			cPrice = bPrice + float(loadUnloadTemplateData[0]['two_load_two_unload']) / 100
	else:
		cPrice = bPrice
	return 	cPrice


#总价计算公式
def calculateSumPrice(basicPrice,tonnage,distance,freight_rate,cube,cube_rate,selectCalcuteWay,goodsTypeId,environment,flag) :

	if (selectCalcuteWay == "整车价格"):
		if (flag == 1):
			basicPrice = database.getVechileBasicPrice(distance, '0', environment)['base_price']
		else:
			basicPrice = database.getVechileBasicPrice(distance,goodsTypeId,environment)['base_price']
		#配置了基础运价
		if ( basicPrice != '' and basicPrice != None) :
			basicPrice = float(basicPrice)/100
			ton_price = float(basicPrice) + float(tonnage) * float(distance) * float(freight_rate)
			cube_price = float(basicPrice) + float(cube) * float(distance) * float(cube_rate)
		else:#没有配置基础运价
			if ( (freight_rate) == ''or ((cube_rate) == '') ):
				ton_price = 0
				cube_price = 0
			else:
				ton_price = float(distance) + float(tonnage) * float(distance) * float(freight_rate)
				cube_price = float(distance) + float(cube) * float(distance) * float(cube_rate)


	if (selectCalcuteWay == "整车线路"):
		#1表示用不限不限计算
		# if (flag == 1):
			if ((freight_rate) == '' or ((cube_rate) == '') or ((basicPrice) == '')):
				ton_price = 0
				cube_price = 0
			else:
				ton_price = float(basicPrice) + float(tonnage) * float(distance) * float(freight_rate)
				cube_price = float(basicPrice) + float(cube) * float(distance) * float(cube_rate)
		# #车长有实际值，则方运量不参与计算
		# else:
		# 	if ((freight_rate) == '' or ((cube_rate) == '') or ((basicPrice) == '')):
		# 		ton_price = 0
		# 		cube_price = 0
		# 	else:
		# 		ton_price = float(basicPrice) + float(tonnage) * float(distance) * float(freight_rate)
		# 		cube_price = 0

	return comparePrice(ton_price,cube_price)


def comparePrice(ton_price,cube_price) :
	if (ton_price >= cube_price) :
		return ton_price
	if (ton_price < cube_price) :
		return cube_price

#取基础价数据，车型车长都有则取对应系数，再考虑不限对应车长，最后考虑不限不限
def get_freight_rate_and_cube_rate(list,carLengthInfo,carTypeInfo):
	#基础价、吨运价系数、方运价系数
	basicPrice = ''
	freight_rate = ''
	cube_rate = ''
	for d in list :
		if ( (carLengthInfo == d['car_length']) and (carTypeInfo == d['car_type']) ) :
			if (d['base_price'] != None):
				basicPrice = d['base_price'] / 100
			freight_rate = d['ton_price_coefficient']
			cube_rate = d['cube_price_coefficient']
			break
	if (basicPrice == '' or freight_rate == '' or cube_rate == '') :
		for d in list:
			if ((carLengthInfo == d['car_length']) and (d['car_type'] == 1) ):
				if (d['base_price'] != None):
					basicPrice = d['base_price']/100
				freight_rate = d['ton_price_coefficient']
				cube_rate = d['cube_price_coefficient']
				break
	#取不限不限数据来计算
	if (basicPrice == '' or freight_rate == '' or cube_rate == ''):
		for d in list:
			if ((d['car_length'] == 1) and (d['car_type'] == 1) ):
				if (d['base_price'] != None):
					basicPrice = d['base_price']/100
				freight_rate = d['ton_price_coefficient']
				cube_rate = d['cube_price_coefficient']
				break
	result = {'basicPrice':basicPrice,'freight_rate':freight_rate,'cube_rate':cube_rate}
	return result

