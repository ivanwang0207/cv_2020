from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


img = Image.open("lena.bmp")
img.show()
width, height = img.size

def histogram(img):
	im = np.array(img)
	arr = im.flatten()
	
	plt.hist(arr, bins=256, facecolor='black')
	plt.savefig("lena_histogram.jpg")
	plt.show()  
	return 0

def intensity_divided(img):
    im = np.array(img)
    arr = im.flatten()
    arr = arr / 3

    plt.hist(arr, bins=256, range=(0,256), facecolor='black')
    plt.savefig("lena_intensity_divided.jpg")
    plt.show()  

    arr = arr.reshape([512,512])
    result = Image.fromarray(np.uint8(arr))
    result.show()

    return result

def histogram_equalization(img):
	im = np.array(img)
	arr = im.flatten()
	count = {}
	for i in arr: # 利用dict計算每個灰階值出現幾次
		if i not in count.keys():
			count[i] = 1
		else:
			count[i] += 1
	count = sorted(count.items())
	
	cdf = {}
	x = 0
	for i in count: # 轉換成累積分佈函數cdf值
		x += i[1]
		cdf[i[0]] = x
	cdf_min = min(cdf.values())
	cdf_max = max(cdf.values())

	for i, c in cdf.items(): # 均衡化
		i_equa = (c - cdf_min)/(cdf_max-cdf_min) * 255
		cdf[i] = int(i_equa)
	arr_equa = [] 
	for i in arr:
		arr_equa.append(cdf[i])
	arr_equa = np.array(arr_equa)	
	
	plt.hist(arr_equa, bins=256, range=(0,256), facecolor='black')
	plt.savefig("lena_equalization.jpg")
	plt.show() 

	arr_equa = arr_equa.reshape([512,512])
	result = Image.fromarray(np.uint8(arr_equa))
	result.show()

	return result


histogram(img)
intensity_divided(img).save("lena_intensity_divided.bmp")
histogram_equalization(img).save("lena_equalization.bmp")