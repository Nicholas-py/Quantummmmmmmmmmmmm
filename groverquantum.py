from setup import *
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from math import sqrt
statements = [['xor',2,3],['xor',0,1],['xor',2,0],['and',0,3]]
def max2(lst):
  maxi = 0-(10**100)
  for i in range(len(lst)):
      maxi = max(max(lst[i][1:]),maxi)
  return maxi
qubit = max2(statements)+1

x = QuantumRegister(qubit,name='x')
c = QuantumRegister(len(statements),name='c')
o = QuantumRegister(1,name= 'o')
op = ClassicalRegister(4,name='op')
qc = QuantumCircuit(x,c,o,op)
qc.x(o[0])
qc.h(o[0])
def h_it_all(qc,reg='all'):
  if reg == 'all':
    for i in range(qc.num_qubits):
      qc.h(i)
  else:
    for i in range(reg.size):
      qc.h(reg[i])
def applyoracle(qc):
  for i in range(len(statements)):
    if statements[i][0] == 'xor':
      qc.cx(statements[i][1],c[i])
      qc.cx(statements[i][2],c[i])
    if statements[i][0] == 'and':
      qc.ccx(statements[i][1],statements[i][2],c[i])
  qc.mct(c,o[0])
  for i in range(len(statements)-1,-1,-1):
    if statements[i][0] == 'xor':
      qc.cx(statements[i][2],c[i])
      qc.cx(statements[i][1],c[i])
    if statements[i][0] == 'and':
      qc.ccx(statements[i][1],statements[i][2],c[i])




def diffuser(qc):
  global x,o
  h_it_all(qc,x)
  for i in range(x.size):
    qc.x(x[i])
  qc.h(x[-1])
  qc.mct(x[0:-1],x[-1])
  qc.h(x[-1])
  for i in range(x.size):
    qc.x(x[i])
  h_it_all(qc,x)

def do_circuit():
  h_it_all(qc,x)
  for i in range(int(sqrt(2**x.size))-2):
    applyoracle(qc)
    diffuser(qc)
  for i in range(4):
    qc.measure(x[i],op[i])
  simulate(qc)
