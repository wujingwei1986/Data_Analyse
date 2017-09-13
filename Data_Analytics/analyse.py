# -*- coding: GB18030 -*-
#wujingwei

import os,sys,time
import numpy as np, pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from pylab import *
sys.path.append("../db")
sys.path.append("../result")
from db import MySqlconn


#获取一个表的数据
def get_Data(ip,user,password,dbname,table):
    conn = MySqlconn.db_connect(ip,user,password)
    cursor = conn.cursor()
    #切换数据库
    changeDB = "use " + dbname
    cursor.execute(changeDB)

    query = "select * from " + table
    data = pd.read_sql(query,conn)
    return data

#分析单个表格的数据
def anaylse_Data(data,start_TransmitPower,end_TransmitPower,DataEncodeType):
    if DataEncodeType == 'FM0':
        DataEncode_Value = 0
    elif DataEncodeType == 'M2':
        DataEncode_Value = 1
    elif DataEncodeType == 'M4':
        DataEncode_Value = 2
    elif DataEncodeType == 'M8':
        DataEncode_Value = 3
    filter_data = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['DataEncodeType']==DataEncode_Value)]
    #print filter_data
    subset = pd.pivot_table(filter_data,index=['ModulationType','TransmitPower','ChannelIndex'],values=['successRate'],columns=['DataEncodeType','ForDataRate','RevDataRate'])
    subset.plot(title=u"参数遍历",grid=True,color=['red','greenyellow','darkviolet','deepskyblue','green','black','lightgrey','darkorange'])
    plt.ylim(80.00,100.00)
    plt.show()

#获取多个表格的数据
def get_Datas(ip,user,password,dbname,tables):
    datas = []
    conn = MySqlconn.db_connect(ip,user,password)
    cursor = conn.cursor()
    #切换数据库
    changeDB = "use " + dbname
    cursor.execute(changeDB)
    for table in tables:
        query = "select * from " + table
        datas.append(pd.read_sql(query,conn))
    return datas

def anaylse_Datas(datas,start_TransmitPower,end_TransmitPower,ModulationType,DataEncodeType,ForRevDataRate,lable_names,save_path):
    subdatas = []
    plt.figure(figsize=(18,9))
    if ModulationType == 'DSB-ASK':
        Modulation_Value = 1
    elif ModulationType == 'PR-ASK':
        Modulation_Value = 3

    if DataEncodeType == 'FM0':
        DataEncode_Value = 0
    elif DataEncodeType == 'M2':
        DataEncode_Value = 1
    elif DataEncodeType == 'M4':
        DataEncode_Value = 2
    elif DataEncodeType == 'M8':
        DataEncode_Value = 3

    ForDataRate =  int(ForRevDataRate.split('/')[0])
    RevDataRate =  int(ForRevDataRate.split('/')[1])
    for num,data in enumerate(datas):
        filter_data = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['ModulationType']==Modulation_Value) & (data['DataEncodeType']==DataEncode_Value) & (data['ForDataRate']==ForDataRate) & (data['RevDataRate']==RevDataRate)]

        #获取每组数据成功率最低的点和对应频点
        sort_successRate_data = filter_data.sort_values(by='successRate').head(1)
        lower_successRate = sort_successRate_data['successRate'].min()  #min方法主要是消除Name和dtype字段，没有其他意义
        chanIndex = sort_successRate_data['ChannelIndex'].min()

        subset_legend = "subset_legend_"+str(num)

        subset_legend, = plt.plot(filter_data['ChannelIndex'],filter_data['successRate'])
        #图形上添加注释
        plt.annotate('SuccessRate:{0}\nChannelIndex:{1}'.format(lower_successRate,chanIndex), xy = (chanIndex, lower_successRate), xytext = (chanIndex-2, lower_successRate-3), arrowprops = dict(facecolor = 'blue', shrink = 0.02))
        subdatas.append(subset_legend)
    print subdatas
    plt.ylim(80.00,102.00)
    plt.grid(True)
    plt.ylabel("successRate")
    plt.xlabel('start_Power:{0},end_Power:{1},ModulationType:{2},DataEncodeType:{3},ForRevDataRate:{4}'.format(start_TransmitPower,end_TransmitPower,ModulationType,DataEncodeType,ForRevDataRate))
    plt.title("parameter-traversal")

    plt.legend(subdatas,lable_names,loc='lower right')
    figname = '{0}-{1}-{2}-{3}-{4}-{5}'.format(start_TransmitPower,end_TransmitPower,ModulationType,DataEncodeType,ForDataRate,RevDataRate)
    #plt.show()

    savename = os.path.join(save_path,figname)
    plt.savefig(savename, dpi=199 )

