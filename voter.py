'''
Voter.py - Class
Author: John Dunn
Date: Oct. 3, 2016

This class serves to create a Voter object which has certain properties and neighbors.
In this respect, if is similar to the objects in linked lists.
'''
import re

class Voter:

    def __init__(
            self, id, loc = None, district = None, party=None,
            n_nbr=None, ne_nbr=None, e_nbr=None, se_nbr=None,
            s_nbr=None, sw_nbr=None, w_nbr=None, nw_nbr=None
    ):
        self.id = id
        self.loc = loc
        self.district = district
        self.party = party
        self.nbrs = {}
        # The order in which these are added to the dictionary matters
        # for iterating through neighbors in state.py
        self.nbrs['n'] = n_nbr
        self.nbrs['s'] = s_nbr
        self.nbrs['e'] = e_nbr
        self.nbrs['w'] = w_nbr
        self.nbrs['ne'] = ne_nbr
        self.nbrs['sw'] = sw_nbr
        self.nbrs['nw'] = nw_nbr
        self.nbrs['se'] = se_nbr
        self.visited = False

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_loc(self):
        return self.loc

    def set_loc(self,loc):
        self.loc = loc

    def get_district(self):
        return self.district

    def set_district(self, district):
        self.district = district

    def get_party(self):
        return self.party

    def set_party(self, party):
        self.party = party

    def get_nbr(self, cardinal_key):
        assert(cardinal_key in self.nbrs), "{s} is not a key in nbrs dic.".format(cardinal_key)
        return self.nbr[cardinal_key]

    def set_nbr(self, cardinal_key, nbr):
        # Adding a neighbor is dual relationship
        # self <-- Neighboring --> nbr
        assert(cardinal_key in self.nbrs), "{s} is not a key in nbrs dic.".format(cardinal_key)

        self.nbrs[cardinal_key] = nbr

        if cardinal_key == 'n':
            nbr.nbrs['s'] = self
        elif cardinal_key == 'ne':
            nbr.nbrs['sw'] = self
        elif cardinal_key == 'e':
            nbr.nbrs['w'] = self
        elif cardinal_key == 'se':
            nbr.nbrs['nw'] = self
        elif cardinal_key == 's':
            nbr.nbrs['n'] = self
        elif cardinal_key == 'sw':
            nbr.nbrs['ne'] = self
        elif cardinal_key == 'w':
            nbr.nbrs['e'] = self
        elif cardinal_key == 'nw':
            nbr.nbrs['se'] = self

    def has_nbr(self, cardinal_key):
        assert(cardinal_key in self.nbrs), "{s} is not a key in nbrs dic.".format(cardinal_key)

        if self.nbrs[cardinal_key] is not None:
            return True
        else:
            return False

    def isVisited(self):
        return self.visited

    def set_visited(self, val):
        self.visited = val
