from setup import h_it_all
from qiskit import QuantumCircuit
from math import pi
def crz2(qc, x, q1, q2):
  qc.cp(pi*1/(2**x),q2,q1)
def negativecrz2(qc,x,q1,q2):
  qc.cp(-pi*1/(2**x),q1,q2)
  
def QFT(qc,reg='all',swaps=False):
  if reg == 'all':
    qubits = qc.num_qubits
    if not swaps:
      for i in range(qubits):
        qc.h(i)
        for j in range(i+1,qubits):
          crz2(qc,j-i,i,j)
    else:
      for i in range(qubits-1,-1,-1):
        qc.h(i)
        for j in range(0,i):
          crz2(qc,j+1,i,i-j-1)

      for i in range(int(qubits/2)):
        qc.swap(i,qubits-i-1)

  else:
    qubits = reg.size
    if not swaps:
      for i in range(qubits):
        qc.h(reg[i])
        for j in range(i+1,qubits):
          crz2(qc,j-i,reg[i],reg[j])
    else:
      for i in range(qubits-1,-1,-1):
        qc.h(reg[i])
        for j in range(0,i):
          crz2(qc,j+1,reg[i],reg[i-j-1])
      for i in range(int(qubits/2)):
        qc.swap(reg[i],reg[qubits-i-1])
  return qc
  
def invQFT(qc,reg='all',swaps=False):
  if reg == 'all':
    qubits = qc.num_qubits
    if not swaps:
      for i in range(qubits-1,-1,-1):
        for j in range(qubits-1,i,-1):
          negativecrz2(qc,j-i,i,j)
        qc.h(i)
    else:
      for i in range(int(qubits/2)):
        qc.swap(i,qubits-i-1)

      for i in range(qubits):
        for j in range(0,i):
          negativecrz2(qc,i-j,i,j)
        qc.h(i)


  else:
    qubits = reg.size
    if not swaps:
      for i in range(qubits-1,-1,-1):
        for j in range(qubits-1,i,-1):
          negativecrz2(qc,j-i,reg[i],reg[j])
        qc.h(reg[i])

    else:
      for i in range(int(qubits/2)):
        qc.swap(reg[i],reg[qubits-i-1])
      for i in range(qubits):
        for j in range(0,i):
          negativecrz2(qc,i-j,reg[i],reg[j])
        qc.h(reg[i])


  return qc



    
