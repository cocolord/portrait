# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'


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
	return action
# end

def process(data):
	""" 处理动态 """
	if data['verb'] == 'ANSWER_VOTE_UP':
		# 赞同了回答，回答所属的类别
		process_answer(data)
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
	elif data['verb'] == 'TOPIC_FOLLOW':
		# 关注了话题
		pass
	elif data['verb'] == 'QUESTION_FOLLOW':
		# 关注了问题
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