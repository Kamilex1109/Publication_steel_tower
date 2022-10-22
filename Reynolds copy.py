import math

z = [0, 8.57143, 17.14286, 25.71429, 34.28571, 42.85714, 51.42857, 60]
Przekroj_elementu = "LR 101.3x5"
stefa_wiatru = 1
a = 300
C_dir = 1
C_season = 1
p = 1.25
kategoria_terenu = 0


l_dlugosc = 30

def predkosc_wiatru(stefa_wiatru, a):
    if int(stefa_wiatru)==1:
        if int(a)>300:
            v_b0 = 22*(1+0.0006*(int(a)-300))
        else:
            v_b0 = 22
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
    return v_b0 

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

def predkosc_wiatru_v_m_z(q_p_z):
    v_m_z = math.sqrt((2 * q_p_z) / p)
    return v_m_z

Przekroj = Przekroj_elementu
b_rury = float(Przekroj[3:6]) / 1000
v_b0 = predkosc_wiatru(stefa_wiatru, a)
v_b = bazowa_predkosc_wiatru(C_season,C_dir, v_b0)
q_b = wartosc_bazowa_cisnienia_predkosci(p, v_b)
z_min1 = z_min(kategoria_terenu)
z_max1 = z_max(kategoria_terenu)
z_01 = z_0(kategoria_terenu)
A_c_z = []          # podkrytyczny
A_c_sup_z = []      # nadkrytyczny
A_f_z = []
y_test = 0
while y_test < (len(z)-1):
    if y_test < (len(z)-1):
        print(z)
        print(v_b0)
        wysokosc_z1 = wysokosc_z(z[y_test])
        C_e_z = wspolczynnik_ekspozycji(kategoria_terenu,wysokosc_z1)
        q_p_z = wartosc_szczytowa_cisnienia(C_e_z, q_b)
        v_m_z = predkosc_wiatru_v_m_z(q_p_z)
        A_c_z.append(0)
        A_c_sup_z.append(0)
        A_f_z.append(0)
        if Przekroj[0:2] == "RO":
            Re = (b_rury * (15 * (10 ** (-6)))) / v_m_z
            if Re <= (4 * (10 ** 5)):
                A_c_z_n = b_rury * l_dlugosc
                A_c_z[y_test] = 2 * A_c_z_n
            else:
                A_c_sup_z_n = b_rury * l_dlugosc
                A_c_sup_z[y_test] = 2 * A_c_sup_z_n
        elif Przekroj[0:2] == "LR":
            A_f_z_n = b_rury * l_dlugosc
            A_f_z[y_test] = 2 * A_f_z_n
    else:
        break
    y_test += 1 
Pola = []
Pola.append(A_c_z)
Pola.append(A_c_sup_z)
Pola.append(A_f_z)
print(Pola)
