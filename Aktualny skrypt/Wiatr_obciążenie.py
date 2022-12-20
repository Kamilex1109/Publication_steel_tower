# Wczytaj biblioteki Python Standard i DesignScript
import sys
# import clr
# clr.AddReference('ProtoGeometry')
# from Autodesk.DesignScript.Geometry import *
# from cmath import log, log10, sin, sqrt
import math

# Wartości wejściowe do tego węzła będą przechowywane w postaci listy w zmiennych IN.
#dataEnteringNode = IN
# Wstaw kod poniżej tej linii

from cmath import log, log10, sin, sqrt
import math

# ----- DANE WEJŚCIOWE ----
a = 500
stefa_wiatru = 1
C_dir = 1
C_season = 1
p = 1.25
kategoria_terenu = 0
c_s_c_d = 1.1
theta = 0

z = [0, 10, 20, 30, 40, 50, 60]
A_cale = [53.23, 53.23, 53.23, 53.23, 53.23, 54.93]
A_f = [12.165, 12.165, 12.165, 12.165, 12.165, 12.165]
A_c = [0, 0, 0, 0, 0, 0]
A_c_sup = [0, 0, 0, 0, 0, 0]

A_s = []
y=0
while y < len(A_f):
    if y < len(A_f):
        A_suma = A_f[y] + A_c[y] + A_c_sup[y]
        A_s.append(A_suma)
    else:
        break
    y+=1

d_dra = 0.03
A_dra = d_dra * z[1] * 2 + 0.5* d_dra * (z[1] / 0.3)



# ----- Wartość podstawowa bazowej prędkości wiatru -----
v_b0 = 0
if int(stefa_wiatru)==1:
    if int(a)>300:
        v_b0 = 22*(1+0.0006*(int(a)-300))
    else:
        vb0 = 22
elif int(stefa_wiatru)==2:
    if int(a)>300:
        v_b0 = 26
    else:
        v_b0 = 26
elif int(stefa_wiatru)==3:
    if int(a)>300:
        v_b0 = 22*(1+0.0006*(int(a)-300))
    else:
        v_b0 = 22

# ----- Wartość bazowa ciśnienia prędkości wiatru -----
def bazowa_predkosc_wiatru(C_season, C_dir, v_b0):
    v_b = C_dir * C_season * v_b0
    return v_b

def wartosc_bazowa_cisnienia_predkosci(p, v_b):
    q_b = 0.5 * p * v_b ** 2
    return q_b


# ----- Wartość minimalna i maksymalna z od kategorii terenu -----
def z_min(kategoria_terenu):
    if int(kategoria_terenu) == 0:
        Z_min = 1
        return Z_min
    elif int(kategoria_terenu) == 1:
        Z_min = 1
        return z_min
    elif int(kategoria_terenu) == 2:
        Z_min = 2
        return Z_min
    elif int(kategoria_terenu) == 3:
        Z_min = 5
        return Z_min
    elif int(kategoria_terenu) == 4:
        Z_min = 10
        return Z_min
    return Z_min

def z_max(kategoria_terenu):
    if int(kategoria_terenu) == 0:
        Z_max = 200
        return Z_max
    elif int(kategoria_terenu) == 1:
        Z_max = 200
        return Z_max
    elif int(kategoria_terenu) == 2:
        Z_max = 300
        return Z_max
    elif int(kategoria_terenu) == 3:
        Z_max = 400
        return Z_max
    elif int(kategoria_terenu) == 4:
        Z_max = 500
        return Z_max
    return Z_max

def z_0(kategoria_terenu):
    if int(kategoria_terenu) == 0:
        z_0 = 0.003
        return z_0
    elif int(kategoria_terenu) == 1:
        z_0 = 0.01
        return z_0
    elif int(kategoria_terenu) == 2:
        z_0 = 0.05
        return z_0
    elif int(kategoria_terenu) == 3:
        z_0 = 0.3
        return z_0
    elif int(kategoria_terenu) == 4:
        z_0 = 1.0
        return z_0
    return z_0


def wysokosc_z(z):
    if z > z_min1 and z < z_max1:
        z = z
        return z
    elif z < z_min1:
        z = z_min1
        return z
    elif z > z_max1:
        z = z_max1
        return z
    return z

# ----- Współczynnik ekspozycji zależny od kategorii terenu -----
def wspolczynnik_ekspozycji(kategoria_terenu, z1):
    if int(kategoria_terenu) == 0:
        C_e_z = 3.0 * (( z1 / 10) ** 0.17)
        return C_e_z
    elif int(kategoria_terenu) == 1:
        C_e_z = 2.8 * (( z1 / 10) ** 0.19)
        return C_e_z
    elif int(kategoria_terenu) == 2:
        C_e_z = 2.3 * (( z1 / 10) ** 0.24)
        return C_e_z
    elif int(kategoria_terenu) == 3:
        C_e_z = 1.9 * (( z1 / 10) ** 0.26)
        return C_e_z
    elif int(kategoria_terenu) == 4:
        C_e_z = 1.5 * (( z1 / 10) ** 0.29)
        return C_e_z
    return C_e_z

# ----- Wartość szczytowa ciśnienia prędkości wiatru na wysokości z -----
def wartosc_szczytowa_cisnienia(C_e_z, q_b):
    q_p_z = C_e_z * q_b / 1000
    return q_p_z

# ----- Intensywność turbulencji -----
k1 = 1  # zalecana wartość
c_0_z = 1
def intensywnosc_turbulencji(z, z_0):
    I_v_z = k1 / (c_0_z * (math.log(z / z_0)))
    return I_v_z

