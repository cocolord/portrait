# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

from lib.spider import Spider
from lib.util import *
import detail


def more(text):
	if text.find('"is_end": false,') > 0:
		return True
	return False
	# data = json.loads(text)
	# if data['paging']['is_end'] is False:
	# 	self.config['base_url'] = data['paging']['next']
	# 	return True
	# return False
# end


class Activities(Spider):
	"""docstring for Activities"""
	def __init__(self, path):
		super(Activities, self).__init__(path)
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
		return more(text)
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
			self.timeline[time] = detail.get_time_action(data)
	# end

	def _after_loop_file_v1(self):
		root_path = self.config['dump_dir']
		data = sorted(self.verb_dict.iteritems(), key=lambda d:d[1]['count'], reverse=True)
		output_v1(root_path, 'type-verb.json', data)
		timeline = sorted(self.timeline.iteritems(), reverse=True)
		output_v1(root_path, 'timeline-data.json', timeline)
	# end

	def get_user_info(self):
		url = "https://www.zhihu.com/people/" + self.config['id'] + "/activities"
		response = self.simple_request_with_header(url, params="")
		output_v1(self.config['dump_dir'], 'people.html', response.text)
	# end

# end


class Followees(Spider):
	"""docstring for Followees"""
	def __init__(self, path, follow_or_fans):
		super(Followees, self).__init__(path)
		if follow_or_fans != 'followees' and follow_or_fans != 'followers':
			print '@params follow_or_fans wrong'
			return False
		self.config['base_url'] += self.config['id'] + '/' + follow_or_fans
		self.config['requests_dir'] = self.config['dump_dir'] + '/requests-' + follow_or_fans
	# end

	def _get_params_v1(self, index):
		return {
			"per_page": 30,
			"include": "data[*].answer_count,articles_count,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics",
			"limit": 30,
			"offset": 30*(index-1)
		}
	# end

	def _check_more_v1(self, text):
		return more(text)
	# end

# end


if __name__ == '__main__':
	# activities = Activities('config.ini')
	# activities.get_data_v2()
	# activities.extract_v1()
	# activities.get_user_info()

	followees = Followees('config.ini', 'followees')
	followees.get_data_v2()

	follower = Followees('config.ini', 'followers')
	follower.get_data_v2()

