# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

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
			return True
		return False
	# end

# end


if __name__ == '__main__':
	zhihu = Zhihu('config.ini')
	zhihu.get_data_v2()
