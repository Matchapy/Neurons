import numpy as np
import matplotlib.pyplot as plt

'''
Hudgkin-Huxley方程式を元に実装
http://www.hi.is.uec.ac.jp/rcb/paper/PDF/H18_wada.pdf
数値は上記のサイトから引用
'''
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
            self.detected.append(self.counter)

        self.V_prev=V
        self.counter+=1

    def get_Freq(self):
        if(len(self.detected)<2):
            #print('There is not enough data.')
            return 0

        diff=np.diff(self.detected)
        T_mean=sum(diff)/len(diff)
        freq=1/T_mean
        return freq

    def get_count(self):
        return len(self.detected)


class Neuron:
    C=1
    gNa=120
    gk=36
    gL=0.3
    ENa=55
    Ek=-77
    EL=-54.387
    delta_t=0.01

    def __init__(self,V0):
        self.m=0
        self.h=0.6
        self.n=0.4
        self.INa=1
        self.Ik=1
        self.IL=1
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

    def get_h(self):
        return self.h

    def get_m(self):
        return self.m

    def get_params(self):
        return 'V:'+str(self.V)+' INa:'+str(self.INa)+' Ik:'+str(self.Ik)+' IL:'+str(self.IL)+' m:'+str(self.m)+' h:'+str(self.h)+' n:'+str(self.n)

#%% calc
#シミュレート設定
#tは時間、Iは電流値[mA]

t = 2000
t_I=500
I = 100
Nu=Neuron(-50)
freq_counter=Freq_Counter(-10)

x = np.linspace(0,t,t)
y= []
ms=[]
hs=[]
ns=[]
Is=[]

y.append(Nu.get_V())
ms.append(Nu.get_m())
hs.append(Nu.get_h())
ns.append(Nu.get_n())
Is.append(0)
for i in range(t-1):
    now_I=I
    if (i>t_I and i<t_I+100):
        now_I=I
    if (i>t_I+1000 and i<t_I+1100):
        now_I=I
    now_V=Nu.calc(now_I)
    y.append(now_V)
    Is.append(now_I)
    ms.append(Nu.get_m())
    hs.append(Nu.get_h())
    ns.append(Nu.get_n())
    '''
    print('m:'+str(Nu.get_m()))
    print('h:'+str(Nu.get_h()))
    print('n:'+str(Nu.get_n()))
    '''
    freq_counter.update(now_V)
    #print(Nu.get_params())

fig,(ax_I,ax_V,ax_param)=plt.subplots(3,1)
fig.set_figheight(15)
fig.set_figwidth(7)
ax_V.plot(x,y,label='V')
ax_V.set_xlabel('Time')
ax_V.set_ylabel('Voltage')
ax_V.legend()
#plt.savefig('Hudgkin-Huxley.png')
print(str(freq_counter.get_Freq())+'Hz')
#plt.clf()
ax_I.plot(x,Is,label='I')
ax_I.set_xlabel('Time')
ax_I.set_ylabel('Input current')
ax_I.legend()
#plt.savefig('HH-It.png')
#plt.clf()
ax_param.plot(x,ms,label='m')
#plt.savefig('HH-mt.png')
#plt.clf()
ax_param.plot(x,hs,label='h')
#plt.savefig('HH-ht.png')
#plt.clf()
ax_param.plot(x,ns,label='n')
ax_param.set_xlabel('Time')
ax_param.set_ylabel('Gates')
ax_param.set_ylim(0,1.5)
ax_param.legend()
plt.show()
fig.savefig('HH.png')
#print(y)

#%% Fq-Iグラフ
def simulate(I,t):
    Neuro=Neuron(-50)
    fc=Freq_Counter(-10)
    for i in range(t):
        fc.update(Neuro.calc(I))
    #print(fc.get_count())
    return(fc.get_Freq())

Freqs=[]
Is=[]
for I in range(0,200,2):
    #print(I)
    Is.append(I)
    Freqs.append(simulate(I,3000))

plt.plot(Is,Freqs,label='Fq-I')
plt.savefig('HH-FqI.png')
