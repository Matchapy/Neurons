import numpy as np
import matplotlib.pyplot as plt

class Freq_Counter:
    '''
    閾値電圧に対する立ち下がりを検知し、周波数を測定する
    '''

    def __init__(self,Vthr):
        self.V_prev=None
        self.counter=0
        self.detected=[]
        self.Vthr=Vthr

    def update(self,V):
        if self.V_prev is None:
            self.V_prev=V
        elif (self.V_prev>self.Vthr and V<self.Vthr):
            #print(self.counter)
            self.detected.append(self.counter)

        self.V_prev=V
        self.counter+=1

    def get_Freq(self):
        if(len(self.detected)<2):
            print('There is not enough data.')
            return 0

        diff=np.diff(self.detected)
        T_mean=sum(diff)/len(diff)
        freq=1/T_mean
        return freq

def simulate(I,t):
    neuro=Neuron(-40)
    freq_count=Freq_Counter(0)
    for i in range(t):
        freq_count.update(neuro.calc(I))

    return(freq_count.get_Freq())


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
I = 100
Nu=Neuron(-40)
fc=Freq_Counter(0)

x = np.linspace(0,t,t)
y= []
y.append(Nu.get_V())
for i in range(t-1):
    Vnow=Nu.calc(I)
    fc.update(Vnow)
    y.append(Vnow)


plt.plot(x,y,label='Test')
print(str(fc.get_Freq())+'Hz')
print(fc.detected)
#plt.savefig('MLNeuron.png')
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

#%%Freq-I Graph

Freqs=[]
Is=[]
for I in range(10,200,2):
    #print(I)
    Is.append(I)
    Freqs.append(simulate(I,1000))

plt.plot(Is,Freqs,label='Fq-I')
plt.savefig('MLNeuron-FqI.png')
