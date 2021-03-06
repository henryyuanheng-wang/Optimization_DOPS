from autograd import numpy as np
from autograd import grad


def shuffle_data(X, Y):
	p = np.random.permutation(len(X))
	return X[p], Y[p]


def f_theta(theta, Siy, C):
	d = len(Siy)

	# calculate v
	v = np.zeros(d)
	for j in range(d): # u
		for i in range(d): # i
			if Siy[i] == 1 and C[i][j] == 1:
			# if Siy[i] == 1 and j in C[i]:
				v[j] = 1
				break

	return np.dot(theta, v)


def phi_theta(theta, Si, C, alphaz):
	return sum([f_theta(theta, Si[y], C) for y in alphaz])/len(alphaz)


def objective(theta, Ss, zs, C, alphazs):
	res = 0
	N, m = len(Ss), len(Ss[0])
	for i in range(N):
		# calculate hinge loss
		max_loss = 0 
		phi = phi_theta(theta, Ss[i], C, alphazs[i])
		for y in range(m):
			max_loss = max(max((1 if y in alphazs[i] else 0) + \
				f_theta(theta, Ss[i][y], C) - phi, 0), max_loss)
		res += max_loss
	return res


def gradient_descent(theta, Ss, zs, C, alphazs, eta=0.01, iters=1000, print_every=10):
	gradident_fun = grad(objective)
	for i in range(iters):
		# projected gd
		theta -= eta * gradident_fun(theta, Ss, zs, C, alphazs)
		theta[theta < 0] = 0
		if print_every > 0 and (i+1) % print_every == 0:
			print('Iter %d : %s' % (i+1, theta))

	return theta


def dops(X, Y, T, C, m, alpha, init, eta=0.01, iters=1000, print_every=10):
	# config
	M, d = X.shape
	N = int(np.floor(M/m))
	X, Y = shuffle_data(X, Y)
	Ss = [X[i*m:(i+1)*m] for i in range(N)]
	zs = [Y[i*m:(i+1)*m] for i in range(N)]
	maxzs = [e.max() for e in zs] 
	alphazs = [[i for i, e in enumerate(z) if e >= maxz*alpha] for z, maxz in zip(zs, maxzs)]

	# optimize
	theta = gradient_descent(init, Ss, zs, C, alphazs, eta, iters, print_every)
	
	# get result
	res = [f_theta(theta, t, C) for t in T]
	return res, theta, np.argmax(res)
