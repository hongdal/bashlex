from ghmm import * 
import sys

if len(sys.argv) < 2:
    print "Usage: getHmm.py single_line-5000.txt"
    exit(1)

# Number of characters, 1 to 104
alph = IntegerRange(1,105)


# Training sequence O
with open(sys.argv[1]) as infile:
    line = infile.readline()
    line = line.rstrip("\r\n")
    mylist = line.split(',')
    train_set = [ int(i) for i in mylist ]

print "dataset size: " + str(len(train_set))
train_seq = EmissionSequence(alph, train_set)
print "Start to prepare initial parameter for HMM"

# Matrix A 
A = [
    [177.0/178.0, 1.0/178.0, 0.0, 0.0, 0.0],
    [0.0, 332.0/334.0, 1.0/334.0, 1.0/334.0, 0.0],
    [0.0, 0.0, 83.0/84.0, 1.0/84.0, 0.0],
    [0.0, 0.0, 0.0, 63.0/64.0, 1.0/64.0],
    [1.0/67.0, 0.0, 0.0, 0.0, 66.0/67.0]
]

# Matrix B
FP = [1.0/104] * 104
DW = [1.0/104] * 104
CP = [1.0/104] * 104
CH = [1.0/104] * 104
RM = [1.0/104] * 104
B = [FP, DW, CP, CH, RM]

# Initial state distribution 
PI = [1.0, 0, 0, 0, 0]


# Create a model
m=HMMFromMatrices(alph,DiscreteDistribution(alph),A,B,PI)


print "Start to train the HMM"
# Train a model 
m.baumWelch(train_seq)


print "model successfully trained, now writing to ghmm.xml"
# Store a model in the file
m.write("ghmm.xml")
m = HMMOpen("ghmm.xml")


'''
# print observation sequence. 
obs_seq = m.sampleSingle(1000)
sequence_set = obs_seq.sequenceSet()
sequence = sequence_set.getSequence(0)
print sequence 
'''


# predict the internal states of this sequence
v = m.viterbi(train_seq)
print v


# Unused ...
# Testing sequence O
test_set = [1,2,3]
test_seq = EmissionSequence(alph, test_set) 
test_vit = []
