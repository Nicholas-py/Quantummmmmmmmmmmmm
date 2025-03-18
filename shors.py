from setup import h_it_all, circuitmeasure, simulate, draw, statevector,x_it_all,binvar,invbinvar, realcomputer
from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister
from random import randint
from math import log10,log, ceil
from QPE import defractionize
from QFT import QFT, invQFT
from math import pi
from fractions import Fraction
#from qiskit.algorithms import Shor
#from qiskit import IBMQ
#from qiskit.utils import QuantumInstance

def fastexponentmodN(num,pow,N):
  if pow == 1:
    return num
  elif pow == 0:
    return 1
  elif pow % 2 == 0:
    return (fastexponentmodN(num,int(pow/2),N)**2)%N
  else:
    return (fastexponentmodN(num,int(pow/2),N)**2*num)%N


def periodfind(a,N):
  t = 2
  m = a
  while (m*a)%N != 1:
    t += 1
    m = (m*a)%N
    if t >= 10000000:
      return "Screw it. I give up."
  return t


def modexpQ(qc,start,a,N):
  if a == 2 and N == 15:
    qc.swap(2+start,3+start)
    qc.swap(1+start,2+start)
    qc.swap(0+start,1+start)

def fadda(a):
  qc = QuantumCircuit(int(log(a,2))+2)
  abits = "0"+ binvar(a)
  for i in range(len(abits)):
    for j in range(len(abits)-i):
      if abits[j+i] == '1':
        qc.p(pi/(2**j),i)
  U = qc.to_gate()
  U.name = "+"+str(a)
  print(U)
  return U  

def ccfadda(a):
  qc = QuantumCircuit(int(log(a,2))+4)
  qc.append(fadda(a).control().control(),range(int(log(a,2))+4) )
  U = qc.to_gate()
  U.name = "+"+str(a)
  return U

def QFbox(qnum):
  qc = QuantumCircuit(qnum)
  QFT(qc,swaps=True)
  U = qc.to_gate()
  U.name = 'QFT'
  return U

def invQFbox(qnum):
  qc = QuantumCircuit(qnum)
  invQFT(qc,swaps=True)
  U = qc.to_gate()
  U.name = 'invQFT'
  return U


def faddamodn(a,N):
  cs = QuantumRegister(2,name="cs")
  qcount = int(log(a,2))+2
  mc = QuantumRegister(int(log(a,2))+2,name="mc")
  c = QuantumRegister(1,name="c")
  qc = QuantumCircuit(cs,mc,c)
  qc.append(fadda(a).control().control(),[0,1]+list(range(2,mc.size+2)))
  qc.append(fadda(N).inverse(),list(range(2,mc.size+2)))
  qc.append(invQFbox(qcount),range(2,2+qcount))
  qc.cx(-2,-1)
  qc.append(QFbox(qcount),range(2,2+qcount))
  qc.append(fadda(N).control(),[-1]+list(range(2,mc.size+2)))
  qc.append(fadda(a).inverse().control().control(),[0,1]+list(range(2,mc.size+2)))
  qc.append(invQFbox(qcount),range(2,2+qcount))
  qc.x(-2)
  qc.cx(-2,-1)
  qc.x(-2)
  qc.append(QFbox(qcount),range(2,2+qcount))
  qc.append(fadda(a).control().control(),[0,1]+list(range(2,mc.size+2)))

  draw(qc)
  U = qc.to_gate()
  return U

def multaxmodN(a,x,N):
  qcount = int(log(a,2))+2
  x = binvar(x)
  c = QuantumRegister(1)
  x = QuantumRegister(len(x))
  b = QuantumRegister(qcount)
  qc = QuantumCircuit(c,x,b)
  qc.append(QFbox(qcount),range(1+len(x),1+len(x)+qcount))

  for i in range(len(x)):
    qc.append(faddamodn(a,N),[0]+[i]+range(len(x)+1,len(x)+1+qcount))
  qc.append(invQFbox(qcount),range(1+len(x),1+len(x)+qcount))

  draw(qc)
  return qc.to_gate()
def test():
  cs = QuantumRegister(2)
  mc = QuantumRegister(4)
  c = QuantumRegister(1)
  cl = ClassicalRegister(7)  
  qc = QuantumCircuit(cs,mc,c,cl)
  qc.x([0,1,2,4])
  QFT(qc,reg=mc,swaps=True)
  qc.append(faddamodn(4,7),range(7))
  invQFT(qc,reg=mc,swaps=True)
  circuitmeasure(qc,cl,reg=mc)
  draw(qc)
  print('lesim',simulate(qc))
def generalax(a,power,N):
  qc = QuantumCircuit(10)
  for i in range(power):
    pass
    
def cmodexpQgate(a,power,N):
  qc = QuantumCircuit(ceil(log(N,2)))
  for i in range(power):
    if N == 15:
      if a == 2:
        qc.swap(2,3)
        qc.swap(1,2)
        qc.swap(0,1)
      elif a == 4:
        qc.swap(0,2)
        qc.swap(1,3)
      elif a == 7:
        qc.swap(0,1)
        qc.swap(1,2)
        qc.swap(2,3)
        x_it_all(qc)
      elif a == 8:
        qc.swap(0,1)
        qc.swap(1,2)
        qc.swap(2,3)
      elif a == 11:
        qc.swap(0,2)
        qc.swap(1,3)
        x_it_all(qc)
      elif a == 13:
        qc.swap(3,2)
        qc.swap(2,1)
        qc.swap(1,0)
        x_it_all(qc)
      elif a == 14:
        x_it_all(qc)
    elif N == 4:
      if a == 3:
        qc.cx(0,1)
    else:
      print('Those numbers currently not supported')
      raise NotImplementedError()
  U = qc.to_gate()
  U.name = "U^"+str(power)
  return U.control()

