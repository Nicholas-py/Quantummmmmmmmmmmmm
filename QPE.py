from QFT import invQFT
from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from setup import circuitmeasure, h_it_all, cgate, simulate
from qiskit.circuit.library.standard_gates import PhaseGate,HGate
from math import pi


def QPE(qubitcount, gate, precision, *args):
  gatebits = QuantumRegister(qubitcount)
  testbits = QuantumRegister(precision)
  measurebits = ClassicalRegister(precision)
  qc = QuantumCircuit(testbits, gatebits, measurebits)
  h_it_all(qc, testbits)
  qc.x(-1)
  for i in range(precision):
    for j in range(2**i):
      if args != ():
        cgate(qc, gate, args + (i, precision))
      else:
        cgate(qc, gate, i, precision)
  qc.barrier()
  invQFT(qc, reg=testbits)
  qc.barrier()
  circuitmeasure(qc, measurebits, reg=testbits)
  a = simulate(qc, output=False)
  newa = {defractionize(k[::-1]): v for k, v in a.items()}
  return weightedmean(newa)

def weightedmean(datadict):
  newa = dict(sorted(datadict.items()))
  scores = list(newa.values())
  values = list(newa.keys())
  total = sum(scores)
  ee = 0
  for i in range(len(scores)):
    ee += values[i] * scores[i] / total
  return ee



def defractionize(x):
  base = 2**len(x)
  num = 0
  for i in range(len(x)):
    num += int(x[len(x)-i-1]) * 2**i
  return num / base


