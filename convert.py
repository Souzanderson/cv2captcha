from PIL import Image
import numpy as np
import cv2
from pdf2image import convert_from_path 
import pytesseract as ocr
import matplotlib.pyplot as plt

class Convert():
    def __init__(self):
        self.image = None
        self.text = ""
        self.isImage = False
        self.imgconvert = None
        # self.values =[()]
        
    def openPDF(self,pdflocale, pages=0):
        try:
            pgs = convert_from_path(pdflocale, 500)
            if pages == 0:
                self.image = pgs[0]
        except Exception as e:
            print(e)
        return self
        
    def openImage(self, imglocale):
        try:
            self.image = cv2.imread(imglocale)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.imgconvert = self.image
            self.isImage = True
        except Exception as e:
            print(e)
        return self

    def applyFilter(self,d,sigmacolor,sigmaspace,c):
        self.image = cv2.bilateralFilter(self.image,d,sigmacolor,sigmaspace,c)

    def clear(self,l_color, h_color, c_sub=[0,0,255]):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(self.image, l_color, h_color)
        self.image[mask != 0] = c_sub
        self.image = cv2.cvtColor(self.image, cv2.COLOR_HSV2RGB) 
        return self
            
    def openAndClearImage(self,imagelocale):
        self.image = cv2.imread(imagelocale)
        self.clear((0, 0, 0),(255, 70, 255))
        return self

    def border(self):
        edges = cv2.Canny(self.image,100,200)
        plt.imshow(edges)
        plt.show()

    def grayScale(self):
        kernel = np.ones((5, 5), np.uint8)
        cv2.erode(self.image, kernel, iterations = 1)
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(gray, 100, 255, 0)
        self.image = thresh
        return self
        
    def show(self):
        plt.imshow(self.image)
        plt.show()

    def openFile(self,locale):
        try:
            if '.pdf' in locale:
                self.openPDF(locale)
            else:
                self.openImage(locale)
                self.isImage = True
        except Exception as e:
            print(e)
        return self
    
    def convert(self):
        try:
            # img = cv2.cvtColor(self.image, cv2.COLOR_HSV2RGB)
            # npimagem = np.asarray(img).astype(np.uint8)
            # npimagem[:, :, 0] = 0 # zerando o canal R (RED)
            # npimagem[:, :, 1] = 0 # zerando o canal G (GREEN)
            # npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)
            # im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)
            # ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 
            # self.imgconvert = Image.fromarray(thresh) 
            # binimagem.show()
            self.text = ocr.image_to_string(self.image)
            return self
        except Exception as e:
            print(e)
            return self
    
    def normalizeText(self):
        try:
            arr = self.text.split("\n")
            ret = []
            for a in arr:
                if a.strip().lstrip()!="":
                    ret.append(a)
            self.text = "\n".join(ret)
        except Exception as e:
            print(e)
        return self
    
    def getList(self):
        try:
            arr = self.text.split("\n")
            arr = [a.split(" ") for a in arr]
            return arr
        except Exception as e:
            print(e)
            return []   
    
    def getText(self):
        try:
            return self.text
        except Exception as e:
            print(e)
            return self.text
    
    def detect(self,value):
        try:
            return (value in self.text)
        except Exception as e:
            print(e)
            return False
    
    def getLayout(self,layout):
        try:
            values = self.getList()
            resp = {}
            for k in layout:
                # resp[k]
                v = values
                for i in layout[k]['pos']:
                    if i == 'F':
                        v= v[-1]
                    else:
                        v = v[i]
                if 'join' in layout[k]:
                    ini = layout[k]['join'][0]
                    fim = layout[k]['join'][1]
                    if fim == "F":
                        fim = len(v)
                    v = " ".join(v[ini:fim])
                resp[k] = v
            return resp
        except  Exception as e:
            print(e)
            return None
        
    def showConvertedImage(self):
        try:
            self.imgconvert.show()
        except:
            raise('Nenhuma imagem detectada!')