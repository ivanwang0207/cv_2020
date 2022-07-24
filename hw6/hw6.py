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
        

def YokoiConnectivityNumber(originImg):

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

    return Yokoi_arr


if __name__ == '__main__':

    originImg = Image.open('lena.bmp')
    # Get binary image.
    binaryImg = ConvertToBinary(originImg)
    binaryImg.save('binary.bmp')

    # Get downsampling image.
    dsaImg = downsampling(binaryImg, 8)
    dsaImg.save('downsampling.bmp')

    # Get Yokoi Connectivity Number
    Yokoi_arr = YokoiConnectivityNumber(dsaImg)

    with open('Yokoi.txt', "w") as txt_file:
        for line in Yokoi_arr:
            txt_file.write("".join(line) + "\n") # works with any number of elements in a line




