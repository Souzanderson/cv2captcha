import cv2
import matplotlib.pyplot as plt


def clear(hasv_image, l_color, h_color, c_sub=[0,0,255]):
  mask = cv2.inRange(hasv_image, l_color, h_color)
  hasv_image[mask != 0] = c_sub
  return hasv_image

if __name__ == '__main__':
  nemo = cv2.imread('./captcha.jpg')
  nemo = cv2.cvtColor(nemo, cv2.COLOR_BGR2RGB)
  
  hsv_nemo = cv2.cvtColor(nemo, cv2.COLOR_RGB2HSV)

  hsv_nemo = clear(hsv_nemo,(0, 0, 0),(255, 70, 255)) #remove laranja
  # hsv_nemo = clear(hsv_nemo,(110,100,100),(130,255,255))  #remove azul
  final = cv2.cvtColor(hsv_nemo, cv2.COLOR_HSV2RGB)
  plt.imshow(final)
  cv2.imwrite('test.jpg',final)
  plt.show()