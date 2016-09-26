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
     	                                                                           
	c = np.empty(num * num).astype(a.dtype).reshape(num, num)
	for i in range(half):
		for j in range(half):
			c[i][j] = p1[i][j] + p4[i][j] - p5[i][j] + p7[i][j]
			c[i][j + half] = p3[i][j] + p5[i][j]
			c[i + half][j] = p2[i][j] + p4[i][j]
			c[i + half][j + half] = p1[i][j] - p2[i][j] + p3[i][j] + p6[i][j]
	return c

def read_array(n):
	a = np.empty(n * n).astype(int).reshape(n, n)	
	for i in range(n):
		s = input()                            
		a[i] = [int(x) for x in s.split(' ')]
	return a

def resize_array(a, n):
	cn = 2 ** ((n - 1).bit_length())
	if n != cn:
		a = np.hstack((a, np.zeros(n * (cn - n)).astype(a.dtype).reshape(n, cn - n)))
		a = np.vstack((a, np.zeros((cn - n) * cn).astype(a.dtype).reshape(cn - n, cn)))
	return a
	
            
n = int(input())                          

a = read_array(n)
b = read_array(n)                                            
a = resize_array(a, n)                                       
b = resize_array(b, n)
c = multiply(a, b)[:n, :n]
for line in c:
	print(' '.join(str(x) for x in line))
