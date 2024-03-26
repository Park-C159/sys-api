from sqlalchemy import and_, extract, desc, asc
from sqlalchemy.inspection import inspect
import random
import threading
from datetime import datetime

import time

from model import sqlutl

from flask import Flask, make_response, request, jsonify, url_for, redirect, render_template
from flask_cors import CORS  # 引用CORS，后期需要VUE支持跨域访问会用到
from flask_sqlalchemy import SQLAlchemy

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_BINDS

from model.message import *

# from model.utils import *

errObj = {
    'code': 500,
    'msg': "对不起服务器开小差了，请稍后再试..."
}

# Flask类只有一个必须指定的参数，即程序主模块或者包的名字，__name__是系统变量，该变量指的是本py文件的文件名
app = Flask(__name__, static_folder='uploads')
# resources全局配置允许跨域的API接口，我们这边为了学习，配置所有，详细学习请百度搜索文档
CORS(app, resources=r'/*')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS

db = SQLAlchemy(app)


class Data(db.Model):
    __bind_key__ = 'db2'  # 已设置__bind_key__ 数据库名
    __tablename__ = 'fitting2023331'  # 气象数据表格的表名

    date = db.Column(db.String(10), primary_key=True)
    time = db.Column(db.String(8), primary_key=True)
    ourdoor_temperature = db.Column(db.Float, nullable=False)
    ourdoor_humidity = db.Column(db.Float, nullable=False)
    ourdoor_radiation = db.Column(db.Float, nullable=False)
    indoor_temperature = db.Column(db.Float, nullable=False)
    indoor_humidity = db.Column(db.Float, nullable=False)
    indoor_radiation = db.Column(db.Float, nullable=False)
    air_cond_temp = db.Column(db.Integer, nullable=False)
    air_cond_switch = db.Column(db.Boolean, nullable=False)
    spray_switch = db.Column(db.Boolean, nullable=False)
    window_switch = db.Column(db.Boolean, nullable=False)

    def jsonformat(self):
        return {
            'date': self.date,
            'time': self.time,
            'ourdoor_temperature': self.ourdoor_temperature,
            'ourdoor_humidity': self.ourdoor_humidity,
            'ourdoor_radiation': self.ourdoor_radiation,
            'indoor_temperature': self.indoor_temperature,
            'indoor_humidity': self.indoor_humidity,
            'indoor_radiation': self.indoor_radiation,
            'air_cond_temp': self.air_cond_temp,
            'air_cond_switch': self.air_cond_switch,
            'spray_switch': self.spray_switch,
            'window_switch': self.window_switch
        }


class FittingData(db.Model):
    __tablename__ = 'fitting_data'  # 根据实际表名调整

    datetime = db.Column(db.DateTime, primary_key=True)
    ourdoor_temperature = db.Column(db.Float, nullable=False)
    ourdoor_humidity = db.Column(db.Float, nullable=False)
    ourdoor_radiation = db.Column(db.Float, nullable=False)
    indoor_temperature = db.Column(db.Float, nullable=False)
    indoor_humidity = db.Column(db.Float, nullable=False)
    indoor_radiation = db.Column(db.Float, nullable=False)
    air_cond_temp = db.Column(db.Integer, nullable=False)
    air_cond_switch = db.Column(db.Boolean, nullable=False)
    spray_switch = db.Column(db.Boolean, nullable=False)
    window_switch = db.Column(db.Boolean, nullable=False)

    def jsonformat(self):
        return {
            'datetime': self.datetime,
            'ourdoor_temperature': self.ourdoor_temperature,
            'ourdoor_humidity': self.ourdoor_humidity,
            'ourdoor_radiation': self.ourdoor_radiation,
            'indoor_temperature': self.indoor_temperature,
            'indoor_humidity': self.indoor_humidity,
            'indoor_radiation': self.indoor_radiation,
            'air_cond_temp': self.air_cond_temp,
            'air_cond_switch': self.air_cond_switch,
            'spray_switch': self.spray_switch,
            'window_switch': self.window_switch
        }


