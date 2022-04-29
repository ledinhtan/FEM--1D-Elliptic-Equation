# -*- 1D_Elliptic.py -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 05:02:27 2022

@author: Tan Le Dinh
"""

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

"""
Variable - Describe:
nn ............ The number of nodes
ne ............ The number of elements
coord ......... The vector of node coordinates
absembly ...... The matrix of absembly
dcond ......... The Dirichlet condition
fcond ......... The Neumann condition
ke ............ The stiffness matrix of element
pe ............ The vector of element load
gk ............ The global stiffness matrix
gp ............ The global vector of load
q ............. The global vector of displacement
"""
def ffunc(x):
    return -6*x

#%% Preprocessing
ne = 10
nn = ne + 1
coord = np.arange(0,1+1/ne,1/ne)
absembly = np.zeros((ne,2),dtype=int)
for e in range(ne):
    absembly[e, 0] = e + 1
    absembly[e, 1] = e + 2

fcond = np.array([1, -2])
dcond = np.array([nn, -1])

#%% Processing
gk = np.zeros([nn, nn])
gp = np.zeros([nn, 1])

# Compute the global stiffness matrix and the global load vector
for e in range(ne):
    i = absembly[e, 0] 
    j = absembly[e, 1]
    x1 = coord[i-1]
    x2 = coord[j-1]
    # The element stiffness matrix
    ke = 1/abs(x2-x1)*np.array([[1, -1], [-1, 1]])
    # Absembly the stiffness matrix
    gk[i-1, i-1] = gk[i-1, i-1] + ke[0, 0]
    gk[i-1, j-1] = gk[i-1, j-1] + ke[0, 1]
    gk[j-1, i-1] = gk[j-1, i-1] + ke[1, 0]
    gk[j-1, j-1] = gk[j-1, j-1] + ke[1, 1]
    # The element load vector
    pe = abs(x2-x1)/6*np.array([[2*ffunc(x1)+ffunc(x2)],[ffunc(x1)+2*ffunc(x2)]])
    # Absembly the load vector
    gp[i-1] = gp[i-1] + pe[0]
    gp[j-1] = gp[j-1] + pe[1]

# The condition of node
for i in range(fcond.shape[0]-1):
    gp[fcond[i]-1] = gp[fcond[i]-1] + fcond[i+1]
    
for i in range(dcond.shape[0]-1):
    for j in range(nn):
        gp[j] = gp[j] - gk[j, dcond[i]-1]*dcond[i+1]
    for j in range(nn):
        gk[dcond[i]-1,j] = 0.0
        gk[j,dcond[i]-1] = 0.0
    gk[dcond[i]-1,dcond[i]-1] = 1.0
    gp[dcond[i]-1] = dcond[i+1]
    
q = np.linalg.solve(gk,gp)

#%% Post-processing
print('The numerical results compared with the exact solution')

# The exact solution u_exact = x**3 + 2*x - 4
u_exact = coord**3 + 2*coord - 4
head = ['Node', 'Approximate', 'Exact']
node_vector = np.arange(1,nn+1)
data = np.hstack((node_vector[:,None],q, u_exact[:,None]))
print(tabulate(data, headers=head, tablefmt='grid'))
print('The maximum of error: ', max(abs(q-u_exact[:,None]))[0])

plt.plot(coord, q, 'o', label = 'FEM Solution')
plt.plot(coord, u_exact, label = 'Exact Solution')
plt.xlabel('Ox')
plt.ylabel('Oy')
plt.legend(loc=0)
plt.show()
    
plt.savefig('figure.png')


















