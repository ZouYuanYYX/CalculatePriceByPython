# -*- coding:UTF-8 -*-
__author__ = 'joy'
import pymysql

#连接数据库,dbName库名
def connectMySql(dbName,environment):
    #打开数据库连接
    if (environment == "205环境"):
        return pymysql.connect(host="192.168.158.206",
                           user="dbadmin",
                           passwd="hello1234",
                           db =dbName,
                           port=3307,
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor
                           )
    if (environment == "预发环境"):
        return pymysql.connect(host="192.168.13.24",
                           user="dbadmin",
                           passwd="hello1234",
                           db =dbName,
                           port=3307,
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor
                           )

#获取省市区的编码id,如：330700等
#参数address的格式为：河北省-沧州-吴桥县
def getAddressCode(address,environment):
    sql = "SELECT provinceid,cityid,IDCard FROM commonservice.`regions` WHERE spell = '"+address+"'"
    print sql
    result = executSqlFetchOne(sql,"commonservice",environment)
    print (result)
    addressCode = {"provinceid":result['provinceid'],"cityid":result['cityid'],"district":result['IDCard']}
    print (addressCode)
    return addressCode

#根据货物类型id获取整车线路模板数据
def  getGoodsTypeId(goodsName,environment):
    sql = "SELECT goods_type_id FROM carrier.`goods_name_template` WHERE goods_name = '" + goodsName + "'AND is_deleted = 0"
    result = executSqlFetchOne(sql,"carrier",environment)
    #商品类型找不到就去找商品不限
    print result
    if (result != None):
        print result['goods_type_id']
        sqlTwo = "SELECT id FROM carrier.`one_vehicle_line_price` WHERE goods_type_id = '"+result['goods_type_id']+"'AND is_deleted = 0"
        resultTwo = executSqlFetchOne(sqlTwo,"carrier",environment)
        if (resultTwo == None):
            return '0'
        return result['goods_type_id']
    else:
        return '0'


#再根据出发地、目的地的省市区编号获取唯一的整车线路模板数据
#再根据车型车长数据获取唯一的吨运价系数、方运价系数、基础价、优惠模板id、装卸模板id
#type:获取基础价信息、获取优惠模板信息、获取装卸模板信息
def  getOneVehicleRelationData(start_province,start_city,start_district,arrive_province,arrive_city,arrive_district,goodsTypeId,selectCalcuteWay,distance,type,environment):
    if (selectCalcuteWay == "整车线路"):
        if (type == "获取基础价信息") :
            sql = "SELECT car_type,car_length,ton_price_coefficient,cube_price_coefficient,base_price FROM carrier.`one_vehicle_relation` WHERE  is_deleted = 0 AND one_vehicle_id IN  (SELECT id FROM carrier.`one_vehicle_line_price` WHERE goods_type_id = '%s" %goodsTypeId +"' AND start_province ='%s" %start_province+"' AND start_city='%s" %start_city+"' AND start_district ='%s" %start_district+"' AND arrive_province ='%s" %arrive_province+"' AND arrive_city ='%s" %arrive_city+"' AND arrive_district = '%s" %arrive_district+ "'AND is_deleted = 0) "
        if (type == "获取优惠模板信息"):
            sql = "select price_coefficient,total_price_preferential,other_preferential,add_price from carrier.`preferential_template` where is_deleted = 0 AND id in (SELECT preferential_template_id FROM carrier.`one_vehicle_line_price` WHERE goods_type_id = '%s" %goodsTypeId +"' AND start_province ='%s" %start_province+"' AND start_city='%s" %start_city+"' AND start_district ='%s" %start_district+"' AND arrive_province ='%s" %arrive_province+"' AND arrive_city ='%s" %arrive_city+"' AND arrive_district = '%s" %arrive_district+ "'AND is_deleted = 0)"
        if (type == "获取装卸模板信息"):
            sql = "select one_load_one_unload,one_load_two_unload,one_load_three_unload,two_load_one_unload,two_load_two_unload from carrier.`load_unload_template` where is_deleted = 0 AND id in (SELECT load_unload_template_id FROM carrier.`one_vehicle_line_price` WHERE goods_type_id = '%s" %goodsTypeId +"' AND start_province ='%s" %start_province+"' AND start_city='%s" %start_city+"' AND start_district ='%s" %start_district+"' AND arrive_province ='%s" %arrive_province+"' AND arrive_city ='%s" %arrive_city+"' AND arrive_district = '%s" %arrive_district+ "'AND is_deleted = 0)"

    if (selectCalcuteWay == "整车价格"):
        realDistance = float(distance) * 1000
        if (type == "获取基础价信息"):
            sql = "SELECT car_type,car_length,ton_price_coefficient,cube_price_coefficient,base_price FROM carrier.`one_vehicle_relation` WHERE is_deleted = 0 AND one_vehicle_id IN  (SELECT id FROM carrier.`one_vehicle_price_template` WHERE  is_deleted = 0 AND goods_type_id = '"+goodsTypeId+"' AND %s"  %realDistance + "< distance_end  AND %s" %realDistance +" >= distance_start)"
        if (type == "获取优惠模板信息"):
            sql = "select price_coefficient,total_price_preferential,other_preferential,add_price from carrier.`preferential_template` where  is_deleted = 0 AND  id in (SELECT preferential_template_id FROM carrier.`one_vehicle_price_template` WHERE  is_deleted = 0 AND goods_type_id = '"+goodsTypeId+"' AND %s"  %realDistance + "< distance_end  AND %s" %realDistance +" >= distance_start)"
        if (type == "获取装卸模板信息"):
            sql = "select one_load_one_unload,one_load_two_unload,one_load_three_unload,two_load_one_unload,two_load_two_unload from carrier.`load_unload_template` where  is_deleted = 0 AND id in (SELECT load_unload_template_id FROM carrier.`one_vehicle_price_template` WHERE  is_deleted = 0 AND goods_type_id = '"+goodsTypeId+"' AND %s"  %realDistance + "< distance_end  AND %s" %realDistance +" >= distance_start)"
    result = executSqlFetchAll(sql, "carrier",environment)
    return result

