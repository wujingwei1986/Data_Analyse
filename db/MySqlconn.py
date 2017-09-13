# -*- coding: GB18030 -*-
#wujingwei
import requests,string,time,os,json
import MySQLdb as mysql
import xlrd,re
#���ݿ����

def db_connect(ip,user,password):
    global dbcon
    try:
        dbcon = mysql.connect(host = ip, user = user, passwd = password, db = 'test', charset='utf8')
        return dbcon
    except:
        print u"����ʧ��"
        pass

def is_table_exist(cursor,dbname,tablename):
    db_is_exist = False
    table_is_exist = False

    sql_show_database = "show databases"
    cursor.execute(sql_show_database)
    databases = cursor.fetchall()
    for db in databases:
        if dbname in db[0]:
            db_is_exist = True
            break

    if not db_is_exist:
        createDatabase = "create database " + dbname
        cursor.execute(createDatabase)
    #�л����ݿ�
    changeDB = "use " + dbname
    cursor.execute(changeDB)
    sql_show_table = "show tables;"
    cursor.execute(sql_show_table)
    tables = cursor.fetchall()
    for each in tables:
        if tablename in each[0]:
            table_is_exist = True
            break

    return table_is_exist

def insert_Data(dbcon,excel_file,dbname,tablename):
    sql_create = "create table " + tablename + "(deviceIdHex varchar(10), epcHex varchar(40), antennaIndex int(11), TransmitPower int(11), ModulationType int(11), ChannelIndex int(11), DataEncodeType int(11), ForDataRate int(11), RevDataRate int(11), successCount int(11), totalCount int(11), successRate int(11))"
    # ����α����, �������б������ݿ�����
    cursor = dbcon.cursor()
    #�жϱ��Ƿ��Ѿ�����
    is_exist = is_table_exist(cursor,dbname,tablename)
    print is_exist
    if not is_exist:
        cursor.execute(sql_create) #�������ݱ�
        open_excel_insert_db(cursor,excel_file,tablename) #��excel�������ݲ����
    else:
        print (u"%s���Ѿ�����") %tablename

def open_excel_insert_db(cursor,excel_file,tablename):

    # Open the workbook and define the worksheet
    book = xlrd.open_workbook(excel_file)
    sheet = book.sheet_by_name(u"���Խ��")

    # ��������SQL���
    query = """INSERT INTO """ + tablename + """ (deviceIdHex, epcHex, antennaIndex, TransmitPower, ModulationType, ChannelIndex, DataEncodeType, ForDataRate, RevDataRate, successCount, totalCount, successRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    # ����һ��forѭ��������ȡxls�ļ�ÿ�����ݵ�, �ӵڶ��п�ʼ��Ҫ��������
    for r in range(1, sheet.nrows):
        deviceIdHex  = sheet.cell(r,0).value
        epcHex = sheet.cell(r,1).value
        antennaIndex = sheet.cell(r,2).value
        TransmitPower = sheet.cell(r,3).value
        ModulationType = sheet.cell(r,4).value
        ChannelIndex = sheet.cell(r,5).value
        DataEncodeType = sheet.cell(r,6).value
        ForDataRate = sheet.cell(r,7).value
        RevDataRate = sheet.cell(r,8).value
        successCount = sheet.cell(r,9).value
        totalCount = sheet.cell(r,10).value
        successRate = sheet.cell(r,11).value

        values = (deviceIdHex, epcHex, antennaIndex, TransmitPower, ModulationType, ChannelIndex, DataEncodeType, ForDataRate, RevDataRate, successCount, totalCount, successRate)
        cursor.execute(query, values)

    # �ر��α�
    cursor.close()
    # �ύ
    dbcon.commit()
    # �ر����ݿ�����
    dbcon.close()
