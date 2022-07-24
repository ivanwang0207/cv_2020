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

def dilation(img,kernel):
    im = np.array(img)
    temp = np.zeros((512,512))
    for i in range(width):
        for j in range(height):
            if im[i][j] > 0:
                max_v = 0
                for point in kernel:
                    x, y = point
                    if (x+i) >= 0 and (x+i) < width and (y+j) >= 0 and (y+j) < height:
                        if im[x+i][y+j] > max_v:
                            max_v = im[i+x][j+y]
                for point in kernel:
                    x,y = point
                    if (x+i) >= 0 and (x+i) < width and (y+j) >= 0 and (y+j) < height:
                        temp[x+i][y+j] = max_v
    result = Image.fromarray(np.uint8(temp))
    # result.show()
    return result

def erosion(img, kernel):
    im = np.array(img)
    temp = np.zeros((512,512))
    for i in range(width):
        for j in range(height):
            if im[i][j] > 0:
                exist = True
                min_v = 512
                for point in kernel:
                    x, y = point
                    if (x+i) >= 0 and (x+i) < width and (y+j) >= 0 and (y+j) < height:
                        if im[x+i][y+j] == 0:
                            exist = False
                            break
                        if im[x+i][y+j] < min_v:
                            min_v = im[x+i][y+j]
                    else:
                        exist = False
                        break
                if exist:
                    temp[x+i][y+j] = min_v    
    result = Image.fromarray(np.uint8(temp))
    # result.show()
    return result

def opening(img, kernel):
	return dilation(erosion(img, kernel), kernel)

def closing(img, kernel):
	return erosion(dilation(img, kernel), kernel)


dilation(img, octogonal).save("lena_dilation.bmp")
erosion(img, octogonal).save("lena_erosion.bmp")
opening(img, octogonal).save("lena_opening.bmp")
closing(img,octogonal).save("lena_closing.bmp")
