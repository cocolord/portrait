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
	if not os.path.isfile(path):
		raise UserWarning("file donot exist")
		return False
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

def output_v1(path, name, text):
	""" 输出 response 内容到文件 """
	check_path(path)
	if name.find('.json') > 0:
		text = json.dumps(text, encoding='UTF-8', ensure_ascii=False)
	file = str(path) + '/' + str(name)
	f = open(file, 'w')
	f.write(text)
	f.close()
# end output

def only_check_path(path):
	# 只是检查这个路径是否存在
	return os.path.exists(path)
# end only_check_path

def dict_to_tab_str(dict_type, head=""):
	""" {{}, {}} """
	for key, value in dict_type.items():
		if type(value) is dict:
			print key
			dict_to_tab_str(value, '\t')
		else:
			print head + "%s \t %s" % (value, key)
# end dict_to_tab_str

def list_to_tab_str(list_data, thead=""):
	""" [{}, {}, {}] """
	content = ""
	content += thead + '\n'
	for dict_data in list_data:
		if not type(dict_data) is dict:
			continue
		items = dict_data.items()
		items.sort()
		for key, value in items:
			content += '%s\t' % value
		content = content.rstrip('\t')
		content += '\n'
	return content
# end list_to_tab_str