class User(db.Model):
    # 使用默认数据库，不需要像下面指定__bind_key__
    __tablename__ = 'users'  # 表名

    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    upwd = db.Column(db.String(10), nullable=False)
    uavatar = db.Column(db.String(500))
    uphone = db.Column(db.String(20))
    sex = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    umail = db.Column(db.String(20))
    uidcard = db.Column(db.String(20))
    unickname = db.Column(db.String(255))
    uinfo = db.Column(db.Text)

    def regist(self):
        return {
            "uname": self.uname,
            "uphone": self.uphone,
            "uidcard": self.uidcard
        }

    def jsonformat(self):
        return {
            "uid": self.uid,
            "uname": self.uname,
            "upwd": self.upwd,
            "uavatar": self.uavatar,
            "uphone": self.uphone,
            "sex": self.sex,
            "birthday": self.birthday,
            "umail": self.umail,
            "uidcard": self.uidcard,
            "unickname": self.unickname,
            "uinfo": self.uinfo
        }


class MonitorParam(db.Model):
    __bind_key__ = 'param'  # 已设置__bind_key__ 数据库名
    __tablename__ = 'tb_monitor_param'  # 表名

    monitor_no = db.Column(db.String(32))
    # monitor_no = db.Column(db.String(32), primary_key=True)
    create_time = db.Column(db.DateTime)
    air_temperture = db.Column(db.Float)
    air_humidity = db.Column(db.Float)
    soil_temperture10 = db.Column(db.Float)
    soil_temperture20 = db.Column(db.Float)
    soil_temperture30 = db.Column(db.Float)
    soil_temperture40 = db.Column(db.Float)
    soil_temperture50 = db.Column(db.Float)
    soil_humidity10 = db.Column(db.Float)
    soil_humidity20 = db.Column(db.Float)
    soil_humidity30 = db.Column(db.Float)
    soil_humidity40 = db.Column(db.Float)
    soil_humidity50 = db.Column(db.Float)
    Ph = db.Column(db.Float)
    co2 = db.Column(db.Float)
    light_intencity = db.Column(db.Float)
    electrical_conductivity = db.Column(db.Float)
    battery_voltage = db.Column(db.Float)
    mainboard_temperture = db.Column(db.Float)
    wind_direction = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    rain_fall = db.Column(db.Float)
    air_pressure = db.Column(db.Float)

    __mapper_args__ = {
        'primary_key': [monitor_no, create_time]
    }

    def jsonformat(self):
        return {
            "monitor_no": self.monitor_no,
            "create_time": self.create_time,
            "air_temperture": self.air_temperture,
            "air_humidity": self.air_humidity,
            "soil_temperture10": self.soil_temperture10,
            "soil_temperture20": self.soil_temperture20,
            "soil_temperture30": self.soil_temperture30,
            "soil_temperture40": self.soil_temperture40,
            "soil_temperture50": self.soil_temperture50,
            "soil_humidity10": self.soil_humidity10,
            "soil_humidity20": self.soil_humidity20,
            "soil_humidity30": self.soil_humidity30,
            "soil_humidity40": self.soil_humidity40,
            "soil_humidity50": self.soil_humidity50,
            "Ph": self.Ph,
            "co2": self.co2,
            "light_intencity": self.light_intencity,
            "electrical_conductivity": self.electrical_conductivity,
            "battery_voltage": self.battery_voltage,
            "mainboard_temperture": self.mainboard_temperture,
            "wind_direction": self.wind_direction,
            "wind_speed": self.wind_speed,
            "rain_fall": self.rain_fall,
            "air_pressure": self.air_pressure
        }


class Warn(db.Model):
    __tablename__ = 'warning'  # 表名

    wid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(127), default=None)
    value = db.Column(db.Float, default=None)
    rx = db.Column(db.String(127), default=None)
    wtime = db.Column(db.DateTime, default=None)

    def jsonformat(self):
        return {
            "id": self.wid,
            "content": self.content,
            "value": self.value,
            "rx": self.rx,
            "wtime": self.wtime

        }


