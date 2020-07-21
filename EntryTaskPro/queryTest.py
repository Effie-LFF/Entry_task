import decimal
from _pydecimal import Decimal

from numpy import double
from testbase.testcase import TestCase
from testbase import datadrive
import requests

testdata = [
    # 正常申请
    {"name_id": "user001", "price": 123.3, "discount": 0.9},
    # 参数缺失
    {"price": 123.3, "discount": 0.9},
    {"name_id": "user001", "discount": 0.9},
    {"name_id": "user001", "price": 123.3},
    {"name_id": "user001"},
    {"discount": 0.9},
    {"price": 123.3},
    {},
    # 参数多传
    {"name_id": "user001", "price": 123.3, "discount": 0.9, "add": "add"},
    # 参数名错误
    {"name": "user001", "price": 123.3, "discount": 0.9},
    # 参数为空
    {'price': 123.3, 'discount': 0.9, 'name_id': ""},
    {'price': "", 'discount': 0.9, 'name_id': "user001"},
    {'price': 123.3, 'discount': "", 'name_id': "user001"},
    {'price': "", 'discount': "", 'name_id': "user001"},
    {'price': "", 'discount': 0.9, 'name_id': ""},
    {'price': 123.3, 'discount': "", 'name_id': ""},
    {'price': "", 'discount': "", 'name_id': ""},
    # 参数类型错误
    {'price': "abc", 'discount': 0.9, 'name_id': "user001"},
    {'price': 123.3, 'discount': "abc", 'name_id': "user001"},
    {'price': 123.3, 'discount': 0.9, 'name_id': ['user', '001']},
    {'price': "abc", 'discount': "bc", 'name_id': "user001"},
    {'price': "abc", 'discount': 0.9, 'name_id': ['user', '001']},
    {'price': 123.3, 'discount': "bc", 'name_id': ['user', '001']},
    {'price': "abc", 'discount': "bc", 'name_id': ['user', '001']},
    # double参数a取值
    {'price': double(decimal.MAX_PREC), 'discount': 0.9, 'name_id': "user001"},
    {'price': double(decimal.MAX_PREC + Decimal(0.01)), 'discount': 0.9, 'name_id': "user001"},
    {'price': 0, 'discount': 0.9, 'name_id': "user001"},
    {'price': -0.01, 'discount': 0.9, 'name_id': "user001"},
    # double参数b取值
    {'price': 123.3, 'discount': 1, 'name_id': "user001"},
    {'price': 123.3, 'discount': 1.01, 'name_id': "user001"},
    {'price': 123.3, 'discount': 0, 'name_id': "user001"},
    {'price': 123.3, 'discount': -0.01, 'name_id': "user001"},
    # string参数c取值
    {'price': 123.3, 'discount': 0.9, 'name_id': "use"},
    {'price': 123.3, 'discount': 0.9, 'name_id': "us"},
    {'price': 123.3, 'discount': 0.9, 'name_id': "use" * 10 + "ab"},
    {'price': 123.3, 'discount': 0.9, 'name_id': "use" * 10 + "abc"},
    # 用户不存在
    {'price': 123.3, 'discount': 0.9, 'name_id': "user010"},
    # 余额不足
    {'price': 12300.3, 'discount': 0.9, 'name_id': "user001"}
]


@datadrive.DataDrive(testdata)
class QueryTest(TestCase):
    """
    测试query接口
    """
    owner = "TestFlask"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 1

    def run_test(self):
        # Users()
        # ---------------------------
        self.start_step("测试用户ID")
        # ---------------------------
        # 请求该接口
        response = requests.post('http://127.0.0.1:5000/query', json=self.casedata)
        # 获取响应数据，并解析JSON，转化为python字典
        result = response.json()
        # 打印响应状态码
        # print(response.status_code)

        self.assert_("是否通过检查点", result["result"] == "0")
        print("响应的详细信息：")
        print(result)


if __name__ == '__main__':
    QueryTest().debug_run()
