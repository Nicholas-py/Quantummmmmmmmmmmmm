from setup import *
from dj import *
from groverquantum import *
from qiskit import QuantumCircuit, QuantumRegister
algorithm = input('Which algorithm would you like to run? ')
if algorithm[0] == 'g' or 'g' in algorithm:
  qc = grover(getgroverinput())
  while True:
    varnm = input('Enter commands here: ')
    if varnm == '':
      print('No command')
    elif varnm[0].lower() == 'd':
      draw(qc)
    elif varnm[0].lower() == 'r':
      print('Restarting')
      qc = grover(getgroverinput())
    elif varnm[0].lower() == 's':
      simulate(qc)
    elif varnm[0].lower() == 'c':
      break
    elif 's' in varnm:
      simulate(qc)
    elif 'r' in varnm:
      print('Restarting')
      qc = grover(getgroverinput())
    elif 'd' in varnm:
      draw(qc)
    elif 'c' in varnm:
      break
else:
  print('Not a valid algorithm')
