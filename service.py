def mprint(m1):
    m = [[i2 for i2 in i] for i in m1]
    l=[0 for i in range(0,len(m[0]))]
    for i in range(0,len(m)):
        for i2 in range(0,len(m[i])):
            m[i][i2]=str(m[i][i2])
            ll=len(m[i][i2])
            if ll>l[i2]:
                l[i2]=ll;
    for i in range(0,len(m)):
        for i2 in range(0,len(m[i])):
            ll = len(m[i][i2])
            if ll < l[i2]:
                a=l[i2]-ll
                m[i][i2]=m[i][i2]+' '*a
    for i in range(0,len(m)):
        for i2 in range(0,len(m[i])):
            print(m[i][i2], end=" | ")
        print("")

def mrange(start,end,step=1):
    if step<0:
        return [n for n in range(start, end-1, step)]
    return [n for n in range(start,end+1,step)]

def mcopy(matrix):
    li=len(matrix)
    lj=len(matrix[0])
    newM=[[matrix[i][i2] for i2 in range(0, lj)] for i in range(0, li)]
    return newM

def norma(f,h):
    sum=0
    for fn in f:
        sum=sum+fn**2
    sum=sum*h
    sum=sum**(1/2)
    return sum

def shodimost(sigma,delta_t,h):
    a_plus_c=2*sigma*delta_t/h**2
    b= 1+ 2*sigma*delta_t/h**2
    if a_plus_c<b:return True;