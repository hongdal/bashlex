from ghmm import * 

# Number of characters, 1 to 103
alph = IntegerRange(1,104)

# Matrix A 
A = [
    [177.0/178.0, 1.0/178.0, 0.0, 0.0, 0.0],
    [0.0, 332.0/334.0, 1.0/334.0, 1.0/334.0, 0.0],
    [0.0, 0.0, 83.0/84.0, 1.0/84.0, 0.0],
    [0.0, 0.0, 0.0, 63.0/64.0, 1.0/64.0],
    [1.0/67.0, 0.0, 0.0, 0.0, 66.0/67.0]
]

# Matrix B
FP = [1.0/103] * 103
DW = [1.0/103] * 103
CP = [1.0/103] * 103
CH = [1.0/103] * 103
RM = [1.0/103] * 103
B = [FP, DW, CP, CH, RM]

# Initial state distribution 
PI = [1.0, 0, 0, 0, 0]

# Create a model
m=HMMFromMatrices(alph,DiscreteDistribution(alph),A,B,PI)

# print observation sequence. 
obs_seq = m.sampleSingle(2000000)
sequence_set = obs_seq.sequenceSet()
sequence = sequence_set.getSequence(0)
#print sequence 

# predict the internal states of this sequence
v = m.viterbi(obs_seq)
print type(v)
print v


exit(0)

# Training sequence O
train_set = [1,2,3,4,5]
train_seq = EmissionSequence(alph, train_set)

# Testing sequence O
test_set = [1,2,3]
test_seq = EmissionSequence(alph, test_set) 


test_vit = []
m.baumWelch(train_seq)
