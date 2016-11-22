# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

from talk import Talk
from note import Note
from weibo import Weibo

if __name__ == '__main__':
	talk = Talk('./talk/config.ini')
	talk.get_data()

	note = Note('./note/config.ini')
	note.get_data()

	weibo = Weibo('./weibo/config.ini')
	weibo.get_data()