class Manage(db.Model):
    # 使用默认数据库，不需要像下面指定__bind_key__
    __tablename__ = 'manage'  # 表名

    mid = db.Column(db.Integer, primary_key=True)
    mtime = db.Column(db.DateTime)
    mdose = db.Column(db.String(100))
    mclass = db.Column(db.Integer)
    minfo = db.Column(db.String)

    def jsonformat(self):
        return {
            "mid": self.mid,
            "minfo": self.minfo,
            "mdose": self.mdose,
            "mtime": self.mtime,
            "mclass": self.mclass
        }


def generate_table_names(start_date, end_date):
    # 解析输入日期
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # 生成序列
    current = start
    table_names = []
    while current <= end:
        table_name = f"fitting{current.year}{current.month}{current.day}"
        table_names.append(table_name)
        current += timedelta(days=1)  # 增加一天

    return table_names


def query_to_dict(query_result):
    if not query_result:
        return {}

    columns = [c.key for c in inspect(FittingData).attrs]
    data_dict = {column: [] for column in columns}

    for record in query_result:
        for column in columns:
            value = getattr(record, column)
            # 检查值是否为 datetime 类型，如果是，将其转换为字符串
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            data_dict[column].append(value)

    return data_dict


def getLatestData():
    num1 = random.uniform(19, 36)
    num2 = random.uniform(0.34, 0.56)
    num3 = random.uniform(29000, 50101)

    return num1, num2, num3


UP_LIMIT_TEMPERATURE = 35
DOWN_LIMIT_TEMPERATURE = 20

UP_LIMIT_HUMIDITY = 0.55
DOWN_LIMIT_HUMIDITY = 0.35

UP_LIMIT_LIGHT = 50000
DOWN_LIMIT_LIGHT = 30000


def isWarning(phone):
    # with app.app_context():

        # while True:
    temperature, humidity, light = getLatestData()
    temperatureInfo = humidityInfo = lightInfo = None

    if temperature < DOWN_LIMIT_TEMPERATURE:
        temperatureInfo = "温度报警"
        rx = "-{:.2f}℃".format(DOWN_LIMIT_TEMPERATURE - temperature)
        Temperture.send_temperature_warning(phone, "{:.2f}".format(temperature), "-{:.2f}".format(DOWN_LIMIT_TEMPERATURE - temperature))
        save_warning(temperatureInfo, temperature, rx)
    elif temperature > UP_LIMIT_TEMPERATURE:
        temperatureInfo = "温度报警"
        rx = "+{:.2f}℃".format(temperature - UP_LIMIT_TEMPERATURE)
        Temperture.send_temperature_warning(phone, "{:.2f}".format(temperature), "+{:.2f}".format(temperature - UP_LIMIT_TEMPERATURE))
        save_warning(temperatureInfo, temperature, rx)

    if humidity < DOWN_LIMIT_HUMIDITY:
        humidityInfo = "湿度报警"
        rx = "-{:.2f}%RH".format((DOWN_LIMIT_HUMIDITY - humidity) * 100)
        Humidity.send_humidity_warning(phone, "{:.2f}".format(humidity * 100), "-{:.2f}".format((DOWN_LIMIT_HUMIDITY - humidity) * 100))
        save_warning(humidityInfo, humidity, rx)
    elif humidity > UP_LIMIT_HUMIDITY:
        humidityInfo = "湿度报警"
        value = humidity
        rx = "+{:.2f}%RH".format((value - UP_LIMIT_HUMIDITY) * 100)
        Humidity.send_humidity_warning(phone, "{:.2f}".format(humidity * 100), "+{:.2f}".format((value - UP_LIMIT_HUMIDITY) * 100))
        save_warning(humidityInfo, value, rx)

    if light < DOWN_LIMIT_LIGHT:
        lightInfo = "光照报警"
        rx = "-{:.2f}lx".format(DOWN_LIMIT_LIGHT - light)
        Light.send_light_warning(phone, "{:.2f}".format(light), "-{:.2f}".format(DOWN_LIMIT_LIGHT - light))
        save_warning(lightInfo, light, rx)
        
    elif light > UP_LIMIT_LIGHT:
        lightInfo = "光照报警"
        rx = "+{:.2f}lx".format(light - UP_LIMIT_LIGHT)
        Light.send_light_warning(phone, "{:.2f}".format(light), "+{:.2f}".format(light - UP_LIMIT_LIGHT))
        save_warning(lightInfo, light, rx)

    # 打印警告信息，如果某个指标正常则不打印
    warnings = [info for info in [temperatureInfo, humidityInfo, lightInfo] if info is not None]
    # print(", ".join(warnings) if warnings else "所有指标正常")
    if warnings:
        warning_content = ", ".join(warnings)
        print(warning_content)
        return True
    else:
        print("所有指标正常")
        return False
            # time.sleep(60)


