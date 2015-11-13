import matplotlib.pyplot as plt

GF = [0.01225,0.01198,0.012473,0.01795,0.010092,0.00557,0.012187,0.012283]
uGF = [0.000085,0.000122,0.0002219,0.0,7.79e-05,5.63e-05,5.941e-05,8.477e-05]
lables = ['flat dist, reg geo','wide gaus, reg geo','narrow gaus, reg geo','0.1um TPB','10um TPB','Sample Slit 0.14"','Vert Sample Slit Sections SS']
x = range(1,len(GF)+1)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.errorbar(x,GF,yerr=uGF,fmt='o')
ax.set_xlim(left=0.0,right=len(GF)+1)
ax.set_ylim(bottom=0.0,top=0.02)
ax.set_ylabel('Geometric Factor')
#ax.grid()

plt.show()
