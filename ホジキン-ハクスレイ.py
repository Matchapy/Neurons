import numpy as np
import matplotlib.pyplot as plt

'''
Hudgkin-Huxley方程式を元に実装
http://www.hi.is.uec.ac.jp/rcb/paper/PDF/H18_wada.pdf
数値は上記のサイトから引用
'''
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
        #計算部分
        alp_m=0.1*(40+self.V)/(1-np.exp(-(40+self.V)/10))
        beta_m=4*np.exp(-(self.V+65)/18)
        alp_h=0.07*np.exp(-(self.V+65)/20)
        beta_h=1/(1+np.exp(-(self.V+35)/10))
        alp_n=0.01*(self.V+55)/(1-np.exp(-(self.V+55)/10))
        beta_n=0.125*np.exp(-(self.V+65)/80)

        m_next=(alp_m*(1-self.m)-beta_m*self.m)*self.delta_t+self.m
        h_next=(alp_h*(1-self.h)-beta_h*self.h)*self.delta_t+self.h
        n_next=(alp_n*(1-self.n)-beta_n*self.n)*self.delta_t+self.n

        self.INa=self.gNa*(self.m**3)*self.h*(self.V-self.ENa)
        self.Ik=self.gk*(self.n**4)*(self.V-self.Ek)
        self.IL=self.gL*(self.V-self.EL)
        V_next=((-1*(self.INa+self.Ik+self.IL)+I)/self.C)*self.delta_t+self.V

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
I = 80
Nu=Neuron(-50)

x = np.linspace(0,t,t)
y= []
y.append(Nu.get_V())
for i in range(t-1):
    y.append(Nu.calc(I))

    #print(Nu.get_params())

plt.plot(x,y,label='Test')
plt.savefig('Hudgkin-Huxley.png')
fig=plt.figure()
#print(y)
