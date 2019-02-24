from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.currentState.state = self.gm.getGameState()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            return True

        movables = self.gm.getMovables()
        self.visited[self.currentState] = True

        for move in movables:
            self.gm.makeMove(move)
            gs = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            if gs in self.visited:
                self.gm.reverseMove(move)
                continue
            self.currentState.children.append(gs)
            gs.parent = self.currentState
            self.gm.reverseMove(move)

        while self.currentState.nextChildToVisit < len(self.currentState.children):
            gs = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            if gs in self.visited:
                continue
            self.gm.makeMove(gs.requiredMovable)
            self.currentState = gs
            return False

        if self.current_state.parent:
            self.gm.reverseMove(self.current_state.requiredMovable)
            self.currentState = self.current_state.parent
        return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True