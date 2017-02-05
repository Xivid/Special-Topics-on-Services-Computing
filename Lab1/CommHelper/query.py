#-*- coding: utf-8 -*-
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import webbrowser, logging, platform
def GBK(s):
    if platform.system() == 'Windows':
        return s.decode('utf-8').encode('gbk')
    return s

def getLocation(phonenum):
    url = 'http://webservice.webxml.com.cn/WebServices/MobileCodeWS.asmx?wsdl'
    client = Client(url)
    result = client.service.getMobileCodeInfo(phonenum)
    if result[0] != '1':
    	print GBK("查无结果")
    	exit()
    result = result[12:].split(' ')[:2]
    province = result[0].encode("utf-8")
    city = result[1].encode("utf-8")
    return (province, city)

def getGuide(city):
    imp = Import('http://www.w3.org/2001/XMLSchema', location='http://www.w3.org/2001/XMLSchema.xsd')#导入
    imp.filter.add("http://WebXml.com.cn/")
    url = 'http://webservice.webxml.com.cn/WebServices/WeatherWebService.asmx?wsdl'
    d = ImportDoctor(imp)
    client = Client(url,doctor=d)
    return client.service.getWeatherbyCityName(city.decode('utf-8'))

def getZipCode(province, city):
    imp = Import('http://www.w3.org/2001/XMLSchema', location='http://www.w3.org/2001/XMLSchema.xsd')#导入
    imp.filter.add("http://WebXml.com.cn/")
    url = 'http://webservice.webxml.com.cn/WebServices/ChinaZipSearchWebService.asmx?wsdl'
    d = ImportDoctor(imp)
    client = Client(url,doctor=d)
    logging.getLogger('suds.umx.typed').setLevel(logging.ERROR)
    data = client.service.getZipCodeByAddress(province.decode('utf-8'), city.decode('utf-8'), u"", u"")
    if len(data) < 2:
        s = "Not found."
    else:
        s = '<ul>'
        for item in data[1][0][0]:
            s += '<li>' + item.ADDRESS.encode('utf-8') + ': ' + item.ZIP.encode('utf-8') + '</li>'
        s += '</ul>'
    return s