#分析按频点分析每种编码方式中成功率小于指定数值
def anaylse_Data_with_ChannleIndex(data,start_TransmitPower,end_TransmitPower,successRate):

    filter_data = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate)]
    filter_data_FM0 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==0)]
    filter_data_M2 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==1)]
    filter_data_M4 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==2)]
    filter_data_M8 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==3)]

    fig = plt.figure()#figsize=(10,6)
    fig.subplots_adjust(hspace=0.5) #调整子图之间间距
    #大图的标题
    fig.suptitle(u'功率{0}-{1}各频点成功率小于{2}%个数统计'.format(start_TransmitPower,end_TransmitPower,successRate))
    #===================================总计=======================================
    plt.subplot(313)
    ChannelIndex_num = filter_data.groupby('ChannelIndex').successRate.count()
    y = list(ChannelIndex_num)
    x = range(len(y))
    ylable_num = ChannelIndex_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('Total')
    plt.ylabel('Count')
    ChannelIndex_num.plot(kind = 'bar')
    plt.ylim(0,ylable_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================FM0=======================================
    plt.subplot(321)
    ChannelIndex_FM0_num = filter_data_FM0.groupby('ChannelIndex').successRate.count()
    y = list(ChannelIndex_FM0_num)
    x = range(len(y))
    ylable_FM0_num = ChannelIndex_FM0_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('FM0')
    plt.ylabel('Count')
    ChannelIndex_FM0_num.plot(kind = 'bar')
    plt.ylim(0,ylable_FM0_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================M2=======================================
    plt.subplot(322)
    ChannelIndex_M2_num = filter_data_M2.groupby('ChannelIndex').successRate.count()
    y = list(ChannelIndex_M2_num)
    x = range(len(y))
    ylable_M2_num = ChannelIndex_M2_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title("M2")
    plt.ylabel('Count')
    ChannelIndex_M2_num.plot(kind = 'bar')
    plt.ylim(0,ylable_M2_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================M4=======================================
    plt.subplot(323)
    ChannelIndex_M4_num = filter_data_M4.groupby('ChannelIndex').successRate.count()
    y = list(ChannelIndex_M4_num)
    x = range(len(y))
    ylable_M4_num = ChannelIndex_M4_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('M4')
    plt.ylabel('Count')
    ChannelIndex_M4_num.plot(kind = 'bar')
    plt.ylim(0,ylable_M4_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================M8=======================================
    plt.subplot(324)
    ChannelIndex_M8_num = filter_data_M8.groupby('ChannelIndex').successRate.count()
    y = list(ChannelIndex_M8_num)
    x = range(len(y))
    ylable_M8_num = ChannelIndex_M8_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('M8')
    plt.ylabel('Count')
    ChannelIndex_M8_num.plot(kind = 'bar')
    plt.ylim(0,ylable_M8_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    plt.show()

#分析按频点分析每种编码方式中成功率小于指定数值
def anaylse_Data_with_ChannleIndex_by_ForRevDataRate(data,start_TransmitPower,end_TransmitPower,successRate):

    filter_data = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate)]
    filter_data_FM0 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==0)]
    filter_data_M2 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==1)]
    filter_data_M4 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==2)]
    filter_data_M8 = data.loc[(data['TransmitPower']>=start_TransmitPower) & (data['TransmitPower']<=end_TransmitPower) & (data['successRate']<successRate) & (data['DataEncodeType']==3)]

    fig = plt.figure()#figsize=(10,6)
    fig.subplots_adjust(hspace=1) #调整子图之间间距
    #大图的标题
    fig.suptitle(u'功率{0}-{1}各频点成功率小于{2}%个数统计'.format(start_TransmitPower,end_TransmitPower,successRate))
    #===================================总计=======================================
    plt.subplot(313)
    ChannelIndex_num = filter_data.groupby(['ForDataRate','RevDataRate']).successRate.count()
    y = list(ChannelIndex_num)
    x = range(len(y))

    ylable_num = ChannelIndex_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('Total')
    plt.ylabel('Count')

    ChannelIndex_num.plot(kind='bar',color=['red', 'blue'])
    plt.ylim(0,ylable_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================FM0=======================================
    plt.subplot(321)
    ChannelIndex_FM0_num = filter_data_FM0.groupby(['ForDataRate','RevDataRate']).successRate.count()
    y = list(ChannelIndex_FM0_num)
    x = range(len(y))
    ylable_FM0_num = ChannelIndex_FM0_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('FM0')
    plt.ylabel('Count')
    ChannelIndex_FM0_num.plot(kind = 'bar',color=['red', 'blue'])
    plt.ylim(0,ylable_FM0_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================M2=======================================
    plt.subplot(322)
    ChannelIndex_M2_num = filter_data_M2.groupby(['ForDataRate','RevDataRate']).successRate.count()
    y = list(ChannelIndex_M2_num)
    x = range(len(y))
    ylable_M2_num = ChannelIndex_M2_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title("M2")
    plt.ylabel('Count')
    ChannelIndex_M2_num.plot(kind = 'bar',color=['red', 'blue'])
    plt.ylim(0,ylable_M2_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================M4=======================================
    plt.subplot(323)
    ChannelIndex_M4_num = filter_data_M4.groupby(['ForDataRate','RevDataRate']).successRate.count()
    y = list(ChannelIndex_M4_num)
    x = range(len(y))
    ylable_M4_num = ChannelIndex_M4_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('M4')
    plt.ylabel('Count')
    ChannelIndex_M4_num.plot(kind = 'bar',color=['red', 'blue'])
    plt.ylim(0,ylable_M4_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    #===================================M8=======================================
    plt.subplot(324)
    ChannelIndex_M8_num = filter_data_M8.groupby(['ForDataRate','RevDataRate']).successRate.count()
    y = list(ChannelIndex_M8_num)
    x = range(len(y))
    ylable_M8_num = ChannelIndex_M8_num.max() * 1.2 #获取最大值方便调整纵轴坐标
    plt.title('M8')
    plt.ylabel('Count')
    ChannelIndex_M8_num.plot(kind = 'bar',color=['red', 'blue'])
    plt.ylim(0,ylable_M8_num)
    for x,y in zip(x,y):
        plt.text(x,y,'%.0f'%y,ha='center', va= 'bottom',fontsize=12)

    plt.show()