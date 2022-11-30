from qiskit import QuantumCircuit, QuantumRegister
from qiskit import exceptions
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
sim = AerSimulator()   
from qiskit.quantum_info import Statevector
import math
import random
import matplotlib.pyplot as plt

#visualization functions
def draw(qc):
  plt.plot = qc.draw('mpl')
  plt.show(block=False)
  print(qc.draw())



def statevector(qc):
  try:
    ket = Statevector(qc)
  except exceptions.QiskitError:
    print('Statevector Error: You can\'t have a statevector after you\'ve measured')
    return
  def binvar(n,ln):
    bn = str(bin(n))[2:]
    bn = '0'*ln+bn
    bn = bn[len(bn)-ln:]
    return bn
  print('Statevector:')
  lst = list(ket)
  for i in range(len(lst)):
    lst[i] = complex(lst[i])
    lst[i] = str(round(lst[i].real,5))+'+'+str(round(lst[i].imag,5)*1j)
    print('|'+binvar(i,int(math.log(len(lst),2)))+'> :',str(lst[i]))

def simulate(qc):
  try:
    a = sim.run(qc).result().get_counts()
    print(a)
    plot_histogram(a).show()
    return a
  except exceptions.QiskitError:
    print('Simulation Error')
    return

# circuit setup
def h_it_all(qc):
  for i in range(qc.num_qubits):
    qc.h(i)




