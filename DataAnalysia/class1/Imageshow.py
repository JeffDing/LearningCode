from PIL import Image
import numpy as np 

im = np.array(Image.open('beijing.jpg'))

print(im.shape,im.dtype)