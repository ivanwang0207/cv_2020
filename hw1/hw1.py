from PIL import Image
import numpy as np
import cv2
import os

# get the file_dir of the current working directory
file_full_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_full_path)

file_name = "lena.bmp"
img = Image.open(os.path.join(file_dir, file_name))
w, h = img.size # (512, 512)

def upside_down(img):
	result = Image.new(img.mode, img.size)
	for y in range(h//2): # 0-255
		for x in range(w
	): # 0-511
			up = img.getpixel((x, y))
			down = img.getpixel((x, h - 1 - y)) 
		
			result.putpixel((x, h - 1 - y), up)
			result.putpixel((x, y), down)

	result.save(os.path.join(file_dir, "lena_upside_down.bmp"))
	#result.show()

def right_side_left(img):
	result = Image.new(img.mode, img.size)
	for y in range(h): # 0-511
		for x in range(w
	//2): # 0-255
			left = img.getpixel((x, y))
			right = img.getpixel((w
		 - 1 - x, y))
			
			result.putpixel((w
		 - 1 - x, y), left)
			result.putpixel((x, y), right)

	result.save(os.path.join(file_dir, "lena_right_side_left.bmp"))
	#result.show()

def diagonally_mirrored(img):
	result = Image.new(img.mode, img.size)
	for y in range(h):
		for x in range(w
	 - y):
			a = img.getpixel((x, y))
			b = img.getpixel((w
		 - 1 - x, h - 1 - y))
			
			result.putpixel((w
		 - 1 - x, h - 1 - y), a)
			result.putpixel((x, y), b)

	result.save(os.path.join(file_dir, "lena_diagonally_flip.bmp"))
	#result.show()

def rotate(img):
	result = img.rotate(45)
 
	result.save(os.path.join(file_dir, "lena_rotate45.bmp"))
	#result.show()

def shrink(img):
	x, y = int(w
/2) ,int(h/2)
	result = img.resize((x,y))
 
	result.save(os.path.join(file_dir, "lena_shrink.bmp"))
	#result.show()

def binarize(img):
	im = np.array(img.convert('L'))
	th = 128
	im_bin_128 = (im > th) * 255
	result = Image.fromarray(np.uint8(im_bin_128))

	result.save(os.path.join(file_dir, "lena_binarize.bmp"))
	#result.show()
	
def upside_down_opencv(img):
	img = img.tolist()
	for y in range(h//2):
		temp = img[y]
		img[y] = img[h-y-1]
		img[h-y-1] = temp		
	img = np.asarray(img)
 
	cv2.imwrite(os.path.join(file_dir, "lena_upside_down.bmp"),img)

if __name__ == '__main__':
	
	upside_down(img)
	right_side_left(img)
	diagonally_mirrored(img)
	rotate(img)
	shrink(img)
	binarize(img)
 
	#img_arr = cv2.imread(os.path.join(file_dir, file_name))
	#upside_down_opencv(img_arr)
