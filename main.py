from convert import Convert

img = Convert().openImage('captcha2.tif')
# img = Convert().openImage('captcha.jpg')
img.applyFilter(5,75,75,None)

img.clear((0,100,100),(180,255,255),[0,0,0]).grayScale()
img.clear((0,0,100),(12,255,255))
img.convert()

print(img.normalizeText().getText())
img.show()
  