import numpy as np
import cv2
import encode
import time




def FixedLengthBinarization(element, length):
    result = []
    value = 2**(length-1)
    for i in range(length):
        if element/value >=1:
            element = element - value
            result.append(1)
        else:
            result.append(0)
        value /= 2
    return result

def GenerateBineryToDecimal(decodeCode):
    result = []

    for binStr in decodeCode:
        pixelValue = 0
        value = 2 ** (len(decodeCode[0]) - 1)
        for bin in binStr:
            pixelValue = pixelValue + bin*value
            value /= 2
        result.append(pixelValue)
    return result


img = cv2.imread("pic1.jpg")
blockSize = 8



### Change picture into grayscale and 1D array
grayPic = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
syntaxElements = np.array(grayPic.flatten())

n, m = grayPic.shape[0], grayPic.shape[1]

print("Picture length and width: "+str(grayPic.shape))
print("Picture size: "+str(np.size(grayPic))+" bytes")
### Binarization
binStrs = []
for i in syntaxElements:
    binStrs.append(FixedLengthBinarization(i, 8))


### encode and decode ###
start = time.time()
encodeProbCodes = encode.Encode(binStrs)
decodeCode = encode.Decode(encodeProbCodes, blockSize)

end = time.time()
print("execute time: "+str(end - start))
count=0
for i in range(len(encodeProbCodes)):
    count += len(encodeProbCodes[i])
print("Compressed size: "+str(count/8) + " bytes")
### regenerate picture ###

result = np.array(GenerateBineryToDecimal(decodeCode)).reshape(n, m)
cv2.imwrite('result.jpg', result)
