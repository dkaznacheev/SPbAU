import numpy as np
import math

def multiply(a, b):
	num = np.shape(a)[0]
	if num <= 2:
		return np.dot(a, b)
	half = num // 2	
	a11 = a[:half, :half]
	a12 = a[:half, half:]
	a21 = a[half:, :half]
	a22 = a[half:, half:]
	b11 = b[:half, :half]
	b12 = b[:half, half:]
	b21 = b[half:, :half]
	b22 = b[half:, half:]
           
	p1 = multiply(a11 + a22, b11 + b22)
	p2 = multiply(a21 + a22, b11)
	p3 = multiply(a11, b12 - b22)
	p4 = multiply(a22, b21 - b11)
	p5 = multiply(a11 + a12, b22)
	p6 = multiply(a21 - a11, b11 + b12)
	p7 = multiply(a12 - a22, b21 + b22)

	c11 = p1 + p4 - p5 + p7
	c12 = p3 + p5
	c21 = p2 + p4
	c22 = p1 - p2 + p3 + p6                                          
	return np.vstack(( np.hstack((c11, c12)) , np.hstack((c21, c22)) ))

def read_array(n):
	cn = 2 ** ((n - 1).bit_length())
	a = np.zeros(n * n).astype(int).reshape(n, n)	
	for i in range(n):
		s = input()                            
		a[i] = [int(x) for x in s.split(' ')]
	if n != cn:
		a = np.hstack((a, np.zeros(n * (cn - n)).astype(int).reshape(n, cn - n)))
		a = np.vstack((a, np.zeros((cn - n) * cn).astype(int).reshape(cn - n, cn)))
	return a
                    
n = int(input())                          

a = read_array(n)
b = read_array(n)                                            

c = multiply(a, b)[:n, :n]
for line in c:
	print(' '.join(str(x) for x in line))
