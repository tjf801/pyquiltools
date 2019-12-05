import numpy as np
from pyquil import get_qc, Program
from pyquil.gates import *
from pyquil.api import local_qvm

def get_lines_as_list(program):
	"""This is not intended to be used."""
	#This is only used for inverse(). I'm sure there is a better way to do this.
	p = str(program)
	line = ""
	lines = []
	for char in p:
		if char != "\n": line+=char
		else: lines.append(line); line = ""
	for i in range(len(lines)):
		args = [];arg = "";line = lines[i]
		for char in line + " ":
			if char in " (":
				try: arg=int(arg)
				except: 
					try: arg=float(arg)
					except: pass
				try: #Random edge case for "pi/2, pi/4, etc."
					if "pi" in arg:
						if len(arg)>=4: arg = 3.1415926535897932/float(arg[3:])
						elif len(arg)==2: arg = 3.1415926535897932
				except: pass
				args.append(arg)
				arg = ""
			elif char in ")": continue
			else: arg+=char	
		lines[i] = args
	return lines

def inverse(program):
	"""returns the inverse of a quantum program."""
	invp = Program()
	program = get_lines_as_list(program)
	#The inverse of (A)...(Y)(Z) is (Z^-1)(Y^-1)...(A^-1)
	for line in program[::-1]:
		if line[0]=="I":
			invp += I(line[1])
		elif line[0]=="X":
			invp += X(line[1])
		elif line[0]=="Y":
			invp += Y(line[1])
		elif line[0]=="Z":
			invp += Z(line[1])
		elif line[0]=="PHASE":
			invp += PHASE(-line[0], line[1])
		elif line[0]=="H":
			invp += H(line[1])
		elif line[0]=="CNOT":
			invp += CNOT(line[1], line[2])
		elif line[0]=="CCNOT":
			invp += CCNOT(line[1], line[2], line[3])
		elif line[0]=="CPHASE":
			invp += CPHASE(-line[1], line[2], line[3])
		else:
			raise NotImplimentedError("Gate's inverse not implimented")
		#TODO add all quantum gates to this
	
	return invp

def bell(*qbits):
	"""Creates a bell state between any number of given qbits."""
	p = Program()
	p += H(qbits[0])
	for i in range(1, len(qbits)):
		p += CNOT(qbits[i-1], i)
	return p

def QFT(*qbits):
	"""The Quantum Fourier Transform (QFT) on given qbits."""
	#It's recursive, so you can't have more than ~1000 qbits. Sorry.
	#TODO use loops NOT recursion
	qbits = list(qbits)
	n = len(qbits)
	π = np.pi
	p = Program()
	if n==1:
		p += H(qbits[0])
	else:
		p += QFT(*qbits[:-1])
		for i in range(1, n):
			p += CPHASE((π / 2**(n-i)), qbits[n-1], qbits[i-1])
		p += H(qbits[n-1])
	return p

def IQFT(*qbits):
	"""The Inverse Quantum Fourier Transform (IQFT) on given qbits."""
	#you could use inverse(QFT()), but this is slightly faster, and it is shorter to type.
	#TODO use loops not recursion
	qbits = list(qbits)
	n = len(qbits)
	π = np.pi
	p = Program()
	if n==1:
		p = p + H(qbits[0])
	else:
		p += H(qbits[n-1])
		for i in range(n-1, 0, -1):
			p += CPHASE(-(π / 2**(n-i)), qbits[n-1], qbits[i-1])
		p = p + IQFT(*qbits[:-1])
	return p

#I am going to add more in the future, possibly stuff with grover's and/or shor's algorithm.
