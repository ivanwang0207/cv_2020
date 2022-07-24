from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open("lena.bmp")
width, height = img.size

# octogonal 3-5-5-5-3 kernel
octogonal = [
    [-1,2],[0,2],[1,2],
[-2,1],[-1,1],[0,1],[1,1],[2,1],
[-2,0],[-1,0],[0,0],[1,0],[2,0],
[-2,-1],[-1,-1],[0,-1],[1,-1],[2,-1],
    [-1,-2],[0, -2], [1, -2]]
    
J = [[0, 0], [1, 0], [0, -1]]
K = [[0, 1], [-1, 1], [-1, 0]]

def binarize(img_bin):
	im = np.array(img)
	th = 128
	im_bin_128 = (im > th) * 255
	result = Image.fromarray(np.uint8(im_bin_128))
	return result

def dilation(img,kernel):
    im = np.array(img)
    temp = np.zeros((512,512))

    for i in range(width):
        for j in range(height):
            if im[i][j] == 255:
                for point in kernel:
                    x, y = point
                    if (x+i) >= 0 and (x+i) < width and (y+j) >= 0 and (y+j) < height:
                        temp[i+x][j+y] = 255
    result = Image.fromarray(np.uint8(temp))
    # result.show()
    return result

def erosion(img, kernel):
    im = np.array(img)
    temp = np.zeros((512,512))

    for i in range(width):
        for j in range(height):
            temp[i][j] = 255
            for point in kernel:
                x, y = point
                if im[i+x][j+y] != 255 or (x+i) < 0 or (x+i) >= width or (y+j) < 0 or (y+j) >= height :
                    temp[i][j] = 0
                    break
    result = Image.fromarray(np.uint8(temp))
    # result.show()
    return result

def opening(img, kernel):
	return dilation(erosion(img, kernel), kernel)

def closing(img, kernel):
	return erosion(dilation(img, kernel), kernel)

def hit_miss(img):
    im = np.array(img)
    A = np.array(erosion(im, J))
    B = np.array(erosion(255-im, K))
    temp = np.zeros((512,512))

    for i in range(width):
        for j in range(height):
            if B[i][j] == 255 and A[i][j] == 255:
                temp[i][j] = 255
    result = Image.fromarray(np.uint8(temp))
    result.show()
    return result


binarize(img).save("lena_binarize.bmp")
img_bin = Image.open("lena_binarize.bmp") #讀入binarize 的檔案

dilation(img_bin, octogonal).save("lena_dilation.bmp")
erosion(img_bin, octogonal).save("lena_erosion.bmp")
opening(img_bin, octogonal).save("lena_opening.bmp")
closing(img_bin,octogonal).save("lena_closing.bmp")
hit_miss(img_bin).save("lena_hit_miss.bmp")
