import decimal
from decimal import Decimal

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from numpy.core import double

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'lff12345'
    database = 'my_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class User(db.Model):
    # 定义表名
    __tablename__ = 'users'
    # 定义字段
    name_id = db.Column(db.String(32), unique=True, primary_key=True)
    balance = db.Column(db.DECIMAL(38, 2))

    def __int__(self, name_id, balance):
        self.name_id = name_id
        self.balance = balance


def add(name_id, balance):
    """
    增加数据
    :param name_id: 用户名
    :param balance: 余额
    :return:
    """
    user = User(name_id=name_id, balance=balance)
    db.session.add(user)
    db.session.commit()


def is_double(s):
    """
    判断是否是浮点数类型
    """
    try:
        double(s)
        return True
    except (TypeError, ValueError):
        return False


def is_enough(a, b, c):
    """
    判断用户余额是否足够
    :param a: price价格
    :param b: dicount 折扣
    :param c: balance 用户余额
    :return: 是否足够
    """
    if c >= a * b:
        return True
    else:
        return False


@app.route('/query', methods=["POST"])
def query():
    """
    price = request.form.get("price")
    discount = request.form.get("discount")
    name_id = request.form.get("name_id")
    #user = Users.query.filter(Users.id == name_id).all()
    """
    # 接收前端发来的数据
    # data = json.loads(request.form.get('data'))
    # 接收http发送来的数据
    data = request.get_json()

    buy = False
    account = None
    try:
        if data['name_id'] is None or data['price'] is None:
            '''参数缺失'''
            result = "10"
        else:
            '''a、b参数均不缺失'''
            name_id = data['name_id']
            if name_id == "":
                '''c参数为空'''
                result = "40"
                # error_msg = "empty params"
            elif type(name_id) == str:
                '''c参数参数是字符串类型'''
                if 32 >= len(name_id) >= 3:
                    '''c参数长度符合条件'''
                    user = User.query.filter(User.name_id == name_id).first()
                    if user is None:
                        '''c用户不存在'''
                        result = "90"
                        # error_msg = "not exist"
                    else:
                        '''c用户存在'''
                        balance = user.balance
                        if data["price"] == "":
                            '''a参数值为空'''
                            result = "40"
                            account = user.balance
                            # error_msg = "empty params"
                        elif is_double(data['price']):
                            '''a参数为double类型'''
                            price = Decimal.from_float(data['price'])
                            if price > decimal.MAX_PREC or price < 0.0:
                                '''a参数超过范围'''
                                result = "60"
                                account = balance
                                return jsonify({'result': result,
                                                'buy': buy,
                                                'account': double(account)})
                            else:
                                '''a参数正常'''
                                if data["discount"] == "":
                                    '''b参数为空'''
                                    discount = Decimal.from_float(1.0)
                                elif data["discount"] is None:
                                    '''b参数缺失'''
                                    result = "10"
                                    account = balance
                                    return jsonify({'result': result,
                                                    'buy': buy,
                                                    'account': double(account)})
                                elif is_double(data["discount"]):
                                    '''b参数为double类型'''
                                    discount = Decimal.from_float(data["discount"])
                                    if discount < 0.0 or discount > 1.0:
                                        '''b参数取值不在范围内'''
                                        result = "70"
                                        account = balance
                                        return jsonify({'result': result,
                                                        'buy': buy,
                                                        'account': double(account)})
                                else:
                                    '''b参数为非double类型'''
                                    result = "50"
                                    account = balance
                                    return jsonify({'result': result,
                                                    'buy': buy,
                                                    'account': double(account)})

                                if is_enough(price, discount, balance):
                                    '''余额足够'''
                                    result = "0"
                                    buy = True
                                    account = price.fma(-discount, balance)
                                    # error_msg = 'success'
                                else:
                                    '''余额不足'''
                                    result = '100'
                                    account = balance
                                    # error_msg = "not enough"
                        else:
                            '''a参数类型错误,非double类型'''
                            result = "50"
                            account = balance
                else:
                    '''c参数长度越界'''
                    result = "80"
                    # error_msg = "out of range"
            else:
                '''c参数非字符串类型'''
                result = "50"
    except KeyError:
        result = "10"
    return jsonify({'result': result,
                    'buy': buy,
                    'account': double(account)})


if __name__ == '__main__':
    # app.run(debug=True)
    # 创建所有表
    db.create_all()
    add('user001', 1234.12)
    add('user002', 1111.15)
    add('user003', 2134.54)
    add('user004', 8888888.8)
    add('use', 1234.12)
    add('use' * 10 + 'ab', 1234.12)

    # 删除所有表
    # db.drop_all()
