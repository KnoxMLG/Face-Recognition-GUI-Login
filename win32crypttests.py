import time
import win32crypt

tes=[]
string='100'
i=0

while i<10000:
    tes.append(string+str(i))
    i+=1
start=time.time()
for s in tes:
    win32crypt.CryptProtectData(s.encode('utf-8'), None, None, None, None, 0)
end=time.time()
print(end-start)

#takes 1/10000th of a second to compute a single encryption on my local machine (O(n))

l=0
while l<len(tes):
    tes[l]=win32crypt.CryptProtectData(tes[l].encode('utf-8'), None, None, None, None, 0)
    l+=1

start2=time.time()
for m in tes:
    (win32crypt.CryptUnprotectData(m, None)[1]).decode("utf-8")
end2=time.time()

print(end2-start2)

#takes 0.00008 to decrypt a single string on local machine (O(n))

'''
conclusions:
for datasets <1000000 large, it should be computationally okay to check every entry
i wont have to worry pepokay
'''