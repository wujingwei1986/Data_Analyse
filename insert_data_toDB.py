# -*- coding: GB18030 -*-
#wujingwei

import os,sys
import numpy as np, pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from Data_Analytics import analyse
from db import MySqlconn
from excel_data import *

if __name__ == '__main__':
    #数据库连接参数
    ip = '192.168.1.173'
    user = 'root'
    password = 'root'
    dbname = 'iis_parameter_traversal' #数据库名字

    global dbcon
    dbcon = MySqlconn.db_connect(ip,user,password)

    MySqlconn.insert_Data(dbcon,u'V02.00.01-普通模式.xls',dbname,'ccc')
