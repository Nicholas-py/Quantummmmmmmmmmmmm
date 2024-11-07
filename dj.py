from setup import h_it_all, circuitmeasure, simulate
from qiskit import QuantumCircuit, QuantumRegister,ClassicalRegister
import random
def djoracle(qc,qs,type):
  if type == 'constant':
    print('Running for a constant function')
    if random.randint(0,1) == 0:
      qc.x(-1)
  else:
    print('Running for a balanced function')
    for i in range(qs):
      if random.randint(0,1) == 0:
        qc.x(i)
        qc.cx(i,qs)
        qc.x(i)
      else:
        qc.cx(i,qs)

def dj(qs,type):
  x = QuantumRegister(qs)
  o = QuantumRegister(1)
  op = ClassicalRegister(qs)
  qc = QuantumCircuit(x,o,op)
  qc.x(qs)
  h_it_all(qc)
  djoracle(qc,qs,type)
  h_it_all(qc)
  circuitmeasure(qc,op,x)
  a = simulate(qc)
  if list(a.keys())[0][0] == '1':
    print('Predicts balanced function')
  else:
    print('Predicts constant function')
  

def djinterface():
  print('Running Deustch-Jozsa algorithm')
  qs = int(input('Number of qubits: '))
  bn = input('Balanced or constant function? ').lower().strip()
  if 'b' in bn:
    dj(qs,'balanced')
  elif 'c' in bn:
    dj(qs,'constant')
  else:
    dj(qs, random.choice(['balanced,constant']))
