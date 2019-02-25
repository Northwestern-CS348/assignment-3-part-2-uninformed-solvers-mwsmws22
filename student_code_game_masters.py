from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        
        check_facts = ['fact: (on ?disk peg1)', 'fact: (on ?disk peg2)', 'fact: (on ?disk peg3)']
        result = []

        for fact in check_facts:
            check_peg = self.kb.kb_ask(parse_input(fact))
            peg = []
            if check_peg:
                for disk in check_peg:
                    peg.append(int(disk.bindings[0].constant.element[-1]))
                peg.sort()
                result.append(tuple(peg))
            else:
                result.append(tuple())

        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        state = self.getGameState()
        old_peg = state[int(movable_statement.terms[1].term.element[-1]) - 1][1:]
        new_peg = state[int(movable_statement.terms[2].term.element[-1]) - 1]

        self.kb.kb_retract(Fact(Statement(['top', movable_statement.terms[0], movable_statement.terms[1]])))

        if new_peg:
            self.kb.kb_retract(Fact(Statement(['top', 'disk' + str(new_peg[0]), movable_statement.terms[2]])))
        else:
            self.kb.kb_retract(Fact(Statement(['empty', movable_statement.terms[2]])))

        self.kb.kb_assert(Fact(Statement(['on', movable_statement.terms[0], movable_statement.terms[2]])))
        self.kb.kb_assert(Fact(Statement(['top', movable_statement.terms[0], movable_statement.terms[2]])))

        if old_peg:
            self.kb.kb_assert(Fact(Statement(['top', 'disk' + str(old_peg[0]), movable_statement.terms[1]])))
        else:
            self.kb.kb_assert(Fact(Statement(['empty', movable_statement.terms[1]])))

        self.kb.kb_retract(Fact(Statement(['on', movable_statement.terms[0], movable_statement.terms[1]])))

        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        check_facts = ['fact: (coordinate ?tile ?x pos1)', 'fact: (coordinate ?tile ?x pos2)',
                       'fact: (coordinate ?tile ?x pos3)']
        result = []

        for fact in check_facts:
            check_row = self.kb.kb_ask(parse_input(fact))
            row = [0, 0, 0]
            for tile in check_row:
                if tile.bindings[0].constant.element == 'empty':
                    row[int(tile.bindings[1].constant.element[-1])-1] = -1;
                else:
                    row[int(tile.bindings[1].constant.element[-1])-1] = int(tile.bindings[0].constant.element[-1])
            result.append(tuple(row))

        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        self.kb.kb_retract(Fact(Statement(['coordinate', movable_statement.terms[0], movable_statement.terms[1],
                                           movable_statement.terms[2]])))
        self.kb.kb_retract(Fact(Statement(['coordinate', 'empty', movable_statement.terms[3],
                                           movable_statement.terms[4]])))
        self.kb.kb_assert(Fact(Statement(['coordinate', movable_statement.terms[0], movable_statement.terms[3],
                                          movable_statement.terms[4]])))
        self.kb.kb_assert(Fact(Statement(['coordinate', 'empty', movable_statement.terms[1],
                                          movable_statement.terms[2]])))

        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
