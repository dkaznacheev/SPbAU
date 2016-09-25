import numpy as np
import math

def mu(a, b):
	num = np.shape(a)[0]
	if num <= 2:
		return np.dot(a, b)
	half = num // 2	
	a11 = a[:half, :half].copy()
	a12 = a[:half, half:].copy()
	a21 = a[half:, :half].copy()
	a22 = a[half:, half:].copy()
	b11 = b[:half, :half].copy()
	b12 = b[:half, half:].copy()
	b21 = b[half:, :half].copy()
	b22 = b[half:, half:].copy()
           
	p1 = mu(a11 + a22, b11 + b22)
	p2 = mu(a21 + a22, b11)
	p3 = mu(a11, b12 - b22)
	p4 = mu(a22, b21 - b11)
	p5 = mu(a11 + a12, b22)
	p6 = mu(a21 - a11, b11 + b12)
	p7 = mu(a12 - a22, b21 + b22)

	c11 = p1 + p4 - p5 + p7
	c12 = p3 + p5
	c21 = p2 + p4
	c22 = p1 - p2 + p3 + p6
	c1 = np.hstack((c11, c12))
	c2 = np.hstack((c21, c22))
	return np.vstack((c1, c2))
    

n = int(input('Enter n:\n'))

print('Enter matrices:\n') 
a = []
for i in range(n):
	s = input()                            
	a.append([int(x) for x in s.split(' ')])
a = np.array(a)
                                      
b = []
for i in range(n):
	s = input()                            
	b.append([int(x) for x in s.split(' ')])
b = np.array(b)            

cn = pow(2, math.ceil(math.log(n, 2)))
if n != cn:
	a = np.hstack((a, np.zeros(n * (cn - n)).reshape(n, cn - n)))
	a = np.vstack((a, np.zeros((cn - n) * cn).reshape(cn - n, cn)))
	b = np.hstack((b, np.zeros(n * (cn - n)).reshape(n, cn - n)))
	b = np.vstack((b, np.zeros((cn - n) * cn).reshape(cn - n, cn)))

c = mu(a, b)

for line in c:
	for num in line:
		print(num, end = ' ')
	print()
