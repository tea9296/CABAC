import numpy as np
from decimal import Decimal
def dec2bin(x):
    x -= int(x)
    bins = []
    while x:
        x *= 2
        bins.append(1 if x>=1. else 0)
        x -= int(x)
    return bins

def bins2dec(bins):
    count=1
    x =0.0
    for bin in bins:
        x = x + bin*0.5/count
        count*=2
    return x

def ProbabilityModel():
    pModel =[]
    prob = 0.5
    alpha = 0.95
    for i in range(64):
        if i == 0:
            pModel.append(prob)
        else:
            prob = prob*alpha
            pModel.append(prob)
    print(pModel)
    return pModel



binStr = "00001001000000100010101010101111"
print(len(binStr))
pModel = ProbabilityModel()
MPS = '0'
idxP = 0
### for exch block###
intervalStart = 0
intervalRange = 1024
res = []
bitOutstand=0
for binValue in binStr:
    if binValue == MPS:
        intervalRange = intervalRange - (intervalRange*pModel[idxP])  ###R(i+1) = R(i) - R(LPS)
        intervalStart = intervalStart
        if idxP <= 62:
            idxP += 1

    else:
        intervalStart = intervalStart + (intervalRange - (intervalRange*pModel[idxP]))
        intervalRange = intervalRange*pModel[idxP]
        if idxP > 0:
            idxP -= 1
        elif idxP == 0:
            if MPS == '0':
                MPS = '1'
            else:
                MPS = '0'

    ### renormalization not finished ###
    while intervalRange < 256:
        if intervalStart < 256:
            res.append(0)
            if bitOutstand>0:
                res.append(1)
                bitOutstand -= 1
            intervalStart = int(intervalStart*2)
            intervalRange = int(intervalRange*2)
        elif intervalStart >= 512:
            intervalStart = int(intervalStart - 512)
            res.append(1)
            if bitOutstand > 0:
                res.append(0)
                bitOutstand -= 1
            intervalStart = int(intervalStart * 2)
            intervalRange = int(intervalRange * 2)
        elif intervalStart < 512:
            intervalStart = int(intervalStart - 256)
            intervalStart = int(intervalStart * 2)
            intervalRange = int(intervalRange * 2)
            bitOutstand += 1


### end of encoding ###
intervalStart = intervalStart + intervalRange
intervalRange = 2

while intervalRange < 256:
    if intervalStart < 256:
        res.append(0)
        if bitOutstand > 0:
            res.append(1)
            bitOutstand -= 1
        intervalStart = int(intervalStart * 2)
        intervalRange = int(intervalRange * 2)
    elif intervalStart >= 512:
        intervalStart = int(intervalStart - 512)
        res.append(1)
        if bitOutstand > 0:
            res.append(0)
            bitOutstand -= 1
        intervalStart = int(intervalStart * 2)
        intervalRange = int(intervalRange * 2)
    elif intervalStart < 512:
        intervalStart = int(intervalStart - 256)
        intervalStart = int(intervalStart * 2)
        intervalRange = int(intervalRange * 2)
        bitOutstand += 1

if intervalStart/512 >= 1:
    res.append(1)
else:
    res.append(0)

print(intervalRange)
print(intervalStart)
print(res)
print(len(res))
print(bins2dec(res))
"""
### find shortest value in interval ###
print(dec2bin(intervalStart+intervalRange))
print(dec2bin(intervalStart))
endLi = dec2bin(intervalStart+intervalRange)
startLi = dec2bin(intervalStart)
res=[]
for i in range(len(endLi)):
    if endLi[i] != startLi[i]:
        res.append(startLi[i])
        while startLi[i+1] != 0:
            res.append(1)
            i = i+1
        res.append(1)
        break
    else:
        res.append(startLi[i])

print(res)
print(bins2dec(res))
"""






"""

####decoding########

#prob = bins2dec(res)
prob = (intervalRange/2+intervalStart)
MPS = '0'
idxP = 0
intervalStart = 0
intervalRange = 1024
ans = []
for count in range(16):
    if prob < intervalStart + pModel[idxP]*intervalRange:
        ans.append(int(MPS))
        intervalRange = intervalRange - (intervalRange*pModel[idxP])  ###R(i+1) = R(i) - R(LPS)
        intervalStart = intervalStart

        if idxP <= 62:
            idxP += 1

    else:
        if MPS == '0':
            ans.append(1)
        else:
            ans.append(0)
        intervalStart = intervalStart + (intervalRange - (intervalRange*pModel[idxP]))
        intervalRange = intervalRange*pModel[idxP]

        if idxP > 0:
            idxP -= 1
        elif idxP == 0:
            if MPS == '0':
                MPS = '1'
            else:
                MPS = '0'


#print(ans)
"""