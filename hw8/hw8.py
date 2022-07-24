from PIL import Image
import numpy as np
import random, math, csv, os

def GaussianNoise(originImg, amplitude):
    gaussianNoiseImg = Image.new('L', originImg.size)
    for c in range(originImg.size[0]):
        for r in range(originImg.size[1]):
            noisePix = int(originImg.getpixel((c, r)) + amplitude * random.gauss(0, 1))
            if noisePix > 255:
                noisePix = 255
            elif noisePix < 0:
                noisePix = 0
            gaussianNoiseImg.putpixel((c, r), noisePix)
    return gaussianNoiseImg

def SaltAndPepper(originImg, prob):
    saltAndPepperImg = Image.new("L", originImg.size)
    for c in range(originImg.size[0]):
        for r in range(originImg.size[1]):
            randomVal = random.uniform(0, 1)
            if (randomVal <= prob):
                saltAndPepperImg.putpixel((c, r), 0)
            elif (randomVal >= 1 - prob):
                saltAndPepperImg.putpixel((c, r), 255)
            else:
                saltAndPepperImg.putpixel((c, r), originImg.getpixel((c, r)))
    return saltAndPepperImg

def dilation(Img, kernel):
    kernelCenterX = kernel.shape[0]//2 # get the center index of the original image 
    kernelCenterY = kernel.shape[1]//2
    # New image with the same size and 'grayscale' format.
    dilationImg = Image.new('L', Img.size)

    for x in range(Img.size[0]): # iterate the pixels on oringinal image 
        for y in range(Img.size[1]):
            # Record local max with pixel value
            # the initial local max is 0
            localMaxPix = 0
            
            for a in range(kernel.shape[0]): # iterate the pixels on kernel 
                for b in range(kernel.shape[1]):
                    # record the corresponding position of pixel in the original image
                    kX = x + (a - kernelCenterX) 
                    kY = y + (b - kernelCenterY)
                    # check if the position of pixel is out of the range of image 
                    if ((0 <= kX < Img.size[0]) and (0 <= kY < Img.size[1])): 
                        if (kernel[a,b] == 1): # if pixel value == 1 on kernel exactly covers on the original image
                            originPix = Img.getpixel((kX, kY))
                            if (originPix > localMaxPix): #comparing the value of originPix to the existing local max
                                localMaxPix = originPix
            # Paste local max value on original image 
            dilationImg.putpixel((x, y), localMaxPix)

    return dilationImg

def erosion(Img, kernel):
    kernelCenterX = kernel.shape[0]//2 # get the center index of the original image 
    kernelCenterY = kernel.shape[1]//2
    # New image with the same size and 'grayscale' format.
    erosionImg = Image.new('L', Img.size)

    for x in range(Img.size[0]):
        for y in range(Img.size[1]):
            # Record local min with pixel value
            # the initial local min is 255 
            localMinPix = 255

            for a in range(kernel.shape[0]): # iterate the pixels on kernel 
                for b in range(kernel.shape[1]):
                    # record the corresponding position of pixel in the original image
                    kX = x + (a - kernelCenterX)
                    kY = y + (b - kernelCenterY)
                    # check if the position of pixel is out of the range of image 
                    if ((0 <= kX < Img.size[0]) and (0 <= kY < Img.size[1])):
                        if (kernel[a,b] == 1): # if pixel value == 1 on kernel exactly covers on the original image
                            originPix = Img.getpixel((kX, kY))
                            if(originPix < localMinPix): #comparing the value of originPix to the existing local min
                                localMinPix = originPix
            # Paste local min value on original image 
            erosionImg.putpixel((x, y), localMinPix)

    return erosionImg

def opening(Img, kernel):
    openingImg =  dilation(erosion(Img, kernel), kernel)
    return openingImg

def closing(Img, kernel):
    closingImg = erosion(dilation(Img, kernel), kernel)
    return closingImg

def openingThenClosing(Img, kernel):
    return closing(opening(Img, kernel), kernel)

def closingThenOpening(Img, kernel):
    return opening(closing(Img, kernel), kernel)

def boxFilter(originImg, boxWidth, boxHeight):
    kernelCenterX = boxWidth//2
    kernelCenterY = boxHeight//2  
    boxFilterImg = Image.new('L', originImg.size)
    for c in range(originImg.size[0]):
        for r in range(originImg.size[1]):
            boxPixs = []
            for x in range(boxWidth):
                for y in range(boxHeight):
                    destX = c + (x - kernelCenterX)
                    destY = r + (y - kernelCenterY)
                    if ((0 <= destX < originImg.size[0]) and (0 <= destY < originImg.size[1])):
                        originalPix = originImg.getpixel((destX, destY))
                        boxPixs.append(originalPix)
            boxFilterImg.putpixel((c, r), int(sum(boxPixs) / len(boxPixs)))
    return boxFilterImg