def save_warning(content, value=0, rx=""):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_warning = Warn(content=content, wtime=current_time, value=value, rx=rx)
    db.session.add(new_warning)
    db.session.commit()


@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == "GET":
        result = FittingData.query.order_by(asc(FittingData.datetime)).all()
        # data = [row.jsonformat() for row in result]

        step = 60
        needNum = 23
        start = max(0, len(result) - needNum * step - 1)
        sliced_data = result[start::step]
        res = {
            "code": 200,
            "msg": "OK",
            "data": query_to_dict(sliced_data)
        }

        return res
    elif request.method == "POST":
        params = request.json

        start_time = params.get("start")
        end_time = params.get("end")

        result = FittingData.query.filter(
            and_(FittingData.datetime >= start_time, FittingData.datetime <= end_time)).order_by(
            asc(FittingData.datetime)).all()

        res = {
            "code": 200,
            "msg": "请求成功！",
            "data": query_to_dict(result)
        }

        return res

    return {"code": 400, "msg": "无效的参数"}


@app.route('/', methods=['GET'])
def run():
    start_date = "2023-03-01"
    end_date = "2023-03-31"
    table_names = generate_table_names(start_date, end_date)
    # print(table_names)
    # table_names = ['fitting202331', 'fitting202332']  # 指定的表名列表
    union_query = " UNION ".join([f"SELECT * FROM {name}" for name in table_names])

    # 使用 db.engines 获取与特定绑定相关的引擎
    db2_engine = db.engines['db2']

    with db2_engine.connect() as connection:
        executable_query = text(union_query)
        result_proxy = connection.execute(executable_query)
        columns = result_proxy.keys()  # 获取列名
        data = [dict(zip(columns, row)) for row in result_proxy]

        # 将数据插入到主数据库
    for row in data:
        # 合并date和time字段为datetime
        date_str = row['date']
        time_str = row['time']

        # 修改日期时间字符串的格式
        datetime_str = f"{date_str.replace('/', '-')} {time_str}"

        # 解析为datetime
        row['datetime'] = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        # 移除原始的date和time字段
        del row['date']
        del row['time']

        new_entry = FittingData(**row)  # 创建模型实例，假设字段匹配
        db.session.add(new_entry)
    db.session.commit()

    return jsonify(data)


@app.route('/api/mod', methods=['GET', 'POST'])
def mod():
    if request.method == 'POST':
        res = {}
        r = request.json

        u = User.query.filter(
            and_(User.uname == r.get("uname"), User.upwd == r.get("upwd"), User.uphone == r.get("uphone"))).all()

        data = []

        for row in u:
            data.append(row.regist())
        if len(data) == 0:
            res = {
                'code': 300,
                'msg': "原密码输入错误，或用户名不存在！"
            }
        elif len(data) == 1:
            try:
                User.query.filter(User.uname == r.get("uname")).update({'upwd': r.get("npwd")})
                db.session.commit()
                res = {
                    'code': 200,
                    'msg': "恭喜您修改成功！"
                }
            except:
                res = errObj
        else:
            res = {
                "code": 301,
                "msg": "该用户不可更改"
            }


    else:
        res = "get/resgist"
    return make_response(res)


