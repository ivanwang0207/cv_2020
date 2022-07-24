import sys
import numpy as np
import cv2

def convolveImg(img, kernel):
    imgX,imgY = img.shape[0],img.shape[1]
    kernelR,kernelC = kernel.shape[0],kernel.shape[1]

    convImg = np.zeros((imgX - kernelR + 1, imgY - kernelC + 1))
    for i in range(convImg.shape[0]):
        for j in range(convImg.shape[1]):
            minR, maxR = i, i + kernelR
            minC, maxC = j, j + kernelC           
            crop = img[minR : maxR, minC : maxC]
            value = 0           
            for r in range(crop.shape[0]):
                for c in range(crop.shape[1]):
                    value += (crop[r, c] * kernel[kernel.shape[0] - r - 1, kernel.shape[1] - c - 1])           
            convImg[i, j] = value
    return convImg

def LaplacianMask1Array(originImg, threshold):
    k = np.array([
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
    ])
    img_ans = convolveImg(originImg, k)
    cv2.imwrite('LaplacianMask1(th=' + str(threshold) + ').bmp', (img_ans < int(threshold)) * 255)

def LaplacianMask2Array(originImg, threshold):
    k = np.array([
        [1., 1, 1],
        [1, -8, 1],
        [1, 1, 1]
    ]) / 3
    img_ans = convolveImg(originImg, k)
    cv2.imwrite('LaplacianMask2(th=' + str(threshold) + ').bmp', (img_ans < int(threshold)) * 255)

def MinVarianceLaplacianArray(originImg, threshold):
    k = np.array([
        [2., -1, 2],
        [-1, -4, -1],
        [2, -1, 2]
    ]) / 3
    img_ans = convolveImg(originImg, k)
    cv2.imwrite('MinVarianceLaplacian(th=' + str(threshold) + ').bmp', (img_ans < int(threshold)) * 255)

def LaplacianOfGaussianArray(originImg, threshold):
    k = np.array([
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
    ])
    img_ans = convolveImg(originImg, k)
    cv2.imwrite('LaplacianOfGaussian(th=' + str(threshold) + ').bmp', (img_ans < int(threshold)) * 255)

def DifferenceOfGaussianArray(originImg, threshold):
    k = np.array([
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
        [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
    ])
    img_ans = convolveImg(originImg, k)
    cv2.imwrite('DifferenceOfGaussian(th=' + str(threshold) + ').bmp', (img_ans >= int(threshold)) * 255)

if __name__ == '__main__':
    img = cv2.imread('lena.bmp', 0)
    LaplacianMask1Array(img, 15)
    #LaplacianMask2Array(img, 15)
    #MinVarianceLaplacianArray(img, 20)
    #LaplacianOfGaussianArray(img, 3000)
    #DifferenceOfGaussianArray(img, 1)
 
