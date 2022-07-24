from PIL import Image
import numpy as np
import cv2
import os

# get the file_dir of the current working directory
file_full_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_full_path)

file_name = "lena.bmp"
result_name = "result.jpg"

img = Image.open(os.path.join(file_dir, file_name))
width, height = img.size
#print(img.size)
#img.show()

def upside_down(img):
	result = Image.new(img.mode, img.size)
	for y in range(height//2): # 0-255
		for x in range(width): # 0-511
			up = img.getpixel((x, y))
			down = img.getpixel((x, height - 1 - y)) # 512 - 1 - y :511,510,509.....,256
		
			result.putpixel((x, height - 1 - y), up)
			result.putpixel((x, y), down)

	result.show()
	return result

def right_side_left(img):
	result = Image.new(img.mode, img.size)
	for y in range(height): # 0-511
		for x in range(width//2): # 0-255
			left = img.getpixel((x, y))
			right = img.getpixel((width - 1 - x, y))
			
			result.putpixel((width - 1 - x, y), left)
			result.putpixel((x, y), right)

	result.show()
	return result

def diagonally_mirrored(img):
	result = Image.new(img.mode, img.size)
	for y in range(height):
		for x in range(width - y):
			a = img.getpixel((x, y))
			b = img.getpixel((width - 1 - x, height - 1 - y))
			
			result.putpixel((width - 1 - x, height - 1 - y), a)
			result.putpixel((x, y), b)

	result.show()
	return result

def rotate(img):
	result = img.rotate(45)
	result.show()
	return result

def shrink(img):
	x, y = int(width/2) ,int(height/2)
	result = img.resize((x,y))
	result.show()
	return result

def binarize(img):
	im = np.array(img.convert('L'))
	th = 128
	im_bin_128 = (im > th) * 255
	# print(im_bin_128)
	result = Image.fromarray(np.uint8(im_bin_128))
	result.show()
	return result
	
def upside_down2(img):
	img_new = np.zeros(img.shape)
	
	# for y in range(height): 
	# 	temp = img[y,:]
	# 	img_new[height-y-1,:] = temp
	# cv2.imwrite('test.jpg',img_new)

	img = img.tolist()
	for y in range(height//2):
		temp = img[y]
		img[y] = img[height-y-1]
		img[height-y-1] = temp		
	img = np.asarray(img)
	cv2.imwrite(os.path.join(file_dir, result_name),img)

if __name__ == '__main__':

# arr = np.array([[1,2,3],
# 				[4,5,6],
# 				[7,8,9]])

# temp = arr[0]
# print('First temp = arr[0] =  ',temp)
# arr[0] = arr[2]
# print('If arr[0] and temp share same memory: ',np.may_share_memory(arr[0], temp))
# print('After arr[0] asign to arr[2], temp = arr[0] =  ',temp)
# arr[2] = temp
# print('Final arr = \n',arr)

	img2 = cv2.imread(os.path.join(file_dir, file_name))
	upside_down2(img2)

# upside_down(img).save("lena_upside_down.bmp")
# right_side_left(img).save("lena_right_side_left.bmp")
# diagonally_mirrored(img).save("lena_diagonally_flip.bmp")
# rotate(img).save("lena_rotate45.bmp")
# shrink(img).save("lena_shrink.bmp")
# binarize(img).save("lena_binarize.bmp")