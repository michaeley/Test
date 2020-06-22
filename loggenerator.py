#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   loggenerator.py
@Contact :   
@License :   (C)Copyright 2020, xhliu work in WLW

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/6/21 13:09   xhliu      1.0         None
"""
help_str = """
这里是对需求的描述
主要目的是生成用于测试脚本的日志
生成的日志有几个要求。
1. 可以接收屏幕输入。
    1.1 指定 YYYY-MM-DD-HH或使用实时时间, 实时时间默认为YYYYMMDDHH格式
    1.2 指定001 002 003类似格式的日志划分, 默认生成3个，不可自行调整。
    1.3 与要求1合并之后，生成的日志类似于abcdefg2020062021.001.log，其中时间日期和rotation都是可选项。
    1.4 default打印内容为“log文件名-agent-0000000001”，最后的数字为自增数字。
    1.5 指定每条日志间隔时间。
    1.6 指定一次性批量生成日志或持续写入按照大小划分日志。
2. 实现屏幕输入的要求。
3. 有帮助文档。
4. 有单元测试。(todo)

"""
import logging
import os, sys
import time, datetime
import logging.handlers

DATE_FORMAT_ERROR_INFO = "date format input error,please check and reinput...bagabaga"


def help():
    print(help_str)
    start()


def dateformatverify(dateinput):
    """
    检查日期格式是否为YYYYMMDDHH或YYYYMMDD
    :param dateinput:要检查的日期
    :return:如果日期符合格式，返回True，否则打印异常并提示重新输入
    """
    try:
        if (len(dateinput) == 8):
            time.strptime(dateinput, '%Y%m%d')
        elif (len(dateinput) == 10):
            time.strptime(dateinput, '%Y%m%d%H')
        return True
    except Exception as e:
        print(DATE_FORMAT_ERROR_INFO)
        print(e)
        datechecking()


def datechecking(filename_input):
    """
    输入日期，并且检查输入日期的格式。
    如果输入日期格式及范围符合要求，则返回一个文件名列表filenames_array
    :param filename_input: 日志文件名的固定部分，不包含.log
    :return: 文件名列表filenames_array
    """

    # filename_date_exist = input("do you want dateformate(y/n,default is y): ")
    filename_date_exist = "y"
    if (filename_date_exist.find("h") >= 0): help()
    if (filename_date_exist.find("y") >= 0 or filename_date_exist == ""):
        filename_date_start = input("please input start date(YYYYMMDD/YYYYMMDDHH):  ")
        filename_date_end = input("please input end date(YYYYMMDD/YYYYMMDDHH): ")
        if (filename_date_start.find("h") >= 0): help()
        if (filename_date_end.find("h") >= 0): help()
        # 检查日期格式
        if (dateformatverify(filename_date_start) and dateformatverify(filename_date_end)):
            # 如果两次输入的格式不同，重新输入
            if (len(filename_date_start) != len(filename_date_end)):
                print("start date and end date have different pattern. please check and reinput...bagabaga ")
                datechecking()
            # 如果两次输入的都为空，则将文件名置为默认值YYYYMMDDHH
            elif (filename_date_start == "" and filename_date_end == ""):
                filename_time = time.strftime('%Y%m%d%H', time.localtime())
                filenames_input.append(filename_input + filename_time + ".log")
            # 如果两次输入的不一样，根据格式算出日期差值（天或小时）
            # 将算出来的日期差值顺序加入日志名固定部分后面
            # 例如
            # 原来的日志名固定部分是“access”，变更之后变为“access20200621.log、
            #                                               access20200622.log”
            # 豆知识：1. datetime.timedelta也是datetime类型，可以和datetime相加。
            #        2. datetime类型相减只能算days，secs，microsecs，没有hours，months等，需要换算。
            #        3. strftime将datetime类型转换为string.
            #        4. strptime将string转换为datetime.
            elif (filename_date_end != filename_date_start):
                if (len(filename_date_start) == 8):
                    day_count_start = datetime.datetime.strptime(filename_date_start, "%Y%m%d")
                    day_count_end = datetime.datetime.strptime(filename_date_end, "%Y%m%d")
                    daycount = (day_count_end - day_count_start).days
                    for daydiff in range(0, daycount + 1):
                        try:
                            temp_date = datetime.timedelta(days=daydiff)
                            temp_date = temp_date + day_count_start
                            str_temp_date = temp_date.strftime('%Y%m%d')
                            filenames_input.append(filename_input + str_temp_date + ".log")
                        except Exception as e:
                            print(e)
                    print(filenames_input)
                elif (len(filename_date_start) == 10):
                    hour_count_start = datetime.datetime.strptime(filename_date_start, "%Y%m%d%H")
                    hour_count_end = datetime.datetime.strptime(filename_date_end, "%Y%m%d%H")
                    hourcount = int((hour_count_end - hour_count_start).seconds / 3600)
                    for hourdiff in range(0, hourcount + 1):
                        try:
                            temp_date = datetime.timedelta(hours=hourdiff)
                            temp_date = temp_date + hour_count_start
                            str_temp_date = temp_date.strftime('%Y%m%d%H')
                            filenames_input.append(filename_input + str_temp_date + ".log")
                        except Exception as e:
                            print(e)
                    print(filenames_input)
            # 剩下的情况就是开始时间和结束时间相同，随便选一个就行了。
            else:
                filenames_input.append(filename_input + filename_date_start + ".log")
        filenames_array=filenames_input
        return filenames_array


def rotationchecking(filenames_input):
    """
    判断是否需要多个001 002 003之类的文件。需要的话默认是3个，不能改。
    :param filenames_input:
    :return:
    """
    # filename_rotation = input("do you want rotation(y/n): ")
    filename_rotation = "y"
    filenames_array=filenames_input
    if (filename_rotation.find("h") >= 0): help()
    if ((filename_rotation == "y" or filename_rotation == "") and len(filenames_input)):
        for temp_filename in filenames_input:
            # 经过datechecking处理的文件名数组可能，大概，或许加上了".log"，要去掉.log
            if (temp_filename.find(".log")>=0):temp_filename=temp_filename[:-4]
            for temp_rotation in range(1, 4):
                filenames_input_with_rotation.append(temp_filename + "." + str(temp_rotation).zfill(3) + ".log")
        print(filenames_input_with_rotation)
        filenames_array = filenames_input_with_rotation
    return filenames_array


def fileexist(filename):
    '''
    判断文件是否存在
    :param filename:
    :return:
    '''
    if (os.path.exists(filename)):
        return True
    else:
        return False


def filetruncate(filename):
    """
    如果文件存在，先清空再写。
    :param filename:
    :return:
    """
    f = open(filename, "w+")
    f.truncate()
    f.close()


def sethandler(handler, formatter):
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
    filename_input = 'access'
    if (filename_input.find("h") >= 0): help()
    filename_real_time=input("do you want to use real time log filename（y/n，default is y）： ")
    # 实时日志数据
    if (filename_real_time == "y" or filename_real_time == ""):
        num_filename = 1
        filename_date = datetime.datetime.now().strftime('%Y%m%d%H')
        # 用当前时间戳生成文件名，包含YYYYMMDDHH的日期和001.002等自增数字
        filename_input_real = filename_input + filename_date + "." + str(num_filename).zfill(3) + ".log"
        # 如果已经有了先清空
        if (fileexist(filename_input_real)): filetruncate(filename_input_real)
        # logging.basicConfig(filename=filename_input_real,
        #                     format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
        #                     datefmt='%Y-%m-%d %H:%M:%S %p',
        #                     level=10)
        # 日志记录的问题比较复杂，参见
        # https://blog.csdn.net/michaeley1/article/details/106889091
        logger = logging.getLogger("test log")
        fh_filename = logging.FileHandler(filename_input_real)
        fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                                         '%Y-%m-%d %H:%M:%S %p')
        fh_filename = sethandler(fh_filename, fh_formatter)
        logger.addHandler(fh_filename)
        num_content = 1
        while (True):
            logger.error(filename_input_real + "****agent****" + str(num_content).zfill(10))
            num_content += 1
            # 每5秒写一条，每4K一个文件
            time.sleep(5)
            if (os.path.getsize(filename_input_real) >= 4096):
                if (datetime.datetime.now().strftime('%Y%m%d%H') != filename_date):
                    num_filename = 1
                    filename_input_real = filename_input + datetime.datetime.now().strftime('%Y%m%d%H') + "." + str(
                        num_filename).zfill(3) + ".log"
                    if (fileexist(filename_input_real)): filetruncate(filename_input_real)
                    logger.removeHandler(fh_filename)
                    fh_filename = logging.FileHandler(filename_input_real)
                    # 上面removeHandler的时候，把handler的属性也都remove掉了。所以要重新设置一下。
                    fh_filename = sethandler(fh_filename, fh_formatter)
                    logger.addHandler(fh_filename)
                else:
                    num_filename += 1
                    filename_input_real = filename_input + datetime.datetime.now().strftime('%Y%m%d%H') + "." + str(
                        num_filename).zfill(3) + ".log"
                    if (fileexist(filename_input_real)): filetruncate(filename_input_real)
                    logger.removeHandler(fh_filename)
                    fh_filename = logging.FileHandler(filename_input_real)
                    # 上面removeHandler的时候，把handler的属性也都remove掉了。所以要重新设置一下。
                    fh_filename = sethandler(fh_filename, fh_formatter)
                    logger.addHandler(fh_filename)

    # 批量生成
    else:
        # 是否需要输入日期
        filenames_array = datechecking(filename_input)
        print(filenames_array)
        filenames_array = rotationchecking(filenames_array)
        logger = logging.getLogger("test log")
        for filename_input_inarray in filenames_array:
            if (fileexist(filename_input_inarray)): filetruncate(filename_input_inarray)
            fh_filename = logging.FileHandler(filename_input_inarray)
            fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                                             '%Y-%m-%d %H:%M:%S %p')
            fh_filename = sethandler(fh_filename, fh_formatter)
            logger.addHandler(fh_filename)
            for num_content in range(1,41):
                logger.error(filename_input_inarray + "****agent****" + str(num_content).zfill(10))
            logger.removeHandler(fh_filename)


filename_input = ""
filname_date = ""
filename_date_exist = ""
filenames_input = []
filenames_input_with_rotation = []
filenames_array = []
start()