def WriteToFile(r):
    d = dict({'8.gif': '中雨',
    '30.gif': '扬沙',
    '21.gif': '小雨-中雨',
    '13.gif': '阵雪',
    '4.gif': '雷阵雨',
    '7.gif': '小雨',
    'nothing.gif': '没有数据(可自己更换)',
    '23.gif': '大雨-暴雨',
    '11.gif': '大暴雨',
    '10.gif': '暴雨',
    '27.gif': '中雪-大雪',
    '3.gif': '阵雨',
    '2.gif': '阴',
    '20.gif': '沙尘暴',
    '31.gif': '强沙尘暴',
    '5.gif': '雷阵雨并伴有冰雹',
    '22.gif': '中雨-大雨',
    '14.gif': '小雪',
    '6.gif': '雨加雪',
    '26.gif': '小雪-中雪',
    '9.gif': '大雨',
    '0.gif': '晴',
    '12.gif': '特大暴雨',
    '24.gif': '暴雨-大暴雨',
    '25.gif': '大暴雨-特大暴雨',
    '19.gif': '冻雨',
    '18.gif': '雾',
    '1.gif': '多云',
    '29.gif': '浮尘',
    '16.gif': '大雪',
    '15.gif': '中雪',
    '28.gif': '大雪-暴雪',
    '17.gif': '暴雪'})
    f = open("result.html", "w")
    f.write("""
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <style>
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    blockquote {
        margin: 0;
        padding: 0;
    }
    body {
        font-family: "Helvetica Neue", Helvetica, "Hiragino Sans GB", Arial, sans-serif;
        font-size: 13px;
        line-height: 18px;
        color: #737373;
        background-color: white;
        margin: 10px 13px 10px 13px;
    }
    table {
    	margin: 10px 0 15px 0;
    	border-collapse: collapse;
    }
    td,th {
    	border: 1px solid #ddd;
    	padding: 3px 10px;
    }
    th {
    	padding: 5px 10px;
    }

    a {
        color: #0069d6;
    }
    a:hover {
        color: #0050a3;
        text-decoration: none;
    }
    a img {
        border: none;
    }
    p {
        margin-bottom: 9px;
    }
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #404040;
        line-height: 36px;
    }
    h1 {
        margin-bottom: 18px;
        font-size: 30px;
    }
    h2 {
        font-size: 24px;
    }
    h3 {
        font-size: 18px;
    }
    h4 {
        font-size: 16px;
    }
    h5 {
        font-size: 14px;
    }
    h6 {
        font-size: 13px;
    }
    hr {
        margin: 0 0 19px;
        border: 0;
        border-bottom: 1px solid #ccc;
    }
    blockquote {
        padding: 13px 13px 21px 15px;
        margin-bottom: 18px;
        font-family:georgia,serif;
        font-style: italic;
    }
    blockquote:before {
        font-size:40px;
        margin-left:-10px;
        font-family:georgia,serif;
        color:#eee;
    }
    blockquote p {
        font-size: 14px;
        font-weight: 300;
        line-height: 18px;
        margin-bottom: 0;
        font-style: italic;
    }
    code, pre {
        font-family: Monaco, Andale Mono, Courier New, monospace;
    }
    code {
        background-color: #fee9cc;
        color: rgba(0, 0, 0, 0.75);
        padding: 1px 3px;
        font-size: 12px;
        -webkit-border-radius: 3px;
        -moz-border-radius: 3px;
        border-radius: 3px;
    }
    pre {
        display: block;
        padding: 14px;
        margin: 0 0 18px;
        line-height: 16px;
        font-size: 11px;
        border: 1px solid #d9d9d9;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    pre code {
        background-color: #fff;
        color:#737373;
        font-size: 11px;
        padding: 0;
    }
    sup {
        font-size: 0.83em;
        vertical-align: super;
        line-height: 0;
    }
    * {
    	-webkit-print-color-adjust: exact;
    }
    @media screen and (min-width: 914px) {
        body {
            width: 854px;
            margin:10px auto;
        }
    }
    @media print {
    	body,code,pre code,h1,h2,h3,h4,h5,h6 {
    		color: black;
    	}
    	table, pre {
    		page-break-inside: avoid;
    	}
    }
    </style>
    <title>查询结果</title>

    </head>
    <body>
    <h1>%s省%s地区生活指南</h1>

    <p><em>最后更新：%s</em></p>

    <h2>今日概况</h2>

    <h3>%s<!--概况--></h3>

    <ul>
    <li>气温：%s</li>
    <li>风向和风力：%s</li>
    <li>天气趋势：<img src="%s" alt="%s" />转<img src="%s" alt="%s" /></li>
    <li><!--天气实况-->%s</li>
    <li>生活指数：

    <blockquote><p>%s</p></blockquote></li>
    </ul>


    <h2>天气预报</h2>

    <h3>%s<!--第二天概况--></h3>

    <ul>
    <li>气温：%s</li>
    <li>风向和风力：%s</li>
    <li>天气趋势：<img src="%s" alt="%s" />转<img src="%s" alt="%s" /></li>
    </ul>


    <h3>%s<!--第三天概况--></h3>

    <ul>
    <li>气温：%s</li>
    <li>风向和风力：%s</li>
    <li>天气趋势：<img src="%s" alt="%s" />转<img src="%s" alt="%s" /></li>
    </ul>


    <h2>城市介绍</h2>

    <blockquote><p>%s</p></blockquote>

    <h2>邮政编码</h2>

    %s

    </body>
    </html>""" % (r[0], r[1], r[4], r[6], r[5], r[7], 'img/'+r[8], d[r[8]], 'img/'+r[9], d[r[9]], r[10], r[11], r[13], r[12], r[14], 'img/'+r[15], d[r[15]], 'img/'+r[16], d[r[16]], r[18], r[17], r[19], 'img/'+r[20], d[r[20]], 'img/'+r[21], d[r[21]], r[22], r[23]))

    f.close()
    print GBK("已将该地的生活指南保存在result.html中。")
    

location = getLocation(raw_input(GBK("请输入您的客户的手机号：")))
print GBK("您的客户来自"+location[0]+"省"+location[1]+"市。")
guide = getGuide(location[1])
zipcode = getZipCode(location[0], location[1])
result = [guide[0][i].encode('utf-8') for i in range(len(guide[0]))]
result.append(zipcode)
WriteToFile(result)
webbrowser.open("result.html")
