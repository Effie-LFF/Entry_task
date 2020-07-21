# Entry_task
These are for Entry_Task

- myfile.py文件的作用
  1. 连接数据库<br>
  数据库表（mysql）：<br>
&nbsp;&nbsp;&nbsp;&nbsp;name：用户id（全局唯一，包含字母）<br>
&nbsp;&nbsp;&nbsp;&nbsp;account：用户余额（精确到小数点后两位）
  2. 使用python实现一个查询接口，接口名为query，接口监听的端口为5000 <br>
     功能：查询用户账号余额是否足够购买一个物品
  
- queryTest.py文件的作用<br>
&nbsp;&nbsp;&nbsp;&nbsp;给出用例数据，使用qtaf对该接口实现自动化测试
&nbsp;&nbsp;&nbsp;&nbsp;其测试报告在文件 report.txt 中

- locustfile.py文件的作用<br>
&nbsp;&nbsp;&nbsp;&nbsp;使用locust进行性能测试，其测试报告如下：