@app.route('/api/regist', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        res = {}
        r = request.json
        from sqlalchemy import or_
        u = User.query.filter(
            or_(User.uname == r.get("uname"), User.uidcard == r.get("uidcard"), User.uphone == r.get("uphone"))).all()

        data = []
        for row in u:
            data.append(row.regist())
        for i in data:
            jiao = i.items() & r.items()
            for j in jiao:
                if (j[0] == 'uname'):
                    res = {
                        'code': 300,
                        'msg': "用户名已经被占用"
                    }
                    break
                elif (j[0] == 'uidcard'):
                    res = {
                        'code': 300,
                        'msg': "身份证已经被使用"
                    }
                    break
                elif (j[0] == 'uphone'):
                    res = {
                        'code': 300,
                        'msg': "电话已经被占用"
                    }
                    break
                else:
                    res = errObj
        if (res == {}):
            user = User(uname=r.get("uname"), upwd=r.get("upwd"), uphone=r.get("uphone"), uidcard=r.get("uidcard"),
                        uavatar="", sex=0, umail="", birthday="2022-1-14")
            # sql2 = "insert into users(uname, uphone, upwd, uidcard) values(%s,%s,%s,%s)"
            # values = (r.get("uname"), r.get("uphone"), r.get("upwd"), r.get("uid"))
            try:
                # c = sql2 % values
                db.session.add(user)
                db.session.commit()
                res = {
                    'code': 200,
                    'msg': "注册成功！"
                }

            except:
                res = errObj

    else:
        res = "get/resgist"
    return make_response(res)


@app.route('/api/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        res = {}
        r = request.json
        try:
            u = User.query.filter(
                and_(User.uname == r.get("uname"), User.uidcard == r.get("uidcard"),
                     User.uphone == r.get("uphone"))).all()
            data = []
            for row in u:
                data.append(row.jsonformat())
            res = {
                'code': 200,
                'msg': "注册成功！",
                'data': data[0].get("upwd"),
            }
        except:
            res = errObj

    else:
        res = "get/resgist"
    return make_response(res)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = {}
        r = request.json

        u = User.query.filter(
            and_(User.uname == r.get("uname"), User.upwd == r.get("upwd"))).all()
        data = []

        for row in u:
            data.append(row.jsonformat())
        # sql1 = "select * from users where uname = '" + r.get("uname") + "' and  upwd = '" + r.get("upwd") + "';"

        # data = sqlutl.sqlGet(db, sql1)
        if (data != []):
            res = {
                'code': 200,
                'data': data,
                'msg': "恭喜你，登录成功！"
            }
        elif (data == []):
            res = {
                'code': 300,
                'msg': "对不起，未查询到您的信息，请先注册！"
            }
        else:
            res = {
                'code': 500,
                'msg': "对不起，服务器错误。"
            }
    else:
        res = "get/login"
    return res


@app.route('/api/sendmessage', methods=['GET', 'POST'])
def sendMessage():
    if request.method == 'POST':
        params = request.json
        phone = params.get("phone")
        random_num = random.randint(1000, 9999)
        # 转化为字符串
        verification_code = str(random_num)
        success = IdentifyCode.send_verification_code(phone, verification_code)

        if success:
            print('发送成功' if success else '发送失败')
            res = {
                "code": 200,
                "msg": "发送成功",
                "data": verification_code
            }
    elif request.method == 'GET':
        # 生成四位数随机数
        random_number = random.randint(1000, 9999)

        # 转化为字符串
        verification_code = str(random_number)
        success = IdentifyCode.send_verification_code("15212371894", verification_code)
        if success:
            print('发送成功' if success else '发送失败')
            res = {
                "code": 200,
                "msg": "发送成功",
                "data": verification_code
            }
    return res


@app.route('/api/environment', methods=['GET', 'POST'])
def environment():
    try:
        result = MonitorParam.query.filter(MonitorParam.monitor_no == "8dfeaf752b4d40b4a23819478c90f9ae").order_by(
            MonitorParam.create_time.desc()).limit(1).all()
        # result = MonitorParam.query.filter(MonitorParam.monitor_no == "8dfeaf752b4d40b4a23819478c90f9ae").limit(1).all()

        data = []
        for row in result:
            data.append(row.jsonformat())
        res = {
            "code": 200,
            "msg": "OK",
            "data": data
        }
    except:
        res = errObj

    return res


@app.route('/api/hours', methods=['GET', 'POST'])
def hours():
    result = MonitorParam.query.filter(MonitorParam.monitor_no == "8dfeaf752b4d40b4a23819478c90f9ae",
                                       extract('minute', MonitorParam.create_time) == 0).order_by(
        MonitorParam.create_time.desc()).limit(48).all()
    result2 = MonitorParam.query.filter(MonitorParam.monitor_no == "80280c443ed84233bb9acbbfd7a59ed4",
                                        extract('minute', MonitorParam.create_time) == 0).order_by(
        MonitorParam.create_time.desc()).limit(48).all()
    # print(result)
    data = []
    for row in result:
        data.append(row.jsonformat())
    for row in result2:
        data.append(row.jsonformat())

    res = {
        "code": 200,
        "msg": "OK",
        "data": data
    }

    return res


@app.route('/api/minutes', methods=['GET', 'POST'])
def minutes():
    # result = MonitorParam.query.all()
    # print(result)
    # result = db.session.query.all()
    # print(result)
    # print(MonitorParam.create_time)
    result = MonitorParam.query.filter(MonitorParam.monitor_no == "8dfeaf752b4d40b4a23819478c90f9ae").order_by(
        MonitorParam.create_time.desc()).limit(120).all()
    result2 = MonitorParam.query.filter(MonitorParam.monitor_no == "80280c443ed84233bb9acbbfd7a59ed4").order_by(
        MonitorParam.create_time.desc()).limit(120).all()
    # print(result)
    data = []
    for row in result:
        data.append(row.jsonformat())
    for row in result2:
        data.append(row.jsonformat())

    res = {
        "code": 200,
        "msg": "OK",
        "data": data
    }

    return res


@app.route('/api/days', methods=['GET', 'POST'])
def days():
    result = MonitorParam.query.filter(MonitorParam.monitor_no == "8dfeaf752b4d40b4a23819478c90f9ae",
                                       extract('hour', MonitorParam.create_time) == 12,
                                       extract('minute', MonitorParam.create_time) == 0).order_by(
        MonitorParam.create_time.desc()).limit(30).all()
    result2 = MonitorParam.query.filter(MonitorParam.monitor_no == "80280c443ed84233bb9acbbfd7a59ed4",
                                        extract('hour', MonitorParam.create_time) == 12,
                                        extract('minute', MonitorParam.create_time) == 0).order_by(
        MonitorParam.create_time.desc()).limit(30).all()
    # print(result)
    data = []
    for row in result:
        data.append(row.jsonformat())
    for row in result2:
        data.append(row.jsonformat())

    res = {
        "code": 200,
        "msg": "OK",
        "data": data
    }

    return res


@app.route('/api/warning/<string:phone>', methods=['GET', 'POST'])
def warning(phone=""):
    if request.method == 'GET':
        if phone!="":
        # thread = threading.Thread(target=isWarning, args=(app,))
        # thread.start()
            isWarn = isWarning(phone)
        # temperature, humidity, light = getLatestData()
        # print(temperature, humidity, light)

            result = Warn.query.order_by(Warn.wid.desc()).limit(100).all()
            data = []
            for row in result:
                # 将时间戳转换为datetime对象
                # wtime_datetime = datetime.fromtimestamp(row.wtime)
                # 将datetime对象格式化为字符串
                wtime_str = row.wtime.strftime('%Y-%m-%d %H:%M:%S')
                row_dict = row.jsonformat()
                row_dict["wtime"] = wtime_str
                data.append(row_dict)

            res = {
                "code": 200,
                "msg": "OK",
                "data": data,
                "isWarning": isWarn
            }
        else:
            res = {
                "code":201,
                "msg":"請求失敗，請聯係管理員",
                "data":""
            }

        return res


@app.route('/api/manage', methods=['GET', 'POST'])
@app.route('/api/manage/<int:id>', methods=["PUT", "DELETE"])
def manage(id=None):
    if request.method == "GET":
        result = Manage.query.order_by(Manage.mid.desc()).all()
        data = []
        mclass_mapping = {1: "施肥", 2: "浇水", 3: "喷药", 4: "其他"}  # 定义分类映射

        for row in result:
            row_data = row.jsonformat()  # 假设这已经是一个字典了

            # 格式化mtime字段
            if 'mtime' in row_data and isinstance(row_data['mtime'], datetime):
                row_data['mtime'] = row_data['mtime'].strftime('%Y-%m-%d %H:%M:%S')

            # 转换mclass字段
            if 'mclass' in row_data:
                # 使用get方法从映射中获取分类名称，默认为"其他"
                row_data['mclass'] = mclass_mapping.get(row_data['mclass'], "其他")

            data.append(row_data)

        res = {
            "code": 200,
            "msg": "OK",
            "data": data
        }
    elif request.method == "POST":
        params = request.json
        # 确保这里使用的字段与Manage模型匹配
        new_manage = Manage(
            mclass=params['mclass'],
            mtime=datetime.strptime(params['mtime'], '%Y-%m-%d %H:%M:%S'),  # 注意年份格式应为大写的Y，代表四位数的年份
            mdose=params.get('dose', ''),
            minfo=params.get('info', '')
        )
        db.session.add(new_manage)
        db.session.commit()
        res = jsonify({"code": 200, "msg": "创建成功", "data": new_manage.jsonformat()}), 201

    elif request.method == "PUT":
        if not id:
            res = {
                "code": 400,
                "msg": "需要指定ID"
            }
            return res
        manage = Manage.query.filter_by(mid=id).first()
        if not manage:
            res = {
                "code": 404,
                "msg": "资源未找到"
            }
            return res
        data = request.json
        manage.mtime = datetime.strptime(data['mtime'], '%Y-%m-%d %H:%M:%S') if 'mtime' in data else manage.mtime
        manage.mclass = data.get("class", manage.mclass)
        manage.mdose = data.get("dose", manage.mdose)
        manage.minfo = data.get("info", manage.minfo)
        db.session.commit()
        res = {
            "code": 200,
            "msg": "更新成功",
            "data": manage.jsonformat()
        }
    elif request.method == "DELETE":
        if not id:
            return {"code": 400, "msg": "需要指定ID"}
        manage = Manage.query.filter_by(mid=id).first()
        if not manage:
            return {"code": 404, "msg": "资源未找到"}
        db.session.delete(manage)
        db.session.commit()
        res = {"code": 200, "msg": "删除成功"}
    else:
        res = {
            "code": 405,
            "msg": "方法不允许"
        }

    return res


@app.route('/api/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        r = request.json

        m = Manage(mname=r.get("mname"), mclass=int(r.get("mclass")), mtime=r.get("mtime"), mdose=r.get("mdose"))
        try:
            db.session.add(m)
            db.session.commit()
            res = {
                'code': 200,
                'msg': "上传成功！"
            }

        except:
            res = errObj

    else:
        res = "get/upload"
    return make_response(res)


@app.route('/api/delete', methods=['GET', 'POST'])
def deleteManage():
    if request.method == 'POST':
        r = request.json
        mid = r.get("mid")
        m = Manage.query.get(mid)
        if not m:
            res = {
                'code': 300,
                'msg': "信息不存在！"
            }
        else:
            try:
                m_del = Manage.query.filter(Manage.mid == mid).first()
                db.session.delete(m_del)
                db.session.commit()
                db.session.close()
                res = {
                    'code': 200,
                    'msg': "删除成功！"
                }

            except:
                res = errObj

    else:
        res = "get/deleteManage"
    return make_response(res)


@app.route('/api/query', methods=['GET', 'POST'])
def queryInfo():
    if request.method == 'POST':
        r = request.json
        start = r.get("start")
        end = r.get("end")

        result = MonitorParam.query.filter(and_(MonitorParam.create_time >= start, MonitorParam.create_time <= end,
                                                MonitorParam.monitor_no == "8dfeaf752b4d40b4a23819478c90f9ae")).order_by(
            MonitorParam.create_time.desc()).all()
        result2 = MonitorParam.query.filter(and_(MonitorParam.create_time >= start, MonitorParam.create_time <= end,
                                                 MonitorParam.monitor_no == "80280c443ed84233bb9acbbfd7a59ed4")).order_by(
            MonitorParam.create_time.desc()).all()
        # print(result)
        data = []
        for row in result:
            data.append(row.jsonformat())
        for row in result2:
            data.append(row.jsonformat())

        # data = sqlutl.sqlGet(db, sql1)
        if (data != []):
            res = {
                'code': 200,
                'data': data,
                'msg': "恭喜你，查询成功！"
            }
        elif (data == []):
            res = {
                'code': 300,
                'msg': "对不起，未查询到您的信息，请先注册！"
            }
        else:
            res = {
                'code': 500,
                'msg': "对不起，服务器错误。"
            }

    else:
        res = "get/queryInfo"
    return make_response(res)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'


@app.route('/api/uploadAvatar/<int:id>', methods=['POST'])
def upload_file(id=None):
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # 构造用户头像的URL或相对路径
        avatar_url = url_for('static', filename=filename, _external=True)
        print(avatar_url)

        # 更新数据库中的用户uavatar字段
        user_id = id  # 获取当前用户ID
        user = User.query.filter_by(uid=user_id).first()

        if user:
            user.uavatar = avatar_url
            db.session.commit()
            return avatar_url
        else:
            return 'User not found', 404


@app.route('/api/modpwd/<int:id>', methods=['PUT'])
def mod_pwd(id=None):
    if id is None:
        res = {
            "code": 400,
            "msg": "需要指定ID"
        }
    else:
        user = User.query.filter_by(uid=id).first()
        if not user:
            res = {
                "code": 404,
                "msg": "没有找到用户"
            }
        else:
            data = request.json

            if data.get('rawPwd') != '' and user.upwd != data.get('rawPwd'):
                res = {
                    "code": 301,
                    "msg": "原密码错误"
                }
            else:
                user.upwd = data.get('pwd')
                db.session.commit()

                res = {
                    "code": 200,
                    "msg": "修改成功，请重新登陆。"
                }

    return res


@app.route('/api/getUser/<int:id>', methods=['GET', 'PUT'])
def get_user(id=None):
    res = {}
    if id is None:
        res = {
            "code": 400,
            "msg": "需要指定ID"
        }

    else:
        if request.method == "GET":
            result = User.query.filter_by(uid=id).first()
            if result is None:
                res = {
                    "code": 304,
                    "msg": "没有找到指定用户"
                }

            else:
                data = result.jsonformat()
                res = {"code": 200, "data": data, "msg": "ok"}
        elif request.method == "PUT":
            user = User.query.filter_by(uid=id).first()
            if not user:
                res = {
                    "code": 404,
                    "msg": "没有找到用户"
                }
            else:
                data = request.json

                user.uname = data.get('uname', user.uname)
                user.uphone = data.get('uphone', user.uphone)
                user.umail = data.get('umail', user.umail)
                user.uavatar = data.get('uavatar', user.uavatar)
                user.unickname = data.get('unickname', user.unickname)
                user.uinfo = data.get('uinfo', user.uinfo)
                user.umail = data.get('umail', user.umail)

                db.session.commit()

                u = user.jsonformat()

                res = {
                    "code": 200,
                    "data": u,
                    "msg": "更新成功"
                }

    return res


from model.LightGBM_Voting import *
import pandas as pd
@app.route('/api/decision', methods=['POST'])
def decision():
    if request.method == "POST":
        r = request.json
        params_dict = {key: value for key, value in r.items() if key != 'air'}
        params = pd.DataFrame.from_dict(params_dict, orient='index').T
        print(params)

        res_air = predictRes("model/airconditioner", params)
        res_pl = predictRes("model/pl", params)
        res_byc = predictRes("model/byc", params)
        res_tem = predictRes("model/temperature", params)

        data = {
            "airconditioner": bool(res_air[0]),
            "spray": bool(res_pl[0]),
            "windows": bool(res_byc[0]),
            "temperture":  round(float(res_tem[0]), 2),
        }
        print(data)


        return {
            "code":200,
            "data":data,
            "msg":"ok"
        }

if __name__ == '__main__':
    print("start..............................................")


    app.run(host='0.0.0.0', port=3000, threaded=True)
    # run()
    # app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)
