import numpy as np
import matplotlib.pyplot as plt

class Neuron:
    C=1
    gNa=120
    gk=36
    gL=0.3
    INa=1
    Ik=1
    IL=1
    ENa=55
    Ek=-77
    EL=-54.387
    m=0
    h=1
    n=0
    delta_t=0.01



    def __init__(self,V0):
        self.V=V0

    def calc(self,I):
        m_next=(0.1*(40+self.V)/(1-np.exp(-(40+self.V)/10))*(1-self.m)-4*np.exp(-1*(self.V+65)/18)*self.m)*self.delta_t+self.m
        h_next=(0.07*np.exp(-1*(self.V+65)/20)*(1-self.h)-1/(np.exp((35-self.V)/10)+1)*self.h)*self.delta_t+self.h
        n_next=(0.01*(55+self.V)/(1-np.exp(-1*(55+self.V)/10))*(1-self.n)-0.125*np.exp(-1*(self.V+65)/80)*self.n)*self.delta_t+self.n
        self.INa=self.gNa*(self.m**3)*self.h*(self.V-self.ENa)
        self.Ik=self.gk*(self.n**4)*(self.V-self.Ek)
        self.IL=self.gL*(self.V-self.EL)
        V_next=(-1*(self.INa+self.Ik+self.IL)/self.C+I)*self.delta_t+self.V
        self.m=m_next
        self.h=h_next
        self.n=n_next
        self.V=V_next
        return self.V

    def get_V(self):
        return self.V

    def get_n(self):
        return self.n

    def get_params(self):
        return 'V:'+str(self.V)+' INa:'+str(self.INa)+' Ik:'+str(self.Ik)+' IL:'+str(self.IL)+' m:'+str(self.m)+' h:'+str(self.h)+' n:'+str(self.n)

#%% calc
#シミュレート設定
#tは時間、Iは電流値[mA]

t = 2000
I = 100
Nu=Neuron(-50)

x = np.linspace(0,t,t)
y= []
y.append(Nu.get_V())
for i in range(t-1):
    y.append(Nu.calc(I))

    #print(Nu.get_params())

plt.plot(x,y,label='Test')

fig=plt.figure()
#print(y)