def medianFilter(originImg, boxWidth, boxHeight):
    kernelCenterX = boxWidth//2
    kernelCenterY = boxHeight//2  
    medianFilterImg = Image.new('L', originImg.size)
    for c in range(originImg.size[0]):
        for r in range(originImg.size[1]):
            boxPixs = []
            for x in range(boxWidth):
                for y in range(boxHeight):
                    destX = c + (x - kernelCenterX)
                    destY = r + (y - kernelCenterY)
                    if ((0 <= destX < originImg.size[0]) and (0 <= destY < originImg.size[1])):
                        originalPixel = originImg.getpixel((destX, destY))
                        boxPixs.append(originalPixel)
            boxPixs.sort()
            medianPix = boxPixs[len(boxPixs) // 2]
            medianFilterImg.putpixel((c, r), medianPix)
    return medianFilterImg

def SNR(Img, noiseImg):
    mu_s, vs, mu_noise, vn = 0, 0, 0, 0
    w, h = Img.size

    for x in range(w):
        for y in range(h):
            mu_s += Img.getpixel((x, y))
            mu_noise += noiseImg.getpixel((x, y)) - Img.getpixel((x, y))
    mu_s = mu_s / (w * h) / 255
    mu_noise = mu_noise / (w * h) / 255

    for x in range(w):
        for y in range(h):
            vs += (Img.getpixel((x, y))/255 - mu_s)**2
            vn += (noiseImg.getpixel((x, y))/255 - Img.getpixel((x, y))/255 - mu_noise)**2
    vs = vs / (w * h)
    vn = vn / (w * h)

    return 20 * math.log10(math.sqrt(vs) / math.sqrt(vn))

if __name__ == '__main__':
    filename = 'lena.bmp'
    img = Image.open(filename)
    kernel = np.array([
        [0, 1, 1, 1, 0],                 
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1], 
        [0, 1, 1, 1, 0]])
    snr = open('snr.csv', 'w', newline='')
    writer = csv.writer(snr)
    
    for ampl in [10, 30]:
        guassian_noise_img = GaussianNoise(img, ampl)
        guassian_noise_img.save('guassian_noise_' + str(ampl) + '.bmp')
        writer.writerow(['guassian_noise_' + str(ampl), SNR(img, Image.open('guassian_noise_' + str(ampl) + '.bmp'))])

       
        for kernel_size in [3, 5]: 
            boxFilter(guassian_noise_img, kernel_size, kernel_size).save('guassian_noise_' + str(ampl) + '_box_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp')
            medianFilter(guassian_noise_img, kernel_size, kernel_size).save('guassian_noise_' + str(ampl) + '_median_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp')
            writer.writerow(['guassian_noise_' + str(ampl) + '_box_' + str(kernel_size) + 'x' + str(kernel_size), SNR(img, Image.open('guassian_noise_' + str(ampl) + '_box_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp'))])
            writer.writerow(['guassian_noise_' + str(ampl) + '_median_' + str(kernel_size) + 'x' + str(kernel_size), SNR(img, Image.open('guassian_noise_' + str(ampl) + '_median_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp'))])
        
        openingThenClosing(guassian_noise_img, kernel).save('guassian_noise_' + str(ampl) + '_opening_then_closing.bmp' )
        closingThenOpening(guassian_noise_img, kernel).save('guassian_noise_' + str(ampl) + '_closing_then_opening.bmp' )
        writer.writerow(['guassian_noise_' + str(ampl) + '_opening_then_closing', SNR(img, Image.open('guassian_noise_' + str(ampl) + '_opening_then_closing.bmp'))])
        writer.writerow(['guassian_noise_' + str(ampl) + '_closing_then_opening', SNR(img, Image.open('guassian_noise_' + str(ampl)+ '_closing_then_opening.bmp'))])        
    
    for prob in [0.1, 0.05]:
        salt_and_pepper_img = SaltAndPepper(img, prob)
        salt_and_pepper_img.save('salt_and_pepper_' + str(prob) + '.bmp')
        writer.writerow(['salt_and_pepper_' + str(prob), SNR(img, Image.open('salt_and_pepper_' + str(prob) + '.bmp'))])
    
        for kernel_size in [3, 5]: 
            boxFilter(salt_and_pepper_img, kernel_size, kernel_size).save('salt_and_pepper_' + str(prob) + '_box_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp')
            medianFilter(salt_and_pepper_img, kernel_size, kernel_size).save('salt_and_pepper_' + str(prob) + '_median_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp')
            writer.writerow(['salt_and_pepper_' + str(prob) + '_box_' + str(kernel_size) + 'x' + str(kernel_size), SNR(img, Image.open('salt_and_pepper_' + str(prob) + '_box_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp'))])
            writer.writerow(['salt_and_pepper_' + str(prob) + '_median_' + str(kernel_size) + 'x' + str(kernel_size), SNR(img, Image.open('salt_and_pepper_' + str(prob) + '_median_' + str(kernel_size) + 'x' + str(kernel_size) + '.bmp'))])            
        
        openingThenClosing(salt_and_pepper_img, kernel).save('salt_and_pepper_' + str(prob) + '_opening_then_closing.bmp' )
        closingThenOpening(salt_and_pepper_img, kernel).save('salt_and_pepper_' + str(prob) + '_closing_then_opening.bmp' )
        writer.writerow(['salt_and_pepper_' + str(prob) + '_opening_then_closing', SNR(img, Image.open('salt_and_pepper_' + str(prob) + '_opening_then_closing.bmp'))])
        writer.writerow(['salt_and_pepper_' + str(prob) + '_closing_then_opening' , SNR(img, Image.open('salt_and_pepper_' + str(prob) + '_closing_then_opening.bmp'))]) 
        