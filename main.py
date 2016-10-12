import sys
import math
import random

from state import State

print 'Argument List:', str(sys.argv)

# Import the file
f = open(sys.argv[1], 'r')

myState = State(f)
searchStatesExplored = 0


# Generate Initial Solution
s = myState.generate_soln()
searchStatesExplored += 1

# Set initial temp and min temp
T = 1000.0
Tmin = 0.01
alpha = 0.1
k = 0.1


# initialize equilibrium to False
eq = False

print "---------------------------------------"
print " Starting simulated annealing..."
print "---------------------------------------"
while T > Tmin:
    eq = 0
    while eq < 50:
        print "\n---------------------"
        print "T = {}".format(T)
        print "eq: {}".format(eq)
        print "---------------------"
        sP = myState.generate_nbrSoln(s)
        searchStatesExplored += 1
        sFitness = myState.fitness(s)
        sPFitness = myState.fitness(sP)
        dE = myState.fitness(sP) - myState.fitness(s)
        print "S Fitness: {}\nSP Fitness: {}\ndE: {}".format(sFitness, sPFitness, dE)
        print "---------------------"
        if dE == 0:
            # identical solution
            # take it, but also increment eq
            s = sP
            eq += 1
        elif dE < 0:
            # Better solution
            s = sP
            print "Better Solution Found!"
        else:
            # Worse Solution
            prob = math.exp(- dE / (k * T))  # should be between 1 and 0
            print "Found worse solution..."
            print "Acceptance Prob.: {}".format(prob)
            rand = random.random()
            print "Random Val:       {}".format(rand)
            if rand < prob:
                print "Worse Solution Accepted!"
                s = sP
            else:
                eq += 1
    T = T * alpha

# s Should contain the arrived upon solution
print "---------------------------------------"
print " Ended simulated annealing..."
print "---------------------------------------"

print "---------------------------------------"
print " Program Summary"
print "---------------------------------------"
myState.print_solution(s)
myState.print_partyDivision()
myState.print_districtLists(s)
myState.print_nDistrictVotesByParty(s)
print "---------------------------------------"
print " Program Summary"
print "---------------------------------------"
print " Search States Explored: {}".format(searchStatesExplored)
print "---------------------------------------"




