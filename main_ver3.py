


e=0.00001
def norma_m(matrix):
    pass
    return 1

def psi_y_max():
    x=0
    psi=108+2*x^2 #ПГУ по Y
    return psi

def alpha_beta_init():
    alpha=[];beta=[];
    pass

def shodimost_po_m(psi_m,j,k,m):
    e1=norma_m(psi_m[j][k][m+1])-norma_m(psi_m[j][k][m])
    if e1<=e: return True
    else: return False;

def shag_2_2_2(psi_m,j,k,m, alpha,beta):
    psi_m[j][k][m + 1]=alpha[j][k][m+1]*psi_m[j][k+1][m+1] + beta[j][k][m+1]
    return psi_m

def shag_2_2_1(alpha,beta,j,k,m, fita,a,b,c): # 2.2.1	Расчет слева направо прогоночных коэффициентов, где альфа и бета рассчитываются по формулам
    #Прогоночные коэффициенты при k=0 вычисляются из левого ГУ по y,которое задано
    
    beta[j][k][m+1]=(fita[j][k][m] - c[j][k][m+1] * beta[j][k-1][m+1] ) / (b[j][k][m+1] + c[j][k][m+1] * alpha[j][k-1][m+1])
    alpha[j][k][m+1]=-1* (a[j][k][m+1] ) / (b[j][k][m+1] + c[j][k][m+1] * alpha[j][k-1][m+1])
    return alpha,beta

def shag_2(psi_n,j,k):
    m = 0
    n = 0
    psi_m=[]
    k_max=0
    # Начальное значение psi_m[j][k][m + 1] при максимальном индексе k=K находится из правого граничного условия по y.
    psi_m[j][k_max][m + 1] = psi_y_max()
    alpha=0;beta=0;
    alpha, beta=alpha_beta_init()
    m=0
    n=0

    # step 2.2.2 Расчет справа налево (индекс k уменьшается) по прогоночному соотношению
    psi_m=shag_2_2_2(psi_m, j, k, m, alpha, beta)
    if shodimost_po_m(psi_m,j,k,m):
        psi_n[j][k][n+1]=psi_m[j][k][m+1]

    return psi_n

