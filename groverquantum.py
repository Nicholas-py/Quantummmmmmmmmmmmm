from setup import h_it_all, circuitmeasure, simulate,draw,statevector
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from math import sqrt
def getgroverinput():
  statements = []
  eee = input('What is the logic gate of the first criteria? (enter to skip) ').lower().strip()
  while eee in ['xor','or','and']:
    e = int(input('What is the first qubit it affects? ').lower().strip())
    ee = int(input('What\'s the other qubit  it affects? ').lower().strip())
    statements.append([eee,e,ee])
    eee = input('What is the logic gate of the next criteria? (enter to skip) ').lower().strip()
  if eee != '':
    print('Not valid gate, continuing')
  print('Loading output... ')
  return statements

def xor(qc,a,b,o):
  qc.cx(a,o)
  qc.cx(b,o)

def orgate(qc,a,b,o,inv):
  andgate(qc,a,b,o)
  xor(qc,a,b,o)

def andgate(qc,a,b,o):
  qc.ccx(a,b,o)

def max2(lst):
  maxi = -(10**100)
  for i in range(len(lst)):
      maxi = max(max(lst[i][1:]),maxi)
  return maxi
def applyoracle(qc,statements):
  qubit = max2(statements)+1
  for i in range(len(statements)):
    statements[i][1] = qubit - statements[i][1] - 1
    statements[i][2] = qubit - statements[i][2] - 1
    if statements[i][0] == 'xor':
      xor(qc,statements[i][1],statements[i][2],qubit+i)
    elif statements[i][0] == 'and':
      andgate(qc,statements[i][1],statements[i][2],qubit+i)
    elif statements[i][0] == 'or':
      orgate(qc,statements[i][1],statements[i][2],qubit+i,False)
    elif statements[i][0] == 'nor':
      qc.x(qubit+1)
      orgate(qc,statements[i][1],statements[i][2],qubit+i)
      qc.x(qubit+1)
  qc.mct(list(range(qubit,len(statements)+qubit)),len(statements)+qubit)
  for i in range(len(statements)-1,-1,-1):
    if statements[i][0] == 'xor':
      xor(qc,statements[i][1],statements[i][2],qubit+i)
    elif statements[i][0] == 'and':
      andgate(qc,statements[i][1],statements[i][2],qubit+i)
    elif statements[i][0] == 'or':
      orgate(qc,statements[i][1],statements[i][2],qubit+i,True)
    elif statements[i][0] == 'nor':
      qc.x(qubit+1)
      orgate(qc,statements[i][1],statements[i][2],qubit+i)
      qc.x(qubit+1)




def diffuser(qc,x):
  h_it_all(qc,x)
  for i in range(x.size):
    qc.x(x[i])
  qc.h(x[-1])
  qc.mct(x[0:-1],x[-1])
  qc.h(x[-1])
  for i in range(x.size):
    qc.x(x[i])
  h_it_all(qc,x)

def grover(statements,cycles = 'cheese'):
  qubit = max2(statements)+1
  x = QuantumRegister(qubit,name='x')
  c = QuantumRegister(len(statements),name='c')  
  o = QuantumRegister(1,name= 'o')
  op = ClassicalRegister(qubit,name='op')
  qc = QuantumCircuit(x,c,o,op)
  qc.x(o[0])
  qc.h(o[0])
  h_it_all(qc,x)
  if cycles == 'cheese':
    cycles = max(1,int(sqrt(2**x.size))-2)
  for i in range(cycles):
    applyoracle(qc,statements)
    diffuser(qc,x)
  circuitmeasure(qc,op,x)
  return qc


def groverinterface():
  print('Running grover\'s algorithm')
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
