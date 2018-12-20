import numpy as np
import matplotlib.pyplot as plt

class Neuron:
    # Voltage:=[mV]
    # conductances:=[mS/cm2]
    Cm=20
    gl=2
    EL=-60
    gca=4.4
    Eca=120
    gk=8.0
    Ek=-84
    V1=-1.2
    V2=18
    V3=2
    V4=30
    phi=0.04

    def __init__(self,V0):
        self.V=V0
        self.n=0

    def calc(self,I):
        Nss=(1+np.tanh((self.V-self.V3)/self.V4))
        Mss=(1+np.tanh((self.V-self.V1)/self.V2))
        V_next=(I-self.gl*(self.V-self.EL)-self.gca*Mss*(self.V-self.Eca)-self.gk*self.n*(self.V-self.Ek))/self.Cm+self.V
        n_next=(Nss-self.n)*self.phi*np.cosh((self.V-self.V3)/(2*self.V4))+self.n
        self.V=V_next
        self.n=n_next
        return(self.V)

    def get_V(self):
        return self.V

    def get_n(self):
        return self.n

#%% calc
#シミュレート設定
#tは時間、Iは電流値[mA]

t = 200
I = 200
Nu=Neuron(-40)

x = np.linspace(0,t,t)
y= []
y.append(Nu.get_V())
for i in range(t-1):
    y.append(Nu.calc(I))


plt.plot(x,y,label='Test')
plt.savefig('MLNeuron.png')
#print(y)

#%%n-Vgraph

sim_neuron=Neuron(-40)
sim_V=[]
sim_n=[]
sim_n.append(sim_neuron.get_n())
sim_V.append(sim_neuron.get_V())


for i in range(t):
    sim_V.append(sim_neuron.calc(200))
    sim_n.append(sim_neuron.get_n())

plt.plot(sim_V,sim_n,label='n-V')
plt.savefig('MLNeuron-nV.png')
