from setup import draw, simulate
from dj import djinterface
import qrand

from QFT import QFT
from QPE import QPE
from  shors import shors, qperiodfind
import simons
from math import pi
from groverquantum import groverinterface
import testground
from qiskit.circuit.library.standard_gates import PhaseGate

algorithm = input('Which algorithm would you like to run? ').lower().strip()

if algorithm[0] == 'g':
  groverinterface()


elif algorithm[0] == 's':
  x = 0
  a = int(input('Pick a number to be factored: (Not even or prime, please) '))
  if algorithm == 'shorts':
    x = 2
  while x != 1:
    print('Factor of',a,'found:',shors(a,False))
    x += 1

  
elif algorithm[0:2] == 'qp':
  a = int(input('Pick the precision wanted: (whole number) ').lower().strip())
  print('QUANTUM estimated decimal: ',QPE(1,PhaseGate(2*pi*float(input('Enter a decimal: ').lower().strip())),a))

  
elif algorithm[0] == 'p':
  from setup import *
  from dj import *
  from QFT import *
  from groverquantum import *
  from math import *
  from random import *
  from qiskit import *
  from shors import *
  from QPE import *
  print('Type commands below')

  
elif 'd' in algorithm and 'j' in algorithm:
  djinterface()

  
elif 'g' in algorithm:
  groverinterface()

  
elif 'q' in algorithm and 'p' in algorithm:
  a = int(input('Pick the precision wanted: (whole number)'))
  print('QUANTUM estimated decimal: ',QPE(1,PhaseGate(2*pi*float(input('Enter a decimal: ').lower().strip())),a))

  
elif 's' in algorithm:
  a = int(input('Pick a number to be factored: (Not even or prime, please) '))
  print('Factor of',a,'found:',shors(a,False,False))

  
elif 'p' in algorithm:
  from setup import *
  from dj import *
  from QFT import *
  from QPE import *
  from groverquantum import *
  from math import *
  from random import *
  from shors import *
  print('Type commands below')
else:
  print('Algorithm not known. Aborting...')
