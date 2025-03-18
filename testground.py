import time
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from groverquantum import grover, getgroverinput
from setup import *
from shors import shors
from math import pi,log, sqrt
import matplotlib.pyplot as plt
import time
from QFT import QFT,invQFT
import random

def test():
  qc = QuantumCircuit(100,100)
  for i in range(50):
    qc.x(random.randint(0,99))
    if i%10 == 0:
      qc.h(random.randint(0,99))
  for i in range(100):
    try:
      qc.cx(random.randint(0,99),random.randint(0,99))
      #qc.ccx(random.randint(0,99),random.randint(0,99),random.randint(0,99))
    except:
      pass
  #circuitmeasure(qc)
  #job = realcomputer(qc,'simulator_stabilizer')
  print('One moment')
  #time.sleep(5)#
  #print(job.results)
  inp = getgroverinput()
  a = time.time()
  qc = grover(inp)
  print('Circuit initialized. Time =',str(round(time.time()-a,3))+'. Running...')
  job = realcomputer(qc,device='ibmq_qasm_simulator',runtime=True)
  jobdata = job.result().quasi_dists[0]
  print('Real computer time:',round(time.time()-a,3))
  maxi = max(list(jobdata.keys()))
  graphdata = {}
  print('Graphing data')
  for i in jobdata.keys():
    graphdata[binvar(i,ln=int(log(maxi,2))+1)] = jobdata[i]
  plot_histogram(graphdata).show()
  print('Graph complete, calculating most likely result, time =',round(-(a-time.time()),3))
  invdata = {v+0.0000000001*invbinvar(k): k for k, v in graphdata.items()}
  datas = list(invdata.keys())
  mean = sum(datas)/len(datas)
  possibles = []
  stdv = 0
  for i in datas:
    stdv += (i-mean)**2
  stdv /= len(datas)
  stdv = sqrt(stdv)
  for i in datas:
    if i > mean-0.0000001+stdv:
      possibles += [invdata[i]]
  string = possibles[0]
  for i in possibles[1:]:
    string += ', '+i
  print('The most likely results are',string)
  print('Calculation time:',round(time.time()-a,3),'seconds')

