from PIL import Image
import numpy as np 

a = np.array(Image.open('fcity.jpg').convert('L'))
b = 255 - a
im = Image.fromarray(b.astype('uint8'))
im.save('city3.jpg')