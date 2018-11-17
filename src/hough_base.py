import cv2
import numpy as np


def find_center(img_list):

    for img in img_list:
        # 转到HSV空间
        image = cv2.imread(img)
        hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 用颜色分割图像 取出红色的像素
        low_range = np.array([156, 80, 100])
        high_range = np.array([180, 255, 255])

        # inRange得到的是二值图像 在范围内的像素置为白色 范围之外的设为黑色
        th = cv2.inRange(hue_image, low_range, high_range)

        # 膨胀
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)

        circles = cv2.HoughCircles(dilated, cv2.HOUGH_GRADIENT, 1, 50, param1=15, param2=7, minRadius=5, maxRadius=20)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(image, (i[0], i[1]), 1, (255, 255, 0), 1)
            cv2.imshow("Image", image)
        
        cv2.waitKey(3000)

    cv2.destroyAllWindows()


img_list = ['./data/0.png', './data/1.png', './data/3.png', './data/4.png']
# img_list = ['./data/3.png']
find_center(img_list)

