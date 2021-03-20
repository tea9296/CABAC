import numpy as np


def bins2dec(bins):
    count=1
    x =0.0
    for bin in bins:
        x = x + bin*0.5/count
        count*=2
    return x

def readProb10bits(bins):
    x = 0
    count = 1
    numb = 10
    #if len(bins) <numb:
    #    bitsNum = len(bins)
    #else:
    #    bitsNum = numb
    while len(bins) < numb:
        bins.append(0)

    for i in range(numb):

        x = x + bins[numb-i-1]*count
        count *= 2
    return x, numb

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
    return pModel


def Encode(binStrs):
    #binStr = "10101111"
    pModel = ProbabilityModel()
    encodeProbCodes = []
    ### for exch block###
    for binStr in binStrs:
        MPS = '0'
        idxP = 0
        intervalStart = 0
        intervalRange = 1024
        res = []
        bitOutstand = 0
        for binValue in binStr:
            intervalRangeLPS = pModel[idxP] * intervalRange
            intervalRange = intervalRange - intervalRangeLPS
            if binValue == int(MPS):
                # intervalRange = intervalRange - (intervalRange*pModel[idxP])  ###R(i+1) = R(i) - R(LPS)
                # intervalStart = intervalStart
                if idxP <= 62:
                    idxP += 1

            else:
                intervalStart = intervalStart + intervalRange
                intervalRange = intervalRangeLPS
                if idxP > 0:
                    idxP -= 1
                elif idxP == 0:
                    if MPS == '0':
                        MPS = '1'
                    else:
                        MPS = '0'

            ### renormalization ###
            while intervalRange < 256:
                if intervalStart < 256:
                    res.append(0)
                    while bitOutstand > 0:
                        res.append(1)
                        bitOutstand -= 1
                    intervalStart = int(intervalStart * 2)
                    intervalRange = int(intervalRange * 2)
                elif intervalStart >= 512:
                    intervalStart = int(intervalStart - 512)
                    res.append(1)
                    while bitOutstand > 0:
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
        intervalRange = intervalRange - 2
        intervalStart = intervalStart + intervalRange
        intervalRange = 2

        while intervalRange < 256:
            if intervalStart < 256:
                res.append(0)
                while bitOutstand > 0:
                    res.append(1)
                    bitOutstand -= 1
                intervalStart = int(intervalStart * 2)
                intervalRange = int(intervalRange * 2)
            elif intervalStart >= 512:
                intervalStart = int(intervalStart - 512)
                res.append(1)
                while bitOutstand > 0:
                    res.append(0)
                    bitOutstand -= 1
                intervalStart = int(intervalStart * 2)
                intervalRange = int(intervalRange * 2)
            elif intervalStart < 512:
                intervalStart = int(intervalStart - 256)
                intervalStart = int(intervalStart * 2)
                intervalRange = int(intervalRange * 2)
                bitOutstand += 1

        if intervalStart / 512 >= 1:
            res.append(1)
            while bitOutstand > 0:
                res.append(0)
                bitOutstand -= 1
        else:
            res.append(0)
            while bitOutstand > 0:
                res.append(1)
                bitOutstand -= 1
        if intervalRange / 128 >= 2:
            res.append(1)
        else:
            res.append(0)


        encodeProbCodes.append(res)

    return encodeProbCodes



####decoding########
def Decode(encodeProbCodes, encodeBitsNum):

    decodeCode = []
    pModel = ProbabilityModel()
    for encodeProbCode in encodeProbCodes:
        prob, bits = readProb10bits(encodeProbCode)
        intervalRange = 1024
        intervalRangeLPS = 0
        MPS = '0'
        idxP = 0
        ans = []
        for count in range(encodeBitsNum):
            intervalRangeLPS = int(pModel[idxP] * intervalRange)
            intervalRange = intervalRange - intervalRangeLPS
            if prob >= intervalRange:
                if MPS == '0':
                    ans.append(1)
                else:
                    ans.append(0)
                prob = prob - intervalRange
                intervalRange = intervalRangeLPS
                # intervalStart = intervalStart + (intervalRange - (intervalRange*pModel[idxP]))
                # intervalRange = intervalRange*pModel[idxP]

                if idxP > 0:
                    idxP -= 1
                elif idxP == 0:
                    if MPS == '0':
                        MPS = '1'
                    else:
                        MPS = '0'


            else:
                ans.append(int(MPS))
                # intervalRange = intervalRange - (intervalRange*pModel[idxP])  ###R(i+1) = R(i) - R(LPS)
                # intervalStart = intervalStart

                if idxP <= 62:
                    idxP += 1

            ###renormalization###

            while intervalRange < 256:
                intervalRange = intervalRange * 2
                bits += 1
                prob = (prob * 2)
                if bits <= len(encodeProbCode):
                    prob = prob + encodeProbCode[bits - 1]
                # print(prob)

        """
        ### decode terminate
        intervalRange = intervalRange - 2
        if prob >= intervalRange:
            ans.append(1)
        else:
            ans.append(0)
            while intervalRange < 256:
                intervalRange = intervalRange*2
                #print(prob)
                bits += 1
               #print("res"+str(res))
                prob = (prob * 2)
                if bits <= len(res):
                    prob = prob + res[bits-1]

        """

        decodeCode.append(ans)
    return decodeCode
