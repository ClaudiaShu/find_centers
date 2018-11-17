import numpy as np 
import cv2


def findCenter(img_list):

	def axis1(points):
		A = np.array([])
		for i in range(len(points)):
			A = np.append(A, [points[i][0], 1])
		b = points[:, 1]
		A = np.reshape(A, (-1, 2))
		A_ = np.dot(A.T, A)
		b_ = np.dot(A.T, b)

		x = np.linalg.solve(A_, b_)
		return x

	def axis2(points, k):
		A = np.array([])
		for i in range(len(points)):
			A = np.append(A, [points[i][0], 1])
		A = np.append(A, [10000, 0])
		A = np.reshape(A, (-1, 2))
		b = points[:, 1]
		# if k == 0:
		# 	rate =
		b = np.append(b, [-1 / float(k) * 10000])

		A_ = np.dot(A.T, A)
		b_ = np.dot(A.T, b)

		x = np.linalg.solve(A_, b_)

		return x[1]

	for img in img_list:
		pic = cv2.imread(img)
		pic_hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
		low_range = np.array([156, 123, 100])
		high_range = np.array([180, 255, 255])

		th = cv2.inRange(pic_hsv, low_range, high_range)
		dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)

		a = np.array([])

		for i in range(len(dilated)):
			for j in range(len(dilated[0])):
				if dilated[i][j] == 255:
					a = np.insert(a, len(a), [j, i], 0)

		a = np.reshape(a, (-1, 2))
		xmin = np.min(a[:, 0])
		xmax = np.max(a[:, 0])
		ymin = np.min(a[:, 1])
		ymax = np.max(a[:, 1])
		x_aver = float(xmin + xmax) / 2
		y_aver = float(ymin + ymax) / 2

		p1 = np.array([])
		p2 = np.array([])
		p3 = np.array([])
		p4 = np.array([])

		for i in range(len(a)):
			if a[i][0] < x_aver and a[i][1] < y_aver:
				p1 = np.append(p1, [a[i][0], a[i][1]])
			elif a[i][0] > x_aver and a[i][1] < y_aver:
				p2 = np.append(p2, [a[i][0], a[i][1]])
			elif a[i][0] < x_aver and a[i][1] > y_aver:
				p3 = np.append(p3, [a[i][0], a[i][1]])
			elif a[i][0] > x_aver and a[i][1] > y_aver:
				p4 = np.append(p4, [a[i][0], a[i][1]])

		p1 = np.reshape(p1, (-1, 2))
		p2 = np.reshape(p2, (-1, 2))
		p3 = np.reshape(p3, (-1, 2))
		p4 = np.reshape(p4, (-1, 2))

		# 已知四个圆的像素点求垂线
		# 求解交点 即为圆心
		centers = []
		for p in [p1, p2, p3, p4]:
			k1, b1 = axis1(p)
			# if k1 < 0.0001:
			# 	k1 = 0
			# 	b2 = np.sum(p[:, 0])/len(p)
			# 	centers.append([b1, b2])
			# 	continue
			b2 = axis2(p, k1)
			x = (b2 - b1) * k1 / (k1 * k1 + 1)
			y = k1 * x + b1
			centers.append([x, y])

		# 将圆心标注在图上
		for center in centers:
			cv2.circle(pic, (int(center[0]), int(center[1])), 1, (0, 0, 25), 1)

		cv2.imshow('detected' + img, pic)
		cv2.waitKey(5000)

	cv2.destroyAllWindows()


img_list = ['./data/0.png', './data/1.png', './data/3.png', './data/4.png']
# img_list = ['./data/2.png', './data/3.png']
findCenter(img_list)
