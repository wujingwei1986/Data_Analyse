# -*- coding: GB18030 -*-
#wujingwei

import os,sys,time
import numpy as np, pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from Data_Analytics import analyse
from db import MySqlconn

curr_path = os.path.dirname(os.path.realpath(__file__))
result_path = os.path.join(curr_path,'result')
now = time.strftime("%Y-%m-%M-%H_%M_%S",time.localtime(time.time()))
savefig_path = os.path.join(result_path,now)

#�����ļ��б���������
def create_dir():
    isExists=os.path.exists(savefig_path)
    # �жϽ��
    if not isExists:
        # ����������򴴽�Ŀ¼
        # ����Ŀ¼��������
        os.makedirs(savefig_path)

        print savefig_path+' �����ɹ�'
        return True
    else:
        # ���Ŀ¼�����򲻴���������ʾĿ¼�Ѵ���
        print savefig_path+' Ŀ¼�Ѵ���'
        return False

def anaylse_single_data(ip,user,password,dbname,table,start_TransmitPower,end_TransmitPower,DataEncodeType):
    data = analyse.get_Data(ip,user,password,dbname,table)
    analyse.anaylse_Data(data,start_TransmitPower,end_TransmitPower,DataEncodeType)

def anaylse_multiple_datas(ip,user,password,dbname,tables,start_TransmitPower,end_TransmitPower,ModulationType,DataEncodeType,ForRevDataRate,lable_names,save_path):
    datas = analyse.get_Datas(ip,user,password,dbname,tables) #���ݿ��ж�ȡ����
    analyse.anaylse_Datas(datas,start_TransmitPower,end_TransmitPower,ModulationType,DataEncodeType,ForRevDataRate,lable_names,save_path)

def anaylse_single_data_with_ChannleIndex(ip,user,password,dbname,table,start_TransmitPower,end_TransmitPower,successRate):
    data = analyse.get_Data(ip,user,password,dbname,table)
    analyse.anaylse_Data_with_ChannleIndex(data,start_TransmitPower,end_TransmitPower,successRate)

def anaylse_single_data_with_ChannleIndex_by_ForRevDataRate(ip,user,password,dbname,table,start_TransmitPower,end_TransmitPower,successRate):
    data = analyse.get_Data(ip,user,password,dbname,table)
    analyse.anaylse_Data_with_ChannleIndex_by_ForRevDataRate(data,start_TransmitPower,end_TransmitPower,successRate)

if __name__ == '__main__':
    global dbcon
    #���ݿ����Ӳ���
    ip = '192.168.1.173'
    user = 'root'
    password = 'root'
    dbname = 'iis_parameter_traversal'
    table = 'aaa' #���ֻ�Ա�һ������е�����,ʹ��͸�ӱ���ʽչʾ
    tables = ['aaa','bbb','ccc'] #ͬʱ�Աȶ������е�����ʹ�ü�����ͼ
    lable_names = tables   #�����ݶԱ�ʱ����ÿ�����ߵ�����

    Power = range(20,34)
    ModulationType = ['DSB-ASK','PR-ASK']
    DataEncodeType = ['FM0','M2','M4','M8']
    ForRevDataRate = ['40/80','40/160','40/320','40/640','80/80','80/160','80/320','80/640']

    #�������Ա�ͼ��չʾ
    #anaylse_single_data(ip,user,password,dbname,table,30,33,'FM0')

    '''
    #ȫ������������
    create_dir()
    for power_num in Power:
        for ModulationType_num in ModulationType:
            for DataEncodeType_num in DataEncodeType:
                for ForRevDataRate_num in ForRevDataRate:
                    anaylse_multiple_datas(ip,user,password,dbname,tables,power_num,power_num,ModulationType_num,DataEncodeType_num,ForRevDataRate_num,lable_names,savefig_path)
    '''
    #anaylse_single_data_with_ChannleIndex(ip,user,password,dbname,table,18,33,95)

    anaylse_single_data_with_ChannleIndex_by_ForRevDataRate(ip,user,password,dbname,table,18,33,95)