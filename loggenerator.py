#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   loggenerator.py
@Contact :   xhliu@travelsky.com
@License :   (C)Copyright 2020, xhliu work in WLW

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/6/21 13:09   xhliu      1.0         None
"""
help_str="""
这里是对需求的描述
主要目的是生成用于测试脚本的日志
生成的日志有几个要求。
1. 可以接收屏幕输入。
    1.1 指定 YYYY-MM-DD-HH或使用实时时间, 实时时间默认为YYYYMMDDHH格式
    1.2 指定001 002 003类似格式的日志划分, 默认生成3个，不可自行调整。
    1.3 与要求1合并之后，生成的日志类似于abcdefg2020062021.001.log，其中时间日期和rotation都是可选项。
    1.3 指定开始打印日志，结束打印日志
    1.4 default打印内容为“log文件名-agent-0000000001”，最后的数字为自增数字。
    1.5 指定每条日志间隔时间。
    1.6 指定一次性批量生成日志或持续写入按照大小划分日志。
2. 实现屏幕输入的要求。
3. 有帮助文档。
4. 有单元测试。

"""
import logging
import os,sys
import time,datetime

DATE_FORMAT_ERROR_INFO = "date format input error,please check and reinput...bagabaga"


def help():
    print(help_str)
    start()

def dateformatverify(dateinput):
    """
    检查日期格式是否为YYYYMMDDHH或YYYYMMDD
    :param dateinput:
    :return:
    """
    try:
        if(len(dateinput)==8):
            time.strptime(dateinput,'%Y%m%d')
        elif(len(dateinput)==10):
            time.strptime(dateinput,'%Y%m%d%H')
        return True
    except Exception as e:
        print(DATE_FORMAT_ERROR_INFO)
        print(e)
        datechecking()


def datechecking():
    """
    输入日期，并且检查输入日期的格式。
    如果输入日期格式及范围符合要求，则返回一个文件名列表filenames_input
    :return:
    """
    # filename_date_exist = input("do you want dateformate(y/n,default is y): ")
    filename_date_exist="y"
    if (filename_date_exist.find("h")>=0):help()
    if (filename_date_exist.find("y")>=0 or filename_date_exist==""):
        # filename_date_start = input("please input start date(YYYYMMDD/YYYYMMDDHH), if want realtime, please press enter:  ")
        # filename_date_end = input("please input end date(YYYYMMDD/YYYYMMDDHH), if want realtime, please press enter: ")
        filename_date_start = "2020062105"
        filename_date_end = "2020062112"
        if (filename_date_start.find("h") >= 0): help()
        if (filename_date_end.find("h") >= 0): help()
        if (dateformatverify(filename_date_start) and dateformatverify(filename_date_end)):
            if (len(filename_date_start) != len(filename_date_end)):
                print("start date and end date have different pattern. please check and reinput...bagabaga ")
                datechecking()
            elif(filename_date_start=="" and filename_date_end==""):
                filename_time=time.strftime('%Y%m%d%H',time.localtime())
                print(filename_time)
                filenames_input.append(filenames_input+filename_time)
            elif(filename_date_end != filename_date_start):
                if(len(filename_date_start)==8):
                    day_count_start =datetime.datetime.strptime(filename_date_start,"%Y%m%d")
                    day_count_end=datetime.datetime.strptime(filename_date_end,"%Y%m%d")
                    daycount = (day_count_end-day_count_start).days
                    for daydiff in range(0,daycount+1):
                        try:
                            temp_date=datetime.timedelta(days=daydiff)
                            temp_date=temp_date+day_count_end
                            str_temp_date=temp_date.strftime('%Y%m%d')
                            filenames_input.append(filename_input+str_temp_date+".log")
                        except Exception as e:
                            print(e)
                    print(filenames_input)
                elif(len(filename_date_start)==10):
                    hour_count_start=datetime.datetime.strptime(filename_date_start,"%Y%m%d%H")
                    hour_count_end=datetime.datetime.strptime(filename_date_end,"%Y%m%d%H")
                    hourcount = int((hour_count_end-hour_count_start).seconds/3600)
                    for hourdiff in range(0,hourcount+1):
                        try:
                            temp_date=datetime.timedelta(hours=hourdiff)
                            temp_date=temp_date+hour_count_start
                            str_temp_date=temp_date.strftime('%Y%m%d%H')
                            filenames_input.append(filename_input+str_temp_date+".log")
                        except Exception as e:
                            print(e)
                    print(filenames_input)
        filenames_array=filenames_input


def rotationchecking():
    #filename_rotation = input("do you want rotation(y/n): ")
    filename_rotation = "y"
    if (filename_rotation.find("h") >= 0): help()
    if ((filename_rotation=="y" or filename_rotation=="") and len(filenames_input)):
        for temp_filename in filenames_input:
            for temp_rotation in range(1,4):
                filenames_input_with_rotation.append(temp_filename+"."+str(temp_rotation).zfill(3)+".log")
        print(filenames_input_with_rotation)
        filenames_array=filenames_input_with_rotation

def fileexist(filename):
    '''
    判断文件是否存在
    :param filename:
    :return:
    '''
    if(os.path.exists(filename)):
        return True
    else:
        return False

def filetruncate(filename):
    """
    如果文件存在，先清空再写。
    :param filename:
    :return:
    """
    f=open(filename,"w+")
    f.truncate()
    f.close()

def sethandler(handler,formatter):
    """
    由于remove logging.handler的时候把handler的属性都给remove了。所以要重新设置一下，
    用到的地方还挺多的，所以抽出来写个方法。
    :param handler:
    :param formatter:
    :return:
    """
    handler.setFormatter(formatter)
    handler.setLevel(10)
    return handler
# main
# 文件名

def start():
    # filename_input = input("please input log name(without .log):  ")
    filename_input='access'
    if (filename_input.find("h") >= 0): help()
    # filename_real_time=input("do you want to use real time log filename（y/n，default is y）： ")
    filename_real_time = ""
    if(filename_real_time=="y" or filename_real_time==""):
        num_filename = 1
        filename_date=datetime.datetime.now().strftime('%Y%m%d%H')
        filename_input_real=filename_input+filename_date+ "."+str(num_filename).zfill(3)+".log"
        print(filename_input_real)
        if(fileexist(filename_input_real)):filetruncate(filename_input_real)
        # logging.basicConfig(filename=filename_input_real,
        #                     format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
        #                     datefmt='%Y-%m-%d %H:%M:%S %p',
        #                     level=10)
        logger=logging.getLogger("test log")
        fh_filename=logging.FileHandler(filename_input_real)
        fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s','%Y-%m-%d %H:%M:%S %p')
        fh_filename = sethandler(fh_filename,fh_formatter)
        logger.addHandler(fh_filename)
        num_content=1
        while(True):
            logger.error(filename_input_real+"****agent****"+str(num_content).zfill(10))
            num_content+=1
            time.sleep(1)
            if (os.path.getsize(filename_input_real)>=1024):
                if (datetime.datetime.now().strftime('%Y%m%d%H') != filename_date):
                    num_filename=1
                    filename_input_real = filename_input + datetime.datetime.now().strftime('%Y%m%d%H') + "."+ str(
                    num_filename).zfill(3) + ".log"
                    if (fileexist(filename_input_real)): filetruncate(filename_input_real)
                    logger.removeHandler(fh_filename)
                    fh_filename=logging.FileHandler(filename_input_real)
                    # 上面removeHandler的时候，把handler的属性也都remove掉了。所以要重新设置一下。
                    fh_filename = sethandler(fh_filename, fh_formatter)
                    logger.addHandler(fh_filename)
                else:
                    num_filename+=1
                    filename_input_real = filename_input + datetime.datetime.now().strftime('%Y%m%d%H') + "."+ str(
                        num_filename).zfill(3) + ".log"
                    if (fileexist(filename_input_real)): filetruncate(filename_input_real)
                    logger.removeHandler(fh_filename)
                    fh_filename=logging.FileHandler(filename_input_real)
                    # 上面removeHandler的时候，把handler的属性也都remove掉了。所以要重新设置一下。
                    fh_filename = sethandler(fh_filename, fh_formatter)
                    logger.addHandler(fh_filename)


    else:
        # 是否需要输入日期
        datechecking()
        rotationchecking()
    num_content=1
    logging.basicConfig(filename=filename_input,
                        format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %p',
                        level=10)
    if (os.path.exists(filename_input)):
        print (os.path.getsize(filename_input))

    # logging.debug('调试debug')
    # logging.info('消息info')
    # logging.warning('警告warn')
    logging.error(filename_input+'-agent-'+str(num_content).zfill(10))
    num_content+=1
    # logging.critical('严重critical')

filename_input=""
filname_date = ""
filename_date_exist = ""
filenames_input = []
filenames_input_with_rotation = []
filenames_array = []
start()

