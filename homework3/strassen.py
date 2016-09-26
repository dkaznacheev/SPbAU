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
	c1 = np.hstack((c11, c12))
	c2 = np.hstack((c21, c22))
	return np.vstack((c1, c2))

def read_array(n):
	arr = []
	for i in range(n):
		s = input()                            
		arr.append([int(x) for x in s.split(' ')])
	arr = np.array(arr)
	return arr            

def add_zeros(a, n):
	cn = 2 ** ((n - 1).bit_length())
	if n != cn:
		a = np.hstack((a, np.zeros(n * (cn - n)).reshape(n, cn - n)))
		a = np.vstack((a, np.zeros((cn - n) * cn).reshape(cn - n, cn)))
	return a
                  
n = int(input())                          
a = read_array(n)
b = read_array(n)                         
a = add_zeros(a, n)
b = add_zeros(b, n)

c = multiply(a, b)[:n, :n].astype(int)
for line in c:
	print(' '.join(str(x) for x in line))
