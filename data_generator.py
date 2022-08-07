import numpy
import pandas
import scipy.stats
import matplotlib.pyplot as mp

N = 1000 # number of variables
ids = numpy.arange(0,N,1)

# generate a random correlation matrix

gammarvs = scipy.stats.gamma.rvs(size=N,a=0.5,scale=0.01)
eigens = gammarvs/numpy.sum(gammarvs)*N
corrmatrix = scipy.stats.random_correlation.rvs(eigs=eigens)

# generate random means and variances

means = scipy.stats.norm.rvs(size=N,scale=0.005)
variances = scipy.stats.invgamma.rvs(size=N,a=3,scale=0.5)

# generate simulation

Nt = 1000
T = 10
t = numpy.linspace(0,T,Nt) # time index
dt = t[1]-t[0]
X = numpy.zeros((Nt,N))
X[0,:] = 100
for j in range(1,Nt):
    X[j,:] = (X[j-1,:] + means*dt + numpy.matmul(scipy.linalg.cholesky(corrmatrix),
                                                scipy.stats.norm.rvs(size=N))*numpy.sqrt(variances*dt))

# output .json dataset

df = pandas.DataFrame(X,index=t,columns=ids)
df.to_json(r'data.json',orient='columns',date_format='epoch')
