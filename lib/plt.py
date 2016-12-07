# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import numpy as np
import matplotlib.pyplot as plt

def random():
	x = np.arange(1, 10)
	y = x
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	ax1.set_title('Scatter Plot')
	plt.xlabel('X')
	plt.ylabel('Y')
	ax1.scatter(x, y, c='r', marker='o')

	plt.legend('x1')

	plt.show()
	pass


if __name__ == '__main__':
	random()