# ----- Współczynnik wypełnienia -----
def wspolczynnik_wypelnienia(A_cale, A_s):
    fi = A_s / A_cale
    return fi


def wspolczynnik_natarcia_wiatru(A_f, A_c, A_c_sup, A_s, fi):
    def wspolczynnik_K1(A_f, A_c, A_c_sup, A_s):
        K1 = ((0.55 * A_f) / A_s) + ((0.8 * (A_c_sup + A_c)) / A_s)
        return K1
    K1 = wspolczynnik_K1(A_f, A_c, A_c_sup, A_s)
    def wspolczynnik_K2(fi):
        if fi <= 0.2:
            K2 = 0.2
            return K2
        elif fi <= 0.5:
            K2 = fi
            return K2
        elif fi <= 0.8:
            K2 = 1 - fi
            return K2
        elif fi <= 1.0:
            K2 = 0.2
            return K2
    K2 = wspolczynnik_K2(fi)
    K_theta = 1.0 + K1 * K2 * (math.sin(math.radians(2*theta)) ** 2)
    return K_theta

def wspolczynnik_calkowitej_sily(fi, A_f, A_s, A_c, A_c_sup):
    C_1 = 2.25
    C_2 = 1.5
    c_f_0_f = 1.76 * C_1 * (1 - C_2 * fi + fi * fi)
    c_f_0_c = C_1 * (1 - C_2 * fi) + (C_1 + 0.875) * (fi *fi)
    c_f_0_sup = 1.9 - math.sqrt((1 - fi) * (2.8 - 1.14 * C_1 + fi))

    c_f_s_0 = c_f_0_f * (A_f / A_s) + c_f_0_c * (A_c / A_s) + c_f_0_sup * (A_c_sup / A_s)
    return c_f_s_0

def wspolczynnik_sily_na_konstrukcje(c_f_s_0, K_theta):
    c_f_s = c_f_s_0 * K_theta
    return c_f_s

def wspolczynnik_sily_na_wypozenie(q_p_z):
    ro = 1.25
    v_m_z = math.sqrt((2 * q_p_z) / ro)

    Re = (d_dra * (15 * (10 ** (-6)))) / v_m_z
    def wspolczynnik_c_f_A(Re):
        if Re <= (2 * (10 ** 5)):
            c_f_A_0 = 1.2
            return c_f_A_0
        elif Re <= (4 * (10 ** 5)):
            c_f_A_0 = 1.2 + ((Re - (2 * (10 ** 5))) / ((4 * (10 ** 5)) - (2 * (10 ** 5)))) * (0.6 - 1.2)
            return c_f_A_0
        elif Re <= (10 * (10 ** 5)):
            c_f_A_0 = 0.6 + ((Re - (4 * (10 ** 5))) / ((10 * (10 ** 5)) - (4 * (10 ** 5)))) * (0.7 - 0.6)
            return c_f_A_0
        elif Re > (10 * (10 ** 5)):
            c_f_A_0 = 0.7
            return c_f_A_0
    c_f_A_0 = wspolczynnik_c_f_A(Re)

    K_A = 0.8
    psi = 90

    c_f_A = c_f_A_0 * K_A * ((math.sin(math.radians(psi))) ** 2)
    return c_f_A

def wspolczynnik_lacznej_sily(c_f_A, c_f_s):
    c_f = c_f_A + c_f_s
    return c_f

def sila_fw_na_konstrukcje(c_f, q_p_z, A_f):
    F_w = c_s_c_d * c_f * q_p_z * A_f
    return F_w

###### ------ OBLICZENIA ------ #######
v_b = bazowa_predkosc_wiatru(C_season,C_dir, v_b0)
q_b = wartosc_bazowa_cisnienia_predkosci(p, v_b)
z_min1 = z_min(kategoria_terenu)
z_max1 = z_max(kategoria_terenu)
z_01 = z_0(kategoria_terenu)

#### TUTAJ WKLEJKA ####
wynik = []
y_test = 0
while y_test < (len(z)-1):
    if y_test < (len(z)-1):
        A_cale_N = A_cale[y_test]
        A_s_N = A_s[y_test]
        A_f_N = A_f[y_test]
        A_c_N = A_c[y_test]
        A_c_sup_N = A_c_sup[y_test]

        print(z)
        wysokosc_z1 = wysokosc_z(z[y_test])
        C_e_z = wspolczynnik_ekspozycji(kategoria_terenu,wysokosc_z1)
        q_p_z = wartosc_szczytowa_cisnienia(C_e_z, q_b)
        I_v_z = intensywnosc_turbulencji(wysokosc_z1,z_01)
        fi = wspolczynnik_wypelnienia(A_cale_N, A_s_N)
        K_theta = wspolczynnik_natarcia_wiatru(A_f_N, A_c_N, A_c_sup_N, A_s_N, fi)
        c_f_s_0 = wspolczynnik_calkowitej_sily(fi, A_f_N, A_s_N, A_c_N, A_c_sup_N)
        c_f_s = wspolczynnik_sily_na_konstrukcje(c_f_s_0, K_theta)
        c_f_A = wspolczynnik_sily_na_wypozenie(q_p_z)
        c_f = wspolczynnik_lacznej_sily(c_f_A, c_f_s)
        F_w = sila_fw_na_konstrukcje(c_f, q_p_z, A_f_N)
        wynik.append(F_w)
    else:
        break
    y_test += 1


# Przypisz dane wyjściowe do zmiennej OUT.
OUT = wynik

print(OUT)