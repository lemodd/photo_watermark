import urllib.request
import json
import piexif

def getlocation(lat,lng):
    '''
    根据经纬度，转换为地点
    lat:纬度，字符串
    lng:经度，字符串
    '''
    #31.809928, 102.537467, 3019.300
    #lat = '31.809928'
    #lng = '102.537467'

    url = 'http://api.map.baidu.com/geocoder/v2/?location=' + lat + ',' + lng + '&output=json&pois=1&ak=ok5FRlZKYuTOWq3aDzCDgwidTPKwonoG'
    req = urllib.request.urlopen(url)  # json格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    res_jsn = json.loads(res)

     #get()获取json里面的数据
    jsonResult = res_jsn.get('result')
    address = jsonResult.get('addressComponent')
    #国家
    country = address.get('country')
    #国家编号（0：中国）
    country_code = address.get('country_code')
    #省
    province = address.get('province')
    #城市
    city = address.get('city')
    #城市等级
    city_level = address.get('city_level')
    #县级
    district = address.get('district')
    

    return "".join([province,city,district])

def get_photo_addr_date(imgf):
    '''
    获取照片的地址
    imgf:照片文件路径
    '''
    try:
        exif_dict = piexif.load(imgf)
        #['0th', 'Exif', 'GPS', 'Interop', '1st', 'thumbnail']
    except:
        return '',''
    
    gps_raw = exif_dict["GPS"]

    #如果有gps信息
    if gps_raw != {}:
        
        #纬度：度分秒
        gps_lat = gps_raw[2]
        #度 分 秒 转为度保留6位小数
        du = gps_lat[0][0]/gps_lat[0][1]
        fen = gps_lat[1][0]/gps_lat[1][1]
        miao = gps_lat[2][0]/gps_lat[2][1]

        #纬度
        lat = str(du + (miao/60+fen)/60)

        #经度：度分秒
        gps_long = gps_raw[4]

        #度 分 秒 转为度保留6位小数
        du = gps_long[0][0]/gps_long[0][1]
        fen = gps_long[1][0]/gps_long[1][1]
        miao = gps_long[2][0]/gps_long[2][1]
        #经度
        lng = str(du + (miao/60+fen)/60)

        #地址：省，市，县（区）
        addr = getlocation(lat,lng)
        
    #如果没有gps信息，返回空值
    else:
        addr = ''


    #获取拍照时间
    exif = exif_dict["Exif"]
    if exif:
        date = exif_dict["Exif"][36867].decode('utf-8')
    else:
        date = ''
        
    return addr,date


if __name__ == "__main__":
##    res = getlocation('31.809928','102.537467')

    imgfile = 'p.jpg'
    addr,date  = get_photo_addr_date(imgfile)
   
    print(addr,date)
