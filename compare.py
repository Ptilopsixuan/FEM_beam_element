import numpy as np

E = 2e11
b = 0.2
h = 0.3
l = 10
A = b * h
I = b * h**3 / 12
s1 = E * A / l
s2 = 12 * E * I / l**3
s3 = 6 * E * I / l**2
s4 = 4 * E * I / l
s5 = 2 * E * I / l
K = [[s1, 0, 0, -s1, 0, 0],
     [0, s2, s3, 0, -s2, s3],
     [0, s3, s4, 0, -s3, s5],
     [-s1, 0, 0, s1, 0, 0],
     [0, -s2, -s3, 0, s2, -s3],
     [0, s3, s5, 0, -s3, s4]]
cl = [3, 4, 5]
K = [[K[i][j] for j in cl] for i in cl]
P = [0, 1e4, 0]
inv = np.linalg.inv(K)
tmp = np.matmul(inv, P).T
result = [np.round(x, 12) for x in tmp]
result = [float(r) for r in result]
print(result)
print(P)
print(K)
