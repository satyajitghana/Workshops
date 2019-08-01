# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 12:46:07 2019

@author: shadowleaf
"""

#%%
import cv2
import matplotlib.pyplot as plt
import numpy as np

print(cv2.__version__)

#%%
myimage = cv2.imread('knuth.jpg')
myimagegray = cv2.imread('knuth.jpg', cv2.IMREAD_GRAYSCALE)

#%%
print(myimagegray)
print(myimagegray.shape)
print(type(myimagegray))
print(myimagegray.size)

#%%
print(myimage)
print(myimage.shape)
print(type(myimage))
print(myimage.size)

#%% Cropping
#mycropimagegray = myimagegray[:, 0:200]
#cv2.imshow('', mycropimagegray)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#%%
plt.imshow(myimagegray[::-1, ::-1], cmap = 'gray', interpolation = 'bicubic')

#plt.imshow(mycropimagegray, cmap = 'gray', interpolation = 'bicubic')
plt.show()

#%%
#cv2.imshow('my_image', myimage)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#
##%%
#cv2.imshow('', myimagegray)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#
#cv2