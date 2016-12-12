# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import urllib
import requests
import time
import re

from lib.spider import Spider
from lib.util import *

class Weibo(Spider):
	def __init__(self, path):
		super(Weibo, self).__init__(path)
		print '\n in Weibo __init__'
		self.config['base_url'] = "http://m.weibo.cn/page/json?containerid=100505"\
			+ str(self.config['uid']) + "_-_WEIBO_SECOND_PROFILE_WEIBO&page="
	# end

	def _get_params(self, index, page):
		print '\n in Weibo _get_params. \n'
		return str(page)
	# end

	def _check_more(self, text):
		if text.find('"mod_type":"mod\/pagelist"') > 0:
			return True
		else:
			return False
	# end

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
	# end

	def _before_loop_file_v1(self):
		self.process = dict()
		self.process['url'] = dict()
		self.process['topic'] = dict()
		self.process['imgs'] = list()
		self.process['source'] = dict()
		self.wbs_info = list()
		self.content = ""
	# end

	def _get_loop_data_v1(self, text):
		data = json.loads(''.join(text))
		if data['cards'][0]['mod_type'] == "mod/empty":
			print '\n\t no data'
			return []
		return data['cards'][0]['card_group']
	# end

	def _loop_item_v1(self, item):
		""" 循环每一条微博 """
		item = item['mblog']
		# 正文
		if 'text' in item:
			# 还有表情、@、转发 需要处理
			self.content += item['text'] + '\n'

		# 图片
		if 'pics' in item and len(item['pics']) > 0:
			for pic in item['pics']:
				self.process['imgs'].append({
					'time': item['created_timestamp'],
					'url': re.sub(r'sinaimg\.cn\/(.+?)\/', 'sinaimg.cn/large/', pic['url'])
				})

		# 定位、外链
		if 'url_struct' in item and len(item['url_struct']) > 0:
			for loc in item['url_struct']:
				url_type = re.findall(r'card_(.+?).png$', loc['url_type_pic'])
				if len(url_type) == 0:
					continue
				url_type = url_type[0]
				if url_type not in self.process['url']:
					self.process['url'][url_type] = dict()
				if loc['url_title'] not in self.process['url'][url_type]:
					self.process['url'][url_type][loc['url_title']] = 0
				self.process['url'][url_type][loc['url_title']] += 1

		# 话题
		if 'topic_struct' in item and len(item['topic_struct']) > 0:
			for top in item['topic_struct']:
				t_title = top['topic_title']
				if t_title not in self.process['topic']:
					self.process['topic'][t_title] = 0
				self.process['topic'][t_title] += 1

		# 设备
		if 'source' in item:
			source = item['source']
			if source not in self.process['source']:
				self.process['source'][source] = 0
			self.process['source'][source] += 1

		self._one_wb_info(item)
	# end

	def _one_wb_info(self, item):
		# id、日期、时间、转发、评论、点赞、配图个数
		time_obj = time.localtime(item['created_timestamp'])
		wb_time = time.strftime("%Y-%m %H.%M", time_obj).split(' ')
		wb = dict()
		wb['a_idstr'] = item['idstr']
		wb['b_date'] = wb_time[0]
		wb['c_time'] = wb_time[1]
		wb['d_reposts'] = item['reposts_count']
		wb['e_comments'] = item['comments_count']
		wb['f_like'] = item['like_count']
		wb['g_imgs'] = len(item['pic_ids'])
		wb['h_week'] = time.strftime("%w", time_obj)
		self.wbs_info.append(wb)
	# end

	def _after_loop_file_v1(self):
		root_path = self.config['dump_dir']
		wbs_info_txt = list_to_tab_str(self.wbs_info, "idstr\tdate\ttime\treposts"\
			+ "\tcomments\tlike\timgs\tweek")
		output_v1(root_path, 'wb_info.txt', wbs_info_txt)
		# output_v1(root_path, 'wb_info.json', self.wbs_info)
		output_v1(root_path, 'content.txt', self.content)
		output_v1(root_path, 'url.json', self.process['url'])
		output_v1(root_path, 'topic.json', self.process['topic'])
		output_v1(root_path, 'imgs.json', self.process['imgs'])
		output_v1(root_path, 'source.json', self.process['source'])
	# end

	def download_img_v1(self, pic_list):
		""" pic_list: [{
				"url": "http://ww4.sinaimg.cn/large/7cba7d.jpg",
				"time": 1449534237
			}, {}]
		"""
		path = self.config['dump_dir'] + '/img/'
		check_path(path)
		headers = self._get_header_v1()
		for x in pic_list:
			time_array = time.localtime(x['time'])
			created_at = time.strftime("%Y-%m-%d-%H.%M.%S", time_array)
			img_name = path + created_at + '.jpg'
			download = False
			while download is False:
				response = requests.get(x['url'], headers=headers)
				code = response.status_code
				if code == 200:
					data = response.content
					f = file(img_name, "wb")
					f.write(data)
					f.close()
					print x['url'] + ' download completed!'
					download = True
				elif code == 403:
					print "forbidden"
					headers = self._get_header_v1()
	# end

	def data_clean(self):
		# 去掉html标签，提取：@
		# 表情统一处理：[]
		# 标签不需要关注，已从结构化数据中提取
		# re.sub(r'<+.+<\/.>', '', test)
		#
		# 转发
		# 含有 retweeted_status
		# re.sub(r'\/\/+.*', '', test1)
		pass
	# end

	def get_user_info(self):
		""" 获取用户个人主页信息 """
		url = self.config['user_url'] + str(self.config['uid']) \
			+ '_-_INFO&title=%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF&'\
			+ 'uid=' + str(self.config['myid'])
		headers = self._get_header_v1()
		response = self.simple_request_v1(url, headers, '')
		output_v1(self.config['dump_dir'], 'user_info.json', json.loads(response.text))
	# end

# end class


if __name__ == '__main__':
	weibo = Weibo('config.ini')
	# weibo.get_data()
	# weibo.extract_v1()
	# imgs_list = init(weibo.config['dump_dir']  + '/imgs.json')
	# weibo.download_img_v1(imgs_list)
	weibo.get_user_info()
	print '\n\n\t\t done!!! \n\n'


