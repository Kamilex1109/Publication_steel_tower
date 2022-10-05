# Test pola  
z = [0, 8.57143, 17.14286, 25.71429, 34.28571, 42.85714, 51.42857, 60]

b_rury = 0.2
b_wiezy = 6
A_cale = []
s_anteny = 0.3
h_anteny = 1.5
y=0
b_rury = float(b_rury)
while y < (len(z) - 1):
    if y < (len(z) - 1):
        A_cale_n = (z[2] - z[1]) * (b_wiezy + b_rury)
        A_cale.append(A_cale_n)
    else:
        break
    y+=1
A_cale[len(A_cale)-1] = A_cale[len(A_cale)-1] + (2 * s_anteny + h_anteny)
print(A_cale)