def gcd(a,b):
  assert isinstance(a+b,int)
  if b>a:
    a,b = b,a
  if a%b == 0:
    return b
  else:
    return gcd(b,a%b)

def shors(N,gcds=False,factors=False,cheat=False):
  if cheat:
    raise DeprecationWarning("Obsolete!!!")
    provider = IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
    backend = provider.get_backend('stabilizer_simulator')

    quantum_instance = QuantumInstance(backend, shots=1024)
    shor = Shor(quantum_instance=quantum_instance)
    result = shor.factor(N)
    print(f"The list of factors of {N} as computed by the Shor's algorithm is {result.factors[0]}.")



  for i in range(2,30):
    if gcd(N,i) != 1 and factors:
      print('Factor',i,'found through trial division')
      return i
  while True:
    a = randint(2,N-1)
    if gcds:
      print('Guess:',a)
      x = gcd(N,a)
      if x != 1:
        return x
    else:
      while gcd(N,a) != 1:
        a = randint(2,N-1)
      print('Guess:',a)
    r = qperiodfind(a,N,ceil(log(N,2)))
    if isinstance(r,str):
      return 'Number too large'
    print('QPeriod:',r, '('+str(periodfind(a,N))+')')
    if r%2 == 0:
      guess1 = fastexponentmodN(a,int(r/2),N)-1
      guess2 = guess1+2
      if guess1 > 1000000000000000000000000000000:
        print('a**r/2: ~10^'+str(int(log10(guess1))))
      else:
        print('a**r/2 %N:',guess1+1)
      try:
        x1 = gcd(N,guess1)
        x2 = gcd(N,guess2) 
      except ZeroDivisionError:
        return
      print('Guesses:',int(x1),int(x2))
      if x1 != 1 and x1 != N:
        return int(x1)
      if x2 != 1 and x2 != N:
        return int(x2)

def qperiodfind(a,N,precision,draww=False,oneshot=True,bigsim = False):
  measurebits = QuantumRegister(precision,name='a')
  gatebits = QuantumRegister(ceil(log(N,2)),name='x^a mod N')
  cbits = ClassicalRegister(precision)
  qc = QuantumCircuit(measurebits,gatebits,cbits)
  h_it_all(qc,reg=measurebits)
  qc.x(precision)
  for i in range(precision-1,-1,-1):
    qc.append(cmodexpQgate(a,2**(precision-i-1),N),[precision-i-1]+[precision+j for j in range(ceil(log(N,2)))])
  qc.barrier()
  invQFT(qc,reg=measurebits,swaps=True)
  qc.barrier()
  circuitmeasure(qc,cbits,reg=measurebits)
  if draww:
    draw(qc)
  if oneshot:
    if bigsim:
      a = realcomputer(qc,device='simulator_stabilizer',shots = 1).results()
    else: 
      a = simulate(qc,False,1)
    print(a)
    if len(list(a.keys())[0]) != 5:
      draw(qc)
    b = defractionize(list(a.keys())[0])
    return Fraction(b).limit_denominator(N).denominator
  else:
    if bigsim:
      a = realcomputer(qc,device='simulator_stabilizer',shots = 100).results()
    else: 
      a = simulate(qc,False,100)
    newa = {defractionize(k[::-1]): v for k, v in a.items()}
    newa = dict(sorted(newa.items(),key=lambda x:x[1]))
    newa =dict(reversed(list(newa.items())))
    rs = []
    for i in newa.keys():
      if newa[i] > 2:
        rs += [Fraction(i).limit_denominator(N).denominator]
    return max(rs)


def mod21a5(inp):
  qc = QuantumCircuit(10)
  qc.x(0)
  qc.x(1)
  qc.ccx(0,1,9)
  qc.x(0)
  qc.x(1)
  qc.barrier()
  qc.cx(1,8)
  qc.x(4)
  qc.x(0)
  qc.mct([0,1,2,3,4],8)
  qc.x(4)
  qc.x(3)
  qc.x(2)
  qc.mct([0,1,2,3,4],8)
  qc.x(3)
  qc.x(2)
  qc.x(0)
  qc.barrier()
  qc.cx(4,7)
  qc.ccx(0,1,7)
  qc.x(1)
  qc.x(3)
  qc.ccx(1,3,7)
  qc.x(3)
  qc.x(1)
  qc.x(4)
  qc.x(0)
  qc.mct([0,1,2,3,4],7)
  qc.x(4)
  qc.x(0)
  qc.barrier()
  qc.cx(3,6)
  qc.x(2)
  qc.mct([0,1,2],6)
  qc.ccx(1,2,6)
  qc.ccx(0,1,6)
  qc.x(2)
  qc.barrier()
  qc.cx(2,5)
  qc.x(1)
  qc.ccx(1,0,5)
  qc.cx(1,5)
  qc.cx(0,5)
  qc.x(1)
  qc.barrier()
  gate = qc.to_gate()
  gate.name = 'U'
  Cgate = gate.control()
  return Cgate



def apl(a):
  return (a+1)*(a-0.4999999999999999)
