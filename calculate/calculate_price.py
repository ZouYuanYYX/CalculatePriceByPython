# -*- coding:UTF-8 -*-
__author__ = 'joy'
import sys
from common import one_vehicle_price_sum

reload(sys)
sys.setdefaultencoding('utf8')


#计算整车价格
#start_province指编号
#unloadWay装卸方式
#agingWay时效方式
#invoiceWay发票方式
def getOneVehicleLinePrice(start_province,start_city,start_district,arrive_province,arrive_city,arrive_district,
						   tonnage,cube,goodsName,selectCalcuteWay,distance,unloadWay,invoiceWay,agingWay,origin,destination,sessionId,environment):
	#总公式：(总价*优惠模板*时效系数+装卸费)*发票
	#总价*优惠模板*时效系数+装卸费
	cPrice = one_vehicle_price_sum.getVehicleSumPrice(tonnage,cube,start_province, start_city, start_district, arrive_province, arrive_city, arrive_district,goodsName,distance,
					   selectCalcuteWay, sessionId, environment,unloadWay, agingWay, origin, destination)

	#发票
	if (invoiceWay == "无需发票"):
		dPrice = cPrice
	if (invoiceWay == "10%发票") :
		dPrice = cPrice * 1.07
	return dPrice
