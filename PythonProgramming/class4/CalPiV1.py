#CallPiV1
pi = 0
N = 100
for k in range(N): 
	pi+=1/pow(16,k)*(\
		4/(8*k+1)-2/(8*k+4)-\
		1/(8*k+5)-1/(8*k+6))
print("π={:.48f}".format(pi))