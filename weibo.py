# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import urllib
import time
import re

from prettytable import PrettyTable as pt

from lib.spider import Spider
from lib.util import *

class Weibo(Spider):
	def __init__(self, path):
		super(Weibo, self).__init__(path)
		print '\n in Weibo __init__'
		self.config['base_url'] = "http://m.weibo.cn/page/json?containerid=100505"\
			+ str(self.config['uid']) + "_-_WEIBO_SECOND_PROFILE_WEIBO&page="
	# end __init__

	def _get_params(self, index, page):
		print '\n in Weibo _get_params. \n'
		return str(page)
	# end _get_params

	def _check_more(self, text):
		if text.find('{"mod_type":"mod\/empty"') > 0:
			return False
		else:
			return True
	# end _check_more

	def _filter(self, text):
		data = json.loads(''.join(text))
		output = ""
		if data['cards'][0]['mod_type'] == "mod/empty":
			print '\n\t no data'
			return ' '
		for item in data['cards'][0]['card_group']:
			if item['mblog'].has_key('text'):
				summary = item['mblog']['text'].replace('\n', '')
				output += summary + '\n'
			pic_ids = item['mblog']['pic_ids']
			if len(pic_ids) != 0:
				self.download_img(pic_ids, item['mblog']['created_timestamp'])
		return output
	# end _filter

	def download_img(self, pic_arr, timestamp):
		"""
		pic_arr: ["图片id", "图片id"]
		timestamp: "1470756132"
		"""
		uri = "http://ww2.sinaimg.cn/large/"
		path = self.config['dump_dir'] + '-filter/'
		time_array = time.localtime(timestamp)
		created_at = time.strftime("%Y-%m-%d-%H.%M.%S", time_array)
		i = 1
		for x in pic_arr:
			img_url = uri + str(x) + '.jpg'
			img_name = created_at + '-' + str(i) + '.jpg'
			print img_name
			urllib.urlretrieve(img_url, path + img_name)
			i += 1
	# end download_img

##############################################################################
##############################################################################
##############################################################################

	def _before_loop_file_v1(self):
		self.process = dict()
		self.process['url'] = dict()
		self.process['topic'] = dict()
		self.process['imgs'] = list()
		self.wbs_info = list()
		self.content = ""
	# end _before_loop_file_v1

	def _get_loop_data_v1(self, text):
		data = json.loads(''.join(text))
		if data['cards'][0]['mod_type'] == "mod/empty":
			print '\n\t no data'
			return []
		return data['cards'][0]['card_group']
	# end _get_loop_data_v1

	def _loop_item_v1(self, item):
		""" 循环每一条微博 """
		item = item['mblog']
		# 正文
		if item.has_key('text'):
			# 还有表情、@、转发 需要处理
			self.content += item['text'] + '\n'

		# 图片
		if len(item['pic_ids']) > 0:
			print item['created_timestamp']
			self.process['imgs'].append({
				'time': item['created_timestamp'],
				'id_list': item['pic_ids']
			})

		# 定位、外链
		if item.has_key('url_struct') and len(item['url_struct']) > 0:
			for loc in item['url_struct']:
				url_type = re.findall(r'card_(.+?).png$', loc['url_type_pic'])[0]
				if not self.process['url'].has_key(url_type):
					self.process['url'][url_type] = dict()
				if not self.process['url'][url_type].has_key(loc['url_title']):
					self.process['url'][url_type][loc['url_title']] = 0
				self.process['url'][url_type][loc['url_title']] += 1

		# 话题
		if item.has_key('topic_struct') and len(item['topic_struct']) > 0:
			for top in item['topic_struct']:
				t_title = top['topic_title']
				if not self.process['topic'].has_key(t_title):
					self.process['topic'][t_title] = 0
				self.process['topic'][t_title] += 1

		self._one_wb_info(item)
	# end _loop_item_v1

	def _one_wb_info(self, item):
		# id、日期、时间、转发、评论、点赞、配图个数
		time_obj = time.localtime(item['created_timestamp'])
		wb_time = time.strftime("%Y-%m-%d %H.%M.%S", time_obj).split(' ')
		wb = dict()
		wb['a_idstr'] = item['idstr']
		wb['b_date'] = wb_time[0]
		wb['c_time'] = wb_time[1]
		wb['d_reposts'] = item['reposts_count']
		wb['e_comments'] = item['comments_count']
		wb['f_like'] = item['like_count']
		wb['g_imgs'] = len(item['pic_ids'])
		self.wbs_info.append(wb)
	# end _one_wb_info

	def _after_loop_file_v1(self):
		root_path = self.config['dump_dir']
		wbs_info_txt = list_to_tab_str(self.wbs_info, "idstr\tdate\ttime\treposts"\
			+ "\tcomments\tlike\timgs")
		output_v1(root_path, 'wb_info.txt', wbs_info_txt)
		output_v1(root_path, 'wb_info.json', self.wbs_info)
		output_v1(root_path, 'content.txt', self.content)
		output_v1(root_path, 'url.json', self.process['url'])
		output_v1(root_path, 'topic.json', self.process['topic'])
		for x in self.process['imgs']:
			self.download_img_v1(x['id_list'], x['time'])
		print '\n\n\t\t done!!! \n\n'
	# end _after_loop_file_v1

	def download_img_v1(self, pic_list, timestamp):
		"""
		pic_list: ["图片id", "图片id"]
		timestamp: "1470756132"
		"""
		uri = "http://ww2.sinaimg.cn/large/"
		path = self.config['dump_dir'] + '/img/'
		check_path(path)
		time_array = time.localtime(timestamp)
		created_at = time.strftime("%Y-%m-%d-%H.%M.%S", time_array)
		i = 1
		for x in pic_list:
			img_url = uri + str(x) + '.jpg'
			img_name = created_at + '-' + str(i) + '.jpg'
			print img_name
			urllib.urlretrieve(img_url, path + img_name)
			i += 1
	# end download_img

# end class


if __name__ == '__main__':
	weibo = Weibo('weibo/config.ini')
	weibo.get_data()
	# weibo.extract()
	weibo.extract_v1()
