import math
import random
import re # Added this to make it easier to pull out integers

WIN_LINES = [
    [(0, 0), (0, 1), (0, 2)],  # rows
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],  # cols
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],  # diagonals
    [(0, 2), (1, 1), (2, 0)]
]


class GameBoard:

    def __init__(self):

        self.entries = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def print_bd(self):

        for i in range(3):
            for j in range(3):
                print(self.entries[i][j], end='')
            print('')

    def checkwin(self) -> int:

        for line in WIN_LINES:
            vals = [self.entries[r][c] for r, c in line]
            if vals == [1, 1, 1]:
                return 1
            if vals == [2, 2, 2]:
                return 2

        if any(0 in row for row in self.entries):
            return 0

        return 3

    def check_nextplayer(self, bd=None):
        count_1 = sum(cc == 1 for row in bd for cc in row)
        count_2 = sum(cc == 2 for row in bd for cc in row)
        return 1 if count_1 == count_2 else 2

    def getmoves(self):
        return [(r, c) for r in range(3) for c in range(3) if
                self.entries[r][c] == 0]  # all possible position where the board is empty

    def copy(self):
        new_board = GameBoard()
        new_board.entries = [row[:] for row in self.entries]
        return new_board


class MCTSNode:
    def __init__(self, bd: GameBoard, parent: None, action: None):
        self.bd = bd
        self.parent = parent
        self.action = action  # action that led to this node
        self.children = []  # list of child nodes
        self.possible_moves = bd.getmoves()  # moves that can be played from this node
        self.visits = 0
        self.wins = 0.0

    def is_fully_expanded(self):
        return len(self.possible_moves) == 0

    def is_terminal(self):
        return self.bd.checkwin() != 0


def apply_action(bd: GameBoard, action, player):
    r, c = action
    new_bd = bd.copy()
    new_bd.entries[r][c] = player
    return new_bd


class MCTS:
    def __init__(self, c=math.sqrt(2)):
        self.c = c

    def uct_select(self, node: MCTSNode, c=None) -> MCTSNode:
        # node: current node
        # return: child node with highest UCT value
        if c is None:
            c = self.c
        return max(node.children,
                   key=lambda child: (child.wins / child.visits) + c * math.sqrt(math.log(node.visits) / child.visits))

    def expand(self, node: MCTSNode) -> MCTSNode:
        # node: current node
        # return: new child node after applying one of the possible moves

        action = node.possible_moves.pop()
        r, c = action

        child_bd = node.bd.copy()
        player = child_bd.check_nextplayer(child_bd.entries)
        child_bd = apply_action(child_bd, action, player)

        child_node = MCTSNode(child_bd, parent=node, action=action)
        node.children.append(child_node)
        return child_node

    def rollout(self, bd: GameBoard) -> int:
        # bd: current board
        # return: score on the same (+1: for winner player)

        rollout_bd = bd.copy()

        while rollout_bd.checkwin() == 0:
            next_player = rollout_bd.check_nextplayer(rollout_bd.entries)
            actions = rollout_bd.getmoves()
            if not actions:
                break
            action = random.choice(actions)
            rollout_bd = apply_action(rollout_bd, action, next_player)

        winner = rollout_bd.checkwin()
        if winner == 1 or winner == 2:
            return +1
        else:
            return 0

    def backpropagate(self, node: MCTSNode, reward: int):
        current = node
        while current is not None:
            current.visits += 1
            current.wins += reward
            # switch perspective
            reward = -reward

            # propagate to parent
            current = current.parent

    def search(self, root: MCTSNode, iter=2000):
        # based on the rood board, run MCTS and return the best action
        # root = MCTSNode(root_bd, parent=None, action=None)
        root_bd = root.bd
        if root_bd.checkwin() != 0:
            raise ValueError("Game is over")

        for _ in range(iter):
            node = root

            # selection
            while (not node.is_terminal()) and node.is_fully_expanded():
                node = self.uct_select(node, c=self.c)

            # expansion
            if (not node.is_terminal()) and (not node.is_fully_expanded()):
                node = self.expand(node)

            # simulation
            reward = self.rollout(node.bd)

            # backpropagation
            self.backpropagate(node, reward)
        self.c = 0
        best_child = self.uct_select(root, c=0)
        return best_child.action


def MCTS_move(root_state: GameBoard, iterations=2000):
    mcts = MCTS()
    root_node = MCTSNode(bd=root_state, parent=None, action=None)

    best_action = mcts.search(root_node, iter=iterations)
    player = root_state.check_nextplayer(root_state.entries)
    next_state = apply_action(root_state, best_action, player)

    return best_action, player, next_state

def _parse_move_input(s: str):
    nums = re.findall(r'\d+', s)
    if len(nums) < 2:
        return None
    try:
        r = int(nums[0]) - 1
        c = int(nums[1]) - 1
    except ValueError:
        return None
    if 0 <= r <= 2 and 0 <= c <= 2:
        return (r,c)
    return None


def human_vs_mcts_interactive():
    print("Human vs MCTS TicTacToe")
    while True:
        side = input("Would you like to play as X or O?: ").strip().upper()
        if side in ("X", "O"):
            break
        print("Please enter X or O.")
    human = 1 if side == "X" else 2

    while True:
        it_s = input("MCTS iterations for engine (press Enter for 2000). The higher the number the more optimized the computer is! : ").strip()
        if it_s == "":
            iterations = 2000
            break
        if it_s.isdigit() and int(it_s) > 0:
            iterations = int(it_s)
            break
        print("Please enter a positive integer or leave blank for 2000 iterations.")

    bd = GameBoard()

    while True:
        print("Current board:")
        bd.print_bd()
        state = bd.checkwin()
        if state != 0:
            if state == 3:
                print("Game ended in a draw.")
            elif state == 1:
                print("Player X wins!")
            else:
                print(f"Player 0 wins!")
            break

        next_player = bd.check_nextplayer(bd.entries)
        if next_player == human:
            while True:
                raw = input("Enter your move as row,col with values 1,2,3: ").strip()
                mv = _parse_move_input(raw)
                if mv is None:
                    print("Invalid input. Please enter two numbers like '1,3'. Please do not include letters!")
                    continue
                r, c = mv
                if bd.entries[r][c] != 0:
                    print("Cell occupied; pick another.")
                    continue
                bd = apply_action(bd, (r, c), human)
                break
        else:
            print("MCTS thinking...")
            best_action, player, bd = MCTS_move(bd, iterations=iterations)
            print(f"MCTS plays at (row,col) = ({best_action[0] + 1},{best_action[1] + 1})")

    print("Final board:")
    bd.print_bd()

if __name__ == "__main__":
    human_vs_mcts_interactive()