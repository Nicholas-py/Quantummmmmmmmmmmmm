from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from setup import h_it_all,circuitmeasure, draw, simulate,statevector
from QFT import invQFT, QFT
size = 3
def simonoracle(qc,secret):
  size = len(secret)
  for i in range(size-1):
    qc.cx(i,i+size)
first = QuantumRegister(size)
second = QuantumRegister(size-1)
cbits = ClassicalRegister(size)
qc = QuantumCircuit(first,second,cbits)
def simons(qc,size,secret):
  h_it_all(qc,first)
  qc.x(-1)
  QFT(qc,second)
  qc.barrier()
  simonoracle(qc,secret)
  qc.barrier()
  statevector(qc)
  h_it_all(qc,first)
  circuitmeasure(qc,cbits,first)
