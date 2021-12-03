import numpy as np
from functools import reduce

def get_rotl(n,size=64):
    rotl = np.identity(64,dtype="uint8")
    return np.roll(rotl,-n,axis=0)

def get_shift(n,size=64):
    return np.eye(size,k=n,dtype="uint8")

def get_trans():
    tl = get_rotl(24)^np.identity(64,dtype="uint8")^get_shift(16)
    tr = np.identity(64,dtype="uint8")^get_shift(16)
    bl = get_rotl(37)
    br = get_rotl(37)

    trans = np.block([[tl,tr],[bl,br]])
    
    return trans

def get_mat():
    t = np.identity(128,dtype="uint8")
    t_ = get_trans()

    s = np.zeros((128,128),"uint8")
    for i in range(128):
        s[i] = (t[63]+t[127])%2
        t = t@t_%2
    return s


def list2bitvec(lst):
    bitvec = reduce(lambda p,q: (int(p)<<1)|int(q),lst)
    return bitvec

def gauss_jordan(mat,observed):
    r,c = mat.shape
    assert r==c
    #def square mat size
    n = r
    bitmat = [list2bitvec(mat[i]) for i in range(r)]

    res = [d for d in observed]
    #forward elimination
    pivot = 0
    for i in range(n):
        isfound = False
        for j in range(i,n):
            if isfound:
                check = 1<<(n-i-1)
                if bitmat[j]&check==check:
                    bitmat[j] ^= bitmat[pivot]
                    res[j] ^= res[pivot]
            else:
                check = 1<<(n-i-1)
                if bitmat[j]&check==check:
                    isfound = True
                    bitmat[j],bitmat[pivot] = bitmat[pivot],bitmat[j]
                    res[j],res[pivot] = res[pivot],res[j]
        if isfound:
            pivot += 1
    
    #backward assignment
    for i in range(1,n)[::-1]:
        check = 1<<(n-i-1)
        for j in range(i)[::-1]:
            if bitmat[j]&check==check:
                bitmat[j] ^= bitmat[i]
                res[j] ^= res[i]

    return res
    
def motions2state(motions, mat=get_mat()):
    state = list2bitvec(gauss_jordan(mat,motions))
    return state >> 64, state & 0xFFFFFFFFFFFFFFFF

def motions2seed(motions, mat=get_mat()):
    state = list2bitvec(gauss_jordan(mat,motions))
    return (state >> 64) | ((state & 0xFFFFFFFFFFFFFFFF) << 64)