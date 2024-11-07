from qiskit import exceptions
from qiskit import Aer,transpile, assemble
from qiskit.visualization import plot_histogram
aer_sim = Aer.get_backend('aer_simulator')
from qiskit.quantum_info import Statevector
from math import log
import matplotlib.pyplot as plt
from qiskit import IBMQ
from qiskit.primitives import Sampler
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel="ibm_quantum", token='109fa751322d2b7a0c01ab06f499c827aac6c321f8b0f8d4088175d2a52e4e2d5fbbbfe0e80f44686dc440dfdcd254c2b77faf6a66f424c2d352f7451fc05f57')
IBMQ.save_account("109fa751322d2b7a0c01ab06f499c827aac6c321f8b0f8d4088175d2a52e4e2d5fbbbfe0e80f44686dc440dfdcd254c2b77faf6a66f424c2d352f7451fc05f57", overwrite=True) 

#visualization functions
def draw(qc,pause=False):
  plt.plot = qc.draw('mpl')
  plt.show(block=pause)
  print(qc.draw())

def binvar(n,ln='cheese'):
  if ln == 'cheese':
    ln = int(log(max(1,n),2))+1
  bn = str(bin(n))[2:]
  bn = '0'*ln+bn
  bn = bn[len(bn)-ln:]
  return bn

def invbinvar(bn):
  n = 0
  for i in range(len(bn)):
    n += 2**i*int(bn[-(i+1)])
  return n
def statevector(qc):
  try:
    ket = Statevector(qc)
  except exceptions.QiskitError:
    print('Statevector Error. You might have measured before checking the statevector, or passed in incorrect input')
    return
  print('Statevector:')
  lst = list(ket)
  for i in range(len(lst)):
    lst[i] = complex(lst[i])
    real = str(round(lst[i].real,3))
    if real == '0.0' or real == '-0.0':
      real = ''
    complecks = round(lst[i].imag,3)
    if complecks < 0:
      complecks = str(complecks)+'i'
    elif complecks == 0:
      complecks = ''
    elif complecks > 0:
      complecks = '+'*int(real != '') + str(complecks) + 'i'
    lst[i] = real+complecks
    print('|'+binvar(i,int(log(len(lst),2)))+'〉:',str(lst[i]))

def globalphase(qc,angle,qubit='all'):
  if qubit =='all':
    for i in range(qc.num_qubits):
      qc.rz(angle,i)
      qc.x(i)
      qc.rz(angle,i)
      qc.x(i)
  else:
      qc.rz(angle,qubit)
      qc.x(qubit)
      qc.rz(angle,qubit)
      qc.x(qubit)
    

def simulate(qc,output=True,shots=1024):
  try:
    t_qc = transpile(qc, aer_sim)
    qobj = assemble(t_qc)
    a = aer_sim.run(qobj,shots=shots)
    return showresults(a,output)
  except exceptions.QiskitError:
    print('Simulation Error')
    return

def showresults(a,output):
    a = dict(sorted(a.result().get_counts().items()))
    if output:
      print(a)
      plot_histogram(a).show()
    return a

# circuit setup
def h_it_all(qc,reg='all'):
  if reg == 'all':
    for i in range(qc.num_qubits):
      qc.h(i)
  else:
    for i in range(reg.size):
      qc.h(reg[i])
def x_it_all(qc,reg='all'):
  if reg == 'all':
    for i in range(qc.num_qubits):
      qc.x(i)
  else:
    for i in range(reg.size):
      qc.x(reg[i])




def circuitmeasure(qc, cbits='cbits', reg='all'):
  if reg == 'all':
    if cbits == 'cbits':
      for i in range(qc.num_qubits):
        qc.measure(i,i)
    else:
      for i in range(qc.num_qubits):
        qc.measure(i,cbits[i])
      
  else:
    for i in range(reg.size):
      qc.measure(reg[i],cbits[i])

def probabilities(qc):
  try:
    ket = Statevector(qc)
  except exceptions.QiskitError:
    print('Error. You might have measured before checking the probabilities, or passed in incorrect input')
    return
  print('Probabilities:')
  lst = list(ket)
  for i in range(len(lst)):
    lst[i] = complex(lst[i])
    lst[i] = round(lst[i].real**2+lst[i].imag**2,5)
  maxi = max(lst)
  for i in range(len(lst)):
    ies = 'i'*round(lst[i]/maxi*40)
    print('|'+binvar(i,int(log(len(lst),2)))+'〉:',str(lst[i]),ies)


def cgate(qc, gate, *args):
  #print(list(args))
  cgate = gate.control(1)
  qc.append(cgate,list(args))

def realcomputer(circuit,device='ibmq_manila',transpiled = True,shots=1024,runtime = False):
  if runtime:
    sampler = Sampler()
    job = sampler.run(circuit)
    return job
  
  print('Setting up')
  provider = IBMQ.load_account()
  provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
  backend = provider.get_backend(device)
  # prepare the circuit for the backend
  if transpiled:
    mapped_circuit = transpile(circuit, backend=backend)
    qobj = assemble(mapped_circuit, backend=backend, shots=shots)
  else:
    qobj = assemble(circuit, backend=backend, shots=1024)
  print('Setup complete, sending to quantum computer')
  # execute the circuit
  job = backend.run(qobj)
  print('Program in queue')
  return job