def getVechileBasicPrice(distance,goodsTypeId,environment):
    realDistance = float(distance) * 1000
    sql = "SELECT base_price FROM carrier.`one_vehicle_price_template` WHERE  is_deleted = 0 AND goods_type_id = '" + goodsTypeId + "' AND %s" % realDistance + "< distance_end  AND %s" % realDistance + " >= distance_start"
    result = executSqlFetchOne(sql,"carrier",environment)
    return result

#获取时效数据
def getAgingConfigInfo(agingId,environment):
    sql = "SELECT standard_time,standard_coefficient,urgent_time,urgent_coefficient,common_time,common_coefficient FROM carrier.`aging_config_template` WHERE id = '"+agingId+"'AND  is_deleted = 0 "
    result = executSqlFetchOne(sql,"carrier",environment)
    print "时效%s"%result
    return result

#databaseName要连接的数据库名称
def executSqlFetchOne(sql,databaseName,environment):
    print sql
    db = connectMySql(databaseName,environment)
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    # 关闭数据库连接
    cursor.close()
    db.close()
    # result是一个list，list里面是dict字典,找不到数据则返回一个空元组
    print result
    return result

#databaseName要连接的数据库名称
def executSqlFetchAll(sql,databaseName,environment):
    print sql
    db = connectMySql(databaseName,environment)
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchall()
    # 关闭数据库连接
    cursor.close()
    db.close()
    # result是一个list，list里面是dict字典,找不到数据则返回一个空元组
    print result
    return result


#getGoodsTypeId('棉花')
#result = getOneVehicleRelationData('330000','330700','330781','330000','330700','330782','HPLX18112100028001A000')
#base_price = ''
#for r in result:
    #    print r.values()
    #if ((1 in r.values()) and (3 in r.values())):
    #   base_price = r['base_price']/100
    #   print base_price
#   break
#if (base_price == ''):
    #   for d in result:
    #   if ((d['car_length'] == 1) and (d['car_type'] == 1)):
    #       base_price = r['base_price']/100
    #       print base_price
#       break

#getAgingConfigInfo('SXPZ18112100042000A000')