from qiskit import QuantumCircuit
from math import log, inf, ceil
from setup import h_it_all, circuitmeasure, invbinvar,simulate, realcomputer

def deqrand(bitstring,a,b):
  if abs(b-a) < 3:
    if bitstring[0] == '1':
      return b
    return a
  if bitstring[0] == '1':
    return deqrand(bitstring[1:],ceil((a+b)/2),b)
  return deqrand(bitstring[1:],a,int((a+b)/2))
    
def qrand():
  a = int(input('What\'s the minimum random number to generate? '))
  b = int(input('What\'s the maximum random number to make? '))
  assert a>= 0 and b > 0 and b > a
  num = inf
  while num > b:
    qc = QuantumCircuit(int(log(b-a+1,2))+1,int(log(b-a+1,2))+1)
    h_it_all(qc)
    circuitmeasure(qc)    
    lll = simulate(qc,False,shots=1)
    num = invbinvar(list(lll.keys())[0])
  return num+a
  

def realqrand(maxi=1000):
  print('This program can generate true random numbers')
  a = int(input('What\'s the minimum random number to generate? '))
  b = int(input('What\'s the maximum random number to make? (no higher than '+str(maxi)+') '))
  assert a>= 0 and b > 0 and b > a
  qc = QuantumCircuit(int(log(b-a+1,2))+1,int(log(b-a+1,2))+1)
  h_it_all(qc)
  circuitmeasure(qc)    
  simulate(qc,True,1)
  job = realcomputer(qc,device = 'ibmq_lima',shots=1)
  print('Job id: ',job.job_id())
  num = (deqrand(input('Input the result of the quantum computer running this program here: '),a,b))
  return num

