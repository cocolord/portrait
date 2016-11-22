# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import os

def get_dir_list(path):
	# 获得目录下的所有文件
	return os.listdir(path)

def init(path):
	""" 初始化，读取json文本文件 """
	file = open(path, 'r')
	text = file.read()
	file.close()
	obj = json.loads(text)
	return obj
# end init

def read_file(path):
	""" 读取文件 """
	file = open(path, 'r')
	text = file.read()
	file.close()
	return text

def check_path(path):
	""" 检查路径是否存在。makedirs: 包含子文件夹 """
	if not os.path.exists(path):
		os.makedirs(path)
# end check_path

def output(path, name, text):
	""" 输出 response 内容到文件 """
	check_path(path)
	file = str(path) + '/' + str(name) + '.txt'
	f = open(file, 'w')
	f.write(text)
	f.close()
# end output

def check_file(path):
	""" 检查文件是否存在 """
	return os.path.isfile(path)
# end check_file