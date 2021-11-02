

import ipaddress

#class MyIpAddressFuncs:
def myReverseMask(strMask):
    arrOctetsResults = []
    arrOctets = strMask.split(".")
    for i in arrOctets:
        #print('i:'+i)
        i = 255 - int(i)
        arrOctetsResults.append(str(i))
    return '.'.join(arrOctetsResults)

def MaskToCidr(strMask):
    intMaskLength = str(sum([bin(int(x)).count("1") for x in strMask.split(".")]))
    return intMaskLength



if __name__ == '__main__':
    #miaf = MyIpAddressFuncs()
    output = myReverseMask('255.255.192.0')
    print(output)