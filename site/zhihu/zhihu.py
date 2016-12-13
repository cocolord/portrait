# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

import matplotlib.pyplot as plt
import pylab as pl

from lib.spider import Spider
from lib.util import *

class Zhihu(Spider):
	"""docstring for Zhihu"""
	def __init__(self, path):
		super(Zhihu, self).__init__(path)
		self.config['base_url'] = self.config['base_url'] + self.config['id'] \
			+ '/activities?include=data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal'\
			+ '%2Csuggest_edit%2Ccontent%2Cvoteup_count%2Ccomment_count%2Ccollapsed_counts'\
			+ '%2Creviewing_comments_count%2Ccan_comment%2Cmark_infos%2Ccreated_time'\
			+ '%2Cupdated_time%2Crelationship.voting%2Cis_author%2Cis_thanked'\
			+ '%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%3F%28target.type%3Danswer'\
			+ '%29%5D.target.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28'\
			+ 'target.type%3Darticle%29%5D.target.column%2Ccontent%2Cvoteup_count'\
			+ '%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count'\
			+ '%2Ccan_comment%2Ccomment_permission%2Ccreated%2Cupdated%2Cupvoted_followees'\
			+ '%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics'\
			+ '%3Bdata%5B%3F%28target.type%3Dcolumn%29%5D.target.title%2Cintro%2Cdescription'\
			+ '%2Carticles_count%2Cfollowers%3Bdata%5B%3F%28target.type%3Dtopic%29%5D.target.'\
			+ 'introduction%3Bdata%5B%3F%28verb%3DMEMBER_COLLECT_ANSWER%29%5D.extra_object'\
			+ '%3Bdata%5B%3F%28verb%3DMEMBER_COLLECT_ARTICLE%29%5D.extra_object&limit=5'
	# end

	def _get_params_v1(self, index):
		pass
	# end

	def _check_more_v1(self, text):
		data = json.loads(text)
		if data['paging']['is_end'] is False:
			self.config['base_url'] = data['paging']['next']
			# process = threading.Thread(target=extract, args=data['data'])
			# process.start()
			return True
		return False
	# end

	def _before_loop_file_v1(self):
		self.verb_dict = dict()
		self.timeline = dict()
	# end

	def _get_loop_data_v1(self, read_data):
		data = json.loads(''.join(read_data))
		return data['data']
	# end

	def _loop_item_v1(self, data):
		""" 循环每一条动态 """
		verb = data['verb']
		if verb not in self.verb_dict:
			self.verb_dict[verb] = dict()
			self.verb_dict[verb]['action_text'] = data['action_text']
			self.verb_dict[verb]['count'] = 0
		self.verb_dict[verb]['count'] += 1
		time = data['created_time']
		if time not in self.timeline:
			self.timeline[time] = get_time_action(data)
	# end

	def _after_loop_file_v1(self):
		root_path = self.config['dump_dir']
		data = sorted(self.verb_dict.iteritems(), key=lambda d:d[1]['count'], reverse=True)
		output_v1(root_path, 'type-verb.json', data)
		timeline = sorted(self.timeline.iteritems(), reverse=True)
		output_v1(root_path, 'timeline-data.json', timeline)
	# end

# end


def get_time_action(data):
	""" 获取一条动态的主要信息 """
	action = dict()
	action['verb'] = data['verb']
	action['name'] = data['action_text']
	if 'title' in data['target']:
		action['title'] = data['target']['title']
	elif 'question' in data['target'] and 'title' in data['target']['question']:
		action['title'] = data['target']['question']['title']
	elif 'name' in data['target']:
		action['title'] = data['target']['name']
	else:
		print '\n in get_time_action'
		print json.dumps(data)
	return  action
# end

def process(data):
	""" 处理动态 """
	if data['verb'] == 'ANSWER_VOTE_UP':
		# 赞同了回答，回答所属的类别
		process_answer(data)
		pass
	elif data['verb'] == 'TOPIC_FOLLOW':
		# 关注了话题
		pass
	elif data['verb'] == 'QUESTION_FOLLOW':
		# 关注了问题
		pass
	elif data['verb'] == 'MEMBER_VOTEUP_ARTICLE':
		# 赞了文章
		pass
	elif data['verb'] == 'ANSWER_CREATE':
		# 回答了问题，问题所属的类别
		pass
	elif data['verb'] == 'MEMBER_COLLECT_ANSWER':
		# 收藏了回答，回答所属的类别
		pass
	elif data['verb'] == 'MEMBER_FOLLOW_COLUMN':
		# 关注了专栏
		pass
	elif data['verb'] == 'MEMBER_FOLLOW_COLLECTION':
		# 关注了收藏夹
		pass
	else:
		print '\n\t the verb not in if-elif \n'
		print json.dumps(data)
# end

def process_answer(data):
	pass
# end


if __name__ == '__main__':
	# zhihu = Zhihu('config.ini')
	# zhihu.get_data_v2()
	# zhihu.extract_v1()
