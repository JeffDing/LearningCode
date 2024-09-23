from PIL import Image
import numpy as np 

a = np.array(Image.open('fcity.jpg').convert('L'))
b = 255*(a/255)**2 #像素平方
im = Image.fromarray(b.astype('uint8'))
im.save('city5.jpg')