from PIL import Image
import numpy as np 

a = np.array(Image.open('fcity.jpg').convert('L'))
b = (100/255)*a+150   #区间变换
im = Image.fromarray(b.astype('uint8'))
im.save('city4.jpg')