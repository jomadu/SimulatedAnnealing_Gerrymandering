'''
State.py - Class
Author: John Dunn
Date: Oct. 3, 2016

This class serves to map together voter objects

Instance Variables:
 - voters - 2D dict array of Voter() classes
 - totalRows
 - totalCols
 - upperRowsIdx
 - upperColsIdx
 - totalVoters
 - dCnt
 - rCnt
 - independentCnt
 - voterRatio = dCnt / rCnt

 - districts - dict of lists containing voters in districts

'''
import time
import random
import copy
from queue import Queue
from voter import Voter

N = 'n'
NE = 'ne'
E = 'e'
SE = 'se'
S = 's'
SW = 'sw'
W = 'w'
NW = 'nw'


class State:

    def __init__(self, f):
        # --------------------------------
        # Instance Variable Initilaization
        # --------------------------------

        self.nDistricts = None
        self.dCnt = 0
        self.rCnt = 0
        self.independentCnt = 0
        self.totalRows = 0
        self.totalCols = 0
        self.upperRowsIdx = 0
        self.upperColsIdx = 0
        self.totalVoters = 0
        self.voterRatio = 0
        self.voters = []

        # --------------------------------
        # Setup
        # --------------------------------

        # Create a local List-of-Lists variable called voterParties
        # to contain the party affiliations
        voterParties = []

        # Iterate through the file 'f'
        #  - Add party affiliation to voterParties[row][col]
        #  - Increment the count of the appropriate party
        rowIdx = 0
        for row in f:
            colIdx = 0
            rowTkns = row.split()
            voterParties.append([])
            for col in rowTkns:
                voterParties[rowIdx].append(rowTkns[colIdx])
                if voterParties[rowIdx][colIdx] == "D":
                    self.dCnt += 1
                elif voterParties[rowIdx][colIdx] == "R":
                    self.rCnt += 1
                else:
                    self.independentCnt += 1
                colIdx += 1
            rowIdx += 1

        # After iterating through the file:
        #  - rowIdx contains the number of total rows
        #  - colIdx contains the number of total cols
        self.totalRows = rowIdx
        self.upperRowsIdx = rowIdx - 1

        self.totalCols = colIdx
        self.upperColsIdx = colIdx - 1

        # Update the totalVoters and voterRatio
        self.totalVoters = self.totalRows * self.totalCols
        self.voterRatio = self.dCnt / float(self.rCnt)

        print ("State Initialized:\n - Number of Voters: {}\n - Rows: {}\n - Columns: {}"
               .format(self.totalVoters, self.totalRows, self.totalCols))

        # Get desired number of districts from user
        while self.nDistricts is None:
            try:
                response = int(input(("Please enter a number of districts for this state"
                                      "that is a factor of {}:\n".format(self.totalVoters))))
                if (self.totalVoters % response) == 0:
                    self.nDistricts = response
                else:
                    print "Invalid Response..."
            except (ValueError, TypeError, SyntaxError, NameError):
                print "Invalid Response..."

        # Create an instance List-of-Lists variable called voters
        # which will hold all the Voter objects in the State object
        # Initialize each voter with: id, location [row, col], and party
        for i in range(0, self.totalRows):
            self.voters.append([])
            for j in range(0, self.totalCols):
                id = "[row:{:>3d},col:{:>3d}]".format(i, j)
                self.voters[i].append(Voter(id, [i, j], None, voterParties[i][j]))

        # Create links between neighbors
        for i in range(0, self.totalRows):
            for j in range(0, self.totalCols):
                # NW corner of state
                if i == 0 and j == 0:
                    self.voters[i][j].set_nbr(E, self.voters[i][j + 1])
                    self.voters[i][j].set_nbr(SE, self.voters[i + 1][j + 1])
                    self.voters[i][j].set_nbr(S, self.voters[i + 1][j])
                # NE corner of state
                elif i == 0 and j == self.upperColsIdx:
                    self.voters[i][j].set_nbr(W, self.voters[i][j - 1])
                    self.voters[i][j].set_nbr(SW, self.voters[i + 1][j - 1])
                    self.voters[i][j].set_nbr(S, self.voters[i + 1][j])
                # SW corner of state
                elif i == self.upperRowsIdx and j == 0:
                    self.voters[i][j].set_nbr(E, self.voters[i][j + 1])
                    self.voters[i][j].set_nbr(NE, self.voters[i - 1][j + 1])
                    self.voters[i][j].set_nbr(N, self.voters[i - 1][j])
                # SE corner of state
                elif i == self.upperRowsIdx and j == self.upperColsIdx:
                    self.voters[i][j].set_nbr(W, self.voters[i][j - 1])
                    self.voters[i][j].set_nbr(NW, self.voters[i - 1][j - 1])
                    self.voters[i][j].set_nbr(N, self.voters[i - 1][j])
                # N edge of state
                elif i == 0:
                    self.voters[i][j].set_nbr(W, self.voters[i][j - 1])
                    self.voters[i][j].set_nbr(SW, self.voters[i + 1][j - 1])
                    self.voters[i][j].set_nbr(S, self.voters[i + 1][j])
                    self.voters[i][j].set_nbr(SE, self.voters[i + 1][j + 1])
                    self.voters[i][j].set_nbr(E, self.voters[i][j + 1])
                # W edge of state
                elif j == 0:
                    self.voters[i][j].set_nbr(N, self.voters[i - 1][j])
                    self.voters[i][j].set_nbr(NW, self.voters[i - 1][j + 1])
                    self.voters[i][j].set_nbr(W, self.voters[i][j + 1])
                    self.voters[i][j].set_nbr(SW, self.voters[i + 1][j + 1])
                    self.voters[i][j].set_nbr(S, self.voters[i + 1][j])
                # S edge of state
                elif i == self.upperRowsIdx:
                    self.voters[i][j].set_nbr(W, self.voters[i][j - 1])
                    self.voters[i][j].set_nbr(NW, self.voters[i - 1][j - 1])
                    self.voters[i][j].set_nbr(N, self.voters[i - 1][j])
                    self.voters[i][j].set_nbr(NE, self.voters[i - 1][j + 1])
                    self.voters[i][j].set_nbr(E, self.voters[i][j + 1])
                # E edge of state
                elif j == self.upperColsIdx:
                    self.voters[i][j].set_nbr(N, self.voters[i - 1][j])
                    self.voters[i][j].set_nbr(NW, self.voters[i - 1][j - 1])
                    self.voters[i][j].set_nbr(W, self.voters[i][j - 1])
                    self.voters[i][j].set_nbr(SW, self.voters[i + 1][j - 1])
                    self.voters[i][j].set_nbr(S, self.voters[i + 1][j])
                # Non-Border Voter
                else:
                    if not self.voters[i][j].has_nbr(N):
                        self.voters[i][j].set_nbr(N, self.voters[i - 1][j])
                    if not self.voters[i][j].has_nbr(NE):
                        self.voters[i][j].set_nbr(NE, self.voters[i - 1][j + 1])
                    if not self.voters[i][j].has_nbr(E):
                        self.voters[i][j].set_nbr(E, self.voters[i][j + 1])
                    if not self.voters[i][j].has_nbr(SE):
                        self.voters[i][j].set_nbr(SE, self.voters[i + 1][j + 1])
                    if not self.voters[i][j].has_nbr(S):
                        self.voters[i][j].set_nbr(S, self.voters[i + 1][j])
                    if not self.voters[i][j].has_nbr(SW):
                        self.voters[i][j].set_nbr(SW, self.voters[i + 1][j - 1])
                    if not self.voters[i][j].has_nbr(W):
                        self.voters[i][j].set_nbr(W, self.voters[i][j - 1])
                    if not self.voters[i][j].has_nbr(NW):
                        self.voters[i][j].set_nbr(NW, self.voters[i - 1][j - 1])

    def generate_soln(self, districtOriginSeeds=None):
        '''
        Function Description:

        Generates a solution.

        copy.deepCopy() the voters List-of-Lists to initSoln

        Until a solution is found:
            Generate district origins either by seed or randomly
            iterate through rows and cols of initSoln:
                if voter at [row, col] is district origin:
                    set the voters district to the district num
                else:
                    set the voters district to None
            4. Randomly select order for districts to claim voters.
            5. Districts take turns "claiming" voters.
                a. If a district cannot claim a district before a full solution
                   is found, it is "cramped", and the solution is invalid
        '''
        # -------------------------------
        # claim_voter subFunction
        # -------------------------------
        def claim_voter(originVoter):

            districtNum = originVoter.get_district()
            claimedVoter = False
            q = Queue()

            # -----------------------------------------
            # BFS to find and claim voter for district
            # -----------------------------------------

            for row in range(0, self.totalRows):
                for col in range(0, self.totalCols):
                    initSoln[row][col].set_visited(False)

            q.enqueue(originVoter)

            while (not q.empty() and not claimedVoter):

                vtr = q.dequeue()

                # Unclaimed? Claim voter!
                if (vtr.get_district() is None):
                    [vtrRow, vtrCol] = vtr.get_loc()
                    initSoln[vtrRow][vtrCol].set_district(districtNum)
                    claimedVoter = initSoln[vtrRow][vtrCol]

                elif (not vtr.isVisited()) and (vtr.get_district() == districtNum):
                    vtr.set_visited(True)

                    for cardinal in vtr.nbrs:
                        if vtr.nbrs[cardinal] is not None:
                            if not vtr.nbrs[cardinal].isVisited():
                                q.enqueue(vtr.nbrs[cardinal])

            return claimedVoter

        # -------------------------------
        # generate_solution() start
        # -------------------------------
        initSoln = copy.deepcopy(self.voters)
        solutionFound = False
        solutionsTried = 0
        print "Generating an Initial Solution..."
        while not solutionFound:

            # District Origins can either be seeded by the user,
            # or, more likely, randomly generated
            districtOrigins = {}
            if districtOriginSeeds is not None:
                # save the district origin seeds to districtOrigins
                for seed in districtOriginSeeds:
                    [seedRow, seedCol] = seed
                    key = "({},{})".format(seedRow, seedCol)
                    if key not in districtOrigins:
                        districtOrigins[key] = None

            else:
                # Generate (self.nDistricts) random [row, col]
                # coordinates between 0 and (nDistricts-1).
                nDistinctOriginsFound = 0
                while nDistinctOriginsFound < self.nDistricts:
                    randRow = random.randint(0, self.upperRowsIdx)
                    randCol = random.randint(0, self.upperColsIdx)
                    key = "({},{})".format(randRow, randCol)
                    if key not in districtOrigins:
                        districtOrigins[key] = None
                        nDistinctOriginsFound += 1

            # Set Voter object district att. at each random district origin
            # equal to an incrementing districtNum variable or
            # None if not a district origin
            districtCnt = 0
            for row in range(0, self.totalRows):
                for col in range(0, self.totalCols):
                    key = "({},{})".format(row, col)
                    if key in districtOrigins:
                        districtOrigins[key] = initSoln[row][col]
                        initSoln[row][col].set_district(districtCnt)
                        districtCnt += 1
                    else:
                        initSoln[row][col].set_district(None)

            # -------------------------------
            # Start taking claiming turns
            # -------------------------------
            turnsComplete = 1  # Because the origin is technically a turn
            keepClaiming = True
            # crampedDistrict means a district was unable
            # to claim during previous turn
            crampedDistrict = False
            while keepClaiming:
                for key in districtOrigins:
                    originVoter = districtOrigins[key]
                    voterClaimed = claim_voter(originVoter)
                    if not voterClaimed:
                        crampedDistrict = True
                if crampedDistrict:
                    keepClaiming = False
                else:
                    turnsComplete += 1
                    keepClaiming = (turnsComplete < (self.totalVoters / self.nDistricts))

            solutionsTried += 1
            if not crampedDistrict:
                solutionFound = True

        return initSoln

    def isValidSolution(self, soln):
        '''
        This needs to look into self.voters and verify that
        in fact, each of the districts are complete and contiguous

        Iterate through solution rows and cols:
            If you encounter a voter with a new district
                save that voter as the "district origin"
        With each district origin
            do a BFS on each to count the voters of the same district
            that are contiguous.
            if this count is less than the total voters / nDistricts
                the solution is invalid
        '''

        isValid = True
        q = Queue()

        # Establish District Origins
        # and set visited att. to False (for BFS)
        districtOrigins = {}
        for row in range(0, self.totalRows):
            for col in range(0, self.totalCols):
                vtr = soln[row][col]
                vtr.set_visited(False)
                key = vtr.get_district()
                if key not in districtOrigins:
                    districtOrigins[key] = vtr
        # -----------------------------------------
        # BFS to find and claim voter for district
        # -----------------------------------------

        for origin in districtOrigins:

            originVoter = districtOrigins[origin]
            districtNum = originVoter.get_district()
            memberCnt = 0

            for row in range(0, self.totalRows):
                for col in range(0, self.totalCols):
                    soln[row][col].set_visited(False)

            q.enqueue(originVoter)

            while (not q.empty()):

                vtr = q.dequeue()

                if (not vtr.isVisited()) and (vtr.get_district() == districtNum):
                    memberCnt += 1
                    vtr.set_visited(True)
                    for cardinal in vtr.nbrs:
                        if vtr.nbrs[cardinal] is not None:
                            if not vtr.nbrs[cardinal].isVisited():
                                q.enqueue(vtr.nbrs[cardinal])

            if not (memberCnt == (self.totalVoters / self.nDistricts)):
                isValid = False
                return isValid

        return isValid

    def generate_nbrSoln(self, soln):
        '''
        copy.deepcopy() voters to a new List-Of-Lists called nbrSoln
        while we haven't generated a valid neighboring solution:
            set nbrSoln = soln
            pick a random voter in newSoln
            pick a random direction
            if the nbr of voter in the random direction and the voter are
            of different districts
                swap their districts
                check if the nbrSoln is still valid
                if yes
                    we have found a neighboring solution!
                else
                    continue

        '''
        def swapDistricts(originVoter, nbrVoter):
            tempDistrict = copy.copy(nbrVoter.get_district())
            nbrVoter.set_district(originVoter.get_district())
            originVoter.set_district(tempDistrict)

        nbrSoln = []
        nbrSolutionFound = False
        solutionsTried = 0

        while not nbrSolutionFound:
            nbrSoln = copy.deepcopy(soln)
            randRow = random.randint(0, self.upperRowsIdx)
            randCol = random.randint(0, self.upperColsIdx)

            originVoter = nbrSoln[randRow][randCol]
            originDistrict = originVoter.get_district()

            for cardinal in originVoter.nbrs:
                nbrVoter = originVoter.nbrs[cardinal]
                if nbrVoter is not None:
                    nbrDistrict = nbrVoter.get_district()
                    if not (originDistrict == nbrDistrict):
                        swapDistricts(originVoter, nbrVoter)
                        solutionsTried += 1
                        if self.isValidSolution(nbrSoln):
                            nbrSolutionFound = True
                            break
                        else:   
                            # swap back
                            swapDistricts(originVoter, nbrVoter)


        if nbrSolutionFound:
            print "Swapped Voter: {} and Voter: {}".format(originVoter.get_id(), nbrVoter.get_id())
            return nbrSoln
        else:
            return False

    def fitness(self, soln):
        '''
        Returns a value between 0 (best) and 1 (worst)
        that describes the fitness of the districting solution

        create a List-of-Lists called districtVotes
        iterate through the soln rows and columns:
            populate districts L.O.L
        for each district list in districts
            districtVote = 0
            for each voter in district list
                districtVote +1 for D
                districtVote -1 for R
            if districtVote > 0 
                districtVotes +1
            else if districtVote < 0
                districtVotes -1

        districtVotesRatio = districtVotes / float(self.nDistricts)
        fitness = abs(self.voterRatio - districtVotesRatio)
        '''
        districtVotes = {}
        d_districtVotes = 0
        r_districtVotes = 0

        for row in range(0, self.totalRows):
            for col in range(0, self.totalCols):
                districtKey = str(soln[row][col].get_district())

                if districtKey not in districtVotes:
                    districtVotes[districtKey] = 0

                if soln[row][col].get_party() == "D":
                    districtVotes[districtKey] += 1
                elif soln[row][col].get_party() == "R":
                    districtVotes[districtKey] -= 1

        for districtKey in districtVotes:
            if districtVotes[districtKey] > 0:
                d_districtVotes += 1
            elif districtVotes[districtKey] < 0:
                r_districtVotes += 1

        districtVotesRatio = d_districtVotes / float(r_districtVotes)
        fitness = abs(self.voterRatio - districtVotesRatio)
        
        return fitness

    def get_voters(self):
        return self.voters

    def get_voterString(self, soln, row, col):
        vtr = soln[row][col]
        voterStringList = []
        voterStringList.append("Voter ID: {}\n - Loc:{}\n - District: {}\n"
                               " -    Party: {}\n".format(vtr.id, vtr.loc, vtr.district, vtr.party))
        for cardinal in vtr.nbrs:
            if vtr.has_nbr(cardinal):
                voterStringList.append(" -   {:>2}_nbr: {}\n".format(cardinal, vtr.nbrs[cardinal].get_id()))
            else:
                voterStringList.append(" -   {:>2}_nbr: {:>16}\n".format(cardinal, "None"))

        voterString = "".join(voterStringList)

        return voterString

    def print_state(self):
        print ("State of {:d} rows and {:d} columns".format(self.totalRows, self.totalCols))
        for row in range(self.totalRows):
            print ("|------------------------------------------------|")
            print ("|  Row: {:^3}                                      |".format(row))
            print ("|------------------------------------------------|")
            rowStringList = []
            for col in range(self.totalCols):
                rowStringList.append(self.get_voterString(self.voters, row, col) + "\n")
            rowString = "".join(rowStringList)
            print rowString

    def print_partyDivision(self):
            dPct = self.dCnt / float(self.totalVoters)
            rPct = self.rCnt / float(self.totalVoters)
            independentPct = self.independentCnt / float(self.totalVoters)

            print "|------------------------------------------------|"
            print "|  Party Division in population                  |"
            print "|------------------------------------------------|"
            print "|            d: {:>6.2%}                           |".format(dPct)
            print "|            r: {:>6.2%}                           |".format(rPct)
            print "|  Independent: {:>6.2%}                           |".format(independentPct)
            print "|------------------------------------------------|\n"

    def print_nDistrictVotesByParty(self, soln):
        districtVotes = {}
        d_districtVotes = 0
        r_districtVotes = 0

        for row in range(0, self.totalRows):
            for col in range(0, self.totalCols):
                districtKey = str(soln[row][col].get_district())

                if districtKey not in districtVotes:
                    districtVotes[districtKey] = 0

                if soln[row][col].get_party() == "D":
                    districtVotes[districtKey] += 1
                elif soln[row][col].get_party() == "R":
                    districtVotes[districtKey] -= 1

        for districtKey in districtVotes:
            if districtVotes[districtKey] > 0:
                d_districtVotes += 1
            elif districtVotes[districtKey] < 0:
                r_districtVotes += 1

        print "|------------------------------------------------|"
        print "|  Number of District Votes by Party             |"
        print "|------------------------------------------------|"
        print "|       d: {:>3}                                   |".format(d_districtVotes)
        print "|       r: {:>3}                                   |".format(r_districtVotes)
        print "|------------------------------------------------|\n"

    def print_districtLists(self, soln):
        districts = {}

        for row in range(0, self.totalRows):
            for col in range(0, self.totalCols):
                districtKey = str(soln[row][col].get_district())

                if districtKey not in districts:
                    districts[districtKey] = []

                districts[districtKey].append(soln[row][col])

        print "|------------------------------------------------|"
        print "|  Districts                                     |"
        print "|------------------------------------------------|"

        for districtKey in districts:
            districtStringList = []
            districtStringList.append(" District {:<3}:".format(int(districtKey)))
            for vtr in districts[districtKey]:
                [row, col] = vtr.get_loc()
                districtStringList.append("({},{})".format(row, col))
            districtString = " ".join(districtStringList)
            print districtString
        
        print "|------------------------------------------------|\n"    

    def print_solution(self,soln):
        print ("|------------------------------------------------|")
        print ("|  Solution:                                     |")
        print ("|------------------------------------------------|\n")

        columnHeadList = []
        columnHeadList.append("Row\\Col |")
        for col in range(0, self.totalCols):
            columnHeadList.append("{:>4}".format(col))
            columnHeadString = " ".join(columnHeadList)
        print columnHeadString
        print '---------' + ('-----' * self.totalCols)

        for row in range(0, self.totalRows):
            rowStringList = []
            rowStringList.append("{:<8}|".format(row))

            for col in range(0, self.totalCols):
                if soln[row][col].get_district() is not None:
                    rowStringList.append(" {:>2} ".format(soln[row][col].get_district()))
                else:
                    rowStringList.append(" -- ")
            rowString = " ".join(rowStringList)
            print rowString
        print '---------' + ('-----' * self.totalCols) + '\n'
        print ("|------------------------------------------------|")
        print ("|  Fitness: {}".format(self.fitness(soln)))
        print ("|------------------------------------------------|\n")




