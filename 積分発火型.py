
#%% imports
import numpy as np
import matplotlib.pyplot as plt

#%% Voltage:=mV

def neuron(x,I):
    tau = 5
    Vt = x
    Er = -70
    Vthr = 10
    V0 = Er-5
    if(x>Vthr):
        return V0
    else:
        return(((tau-1)*Vt+Er+I)/tau)

#%% calc
t = 200

x = np.linspace(0,t,t)
y= [-70]
for i in range(t-1):
    if(i<50):
        y.append(neuron(y[i],100))
    else:
        y.append(neuron(y[i],0))


# %% plots
#print(y)

plt.plot(x,y,label='Test')
plt.savefig('積分発火型.png')
