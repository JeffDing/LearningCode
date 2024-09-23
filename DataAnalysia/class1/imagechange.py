from PIL import Image
import numpy as np 

a = np.array(Image.open('fcity.jpg'))
print(a.shape,a.dtype)
b = [255,255,255] - a
im = Image.fromarray(b.astype('uint8'))
im.save('city2.jpg')