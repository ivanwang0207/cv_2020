from PIL import Image
import numpy as np


def ConvertToBinary(originImg):
    binaryImage = Image.new('1', originImg.size)
  
    for c in range(originImg.size[0]):
        for r in range(originImg.size[1]):
            originalPixel = originImg.getpixel((c, r))
            if (originalPixel >= 128):
                binaryImage.putpixel((c, r), 1)
            else:
                binaryImage.putpixel((c, r), 0)
    return binaryImage


def downsampling(originImg, factor):

    downsamplingImage = Image.new('1', (64,64))
    for c in range(0, originImg.size[0], factor):
        for r in range(0, originImg.size[1], factor):
            # take the topmost-left pixel as the downsampled data
            downsamplingImage.putpixel((int(c/factor), int(r/factor)), originImg.getpixel((c, r)))

    return downsamplingImage


def neighborhoodPixels(originImg, curPos):
    #define the neighborhood array size
    nbPixs = np.zeros(9)
    #current position in the image
    x, y = curPos

    for dx in range(3):
        for dy in range(3):
            #calculating the position x,y in the image
            posX = x + (dx - 1)
            posY = y + (dy - 1)
            # Check if the pixel is out of boundary 
            if ((0 <= posX < originImg.size[0]) and (0 <= posY < originImg.size[1])):
                # store the position in neighborhood array
                nbPixs[3 * dy + dx] = originImg.getpixel((posX, posY))
            else:
                nbPixs[3 * dy + dx] = 0
    return nbPixs

def hFunc(b, c, d, e):

    if ((b == c) and (b != d or b != e)):
        return 'q'
    if ((b == c) and (b == d and b == e)):
        return 'r'
    if (b != c):
        return 's'

def fFunc(a1, a2, a3, a4):

    if ([a1, a2, a3, a4].count('r') == 4):
        # Return label 5 (interior)
        return 5
    else:
        # Return count of 'q'
        return [a1, a2, a3, a4].count('q')
        

def YokoiConnectivityNumber(originImg, i):

    Yokoi_init_list = [[ " " for x in range(originImg.size[0])] for y in range(originImg.size[1])]
    Yokoi_arr = np.array(Yokoi_init_list) #defined a 2d array to store the result

    for c in range(originImg.size[0]):
        for r in range(originImg.size[1]):
            if (originImg.getpixel((c, r)) != 0):
                # Get neighborhood pixel values.
                nbPixs = neighborhoodPixels(originImg, (c, r))
                Yokoi_arr[r, c] = fFunc(
                    hFunc(nbPixs[4], nbPixs[5], nbPixs[2], nbPixs[1]), 
                    hFunc(nbPixs[4], nbPixs[1], nbPixs[0], nbPixs[3]), 
                    hFunc(nbPixs[4], nbPixs[3], nbPixs[6], nbPixs[7]), 
                    hFunc(nbPixs[4], nbPixs[7], nbPixs[8], nbPixs[5]))
            else:
                Yokoi_arr[r, c] = ' '

    with open('Yokoi' + str(i) + '.txt', "w") as txt_file:
        for line in Yokoi_arr:
            txt_file.write("".join(line) + "\n") # works with any number of elements in a line

    return Yokoi_arr

def mark_pair_relationship(Yokoi_arr, i):
    #print (Yokoi_arr.shape)
    trans_yokoi_arr = Yokoi_arr

    kernel = np.array([[0, 1, 0],[1, 1, 1],[0, 1, 0]])  
    kernelCenterX = kernel.shape[0]//2
    kernelCenterY = kernel.shape[1]//2

    img_pair_list = [[ " " for x in range(trans_yokoi_arr.shape[0])] for y in range(trans_yokoi_arr.shape[1])]
    img_pair = np.array(img_pair_list) #defined a 2d array to store the result

    for x  in range(trans_yokoi_arr.shape[0]):
        for y in range(trans_yokoi_arr.shape[1]):
            if (trans_yokoi_arr[x,y] == '1'):
                for a in range(kernel.shape[0]):
                    for b in range(kernel.shape[1]):
                        if (kernel[a,b] == 1):
                            kx = x + (a - kernelCenterX) 
                            ky = y + (b - kernelCenterY)                            
                            if ((0 <= kx < trans_yokoi_arr.shape[0]) and (0 <= ky < trans_yokoi_arr.shape[1])):                            
                                if (trans_yokoi_arr[kx, ky] == '1'):
                                    if ((kx == x and ky == y) != True):
                                        img_pair[x,y] = 'p'


    with open('marked' + str(i) + '.txt', "w") as txt_file:
        for line in img_pair:
            txt_file.write("".join(line) + "\n") 

    return img_pair.T


def thinning_operator(originImg, i):
    
    yokoi_arr = YokoiConnectivityNumber(originImg, i)
    img_pair = mark_pair_relationship(yokoi_arr, i)    

    for c in range(originImg.size[0]):
        for r in range(originImg.size[1]):
            if (img_pair[c,r] == "p"):
                nbPixs = neighborhoodPixels(originImg, (c, r))
                temp = fFunc(
                    hFunc(nbPixs[4], nbPixs[5], nbPixs[2], nbPixs[1]), 
                    hFunc(nbPixs[4], nbPixs[1], nbPixs[0], nbPixs[3]), 
                    hFunc(nbPixs[4], nbPixs[3], nbPixs[6], nbPixs[7]), 
                    hFunc(nbPixs[4], nbPixs[7], nbPixs[8], nbPixs[5]))
                if (temp == 1):
                    originImg.putpixel((c,r), 0)  
    return originImg


def isEqualImage(image1, image2):
    for c in range(image1.size[0]):
        for r in range(image1.size[1]):
            if (image1.getpixel((c, r)) != image2.getpixel((c, r))):
                return False
    return True



if __name__ == '__main__':

    originImg = Image.open('lena.bmp')
    # Get binary image.
    binaryImg = ConvertToBinary(originImg)
    binaryImg.save('binary.bmp')

    # Get downsampling image.
    dsaImg = downsampling(binaryImg, 8)
    dsaImg.save('downsampling.bmp')

    i = 0
    img = dsaImg

    while (True):
        i = i + 1
        origin = img.copy()
        thinning = thinning_operator(img, i)
        
        if (isEqualImage(thinning, origin)):
            thinning.save("iter" + str(i) + ".bmp")
            break
        img = thinning.copy()

