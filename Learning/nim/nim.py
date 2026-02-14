import random


# NIM GAME LOGIC
class Nim:
    def __init__(self, piles=[1, 3, 5, 7]):
        # Each index represents a pile, value = number of objects in that pile
        self.piles = piles.copy()

        # Player 0 starts first, player 1 goes next (AI)
        self.player = 0

        # Will stay None until someone loses
        self.winner = None

    @staticmethod
    def available_actions(piles):
        # Figure out all the moves that are actually possible
        # Example: (pile_index, how_many_to_remove)
        actions = set()

        for i, pile in enumerate(piles):
            # You can remove at least 1 and at most the size of the pile
            for j in range(1, pile + 1):
                actions.add((i, j))

        return actions

    def move(self, action):
        pile, count = action

        # Safety check – don’t allow illegal moves
        if self.piles[pile] < count:
            raise Exception("Invalid move attempted")

        # Remove objects from the chosen pile
        self.piles[pile] -= count

        # Switch turn to the other player
        self.player = 1 - self.player

        # If all piles are empty, the previous player wins
        if all(p == 0 for p in self.piles):
            self.winner = 1 - self.player


# Q-LEARNING AI
class NimAI:
    def __init__(self, alpha=0.5, epsilon=0.1):
        # Q-table: (state, action) -> how good that action is
        self.q = dict()

        # Learning rate – how fast the AI updates its knowledge
        self.alpha = alpha

        # Exploration rate – how often the AI does random stuff
        self.epsilon = epsilon

    def get_q_value(self, state, action):
        # If we’ve seen this (state, action) before, return its value
        # Otherwise assume it’s neutral (0)
        return self.q.get((tuple(state), action), 0)

    def best_future_reward(self, state):
        # Look ahead: from this state, what’s the best score we can get?
        actions = Nim.available_actions(state)

        if not actions:
            return 0

        return max(self.get_q_value(state, action) for action in actions)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        # Core Q-learning formula
        # Slowly nudges old values toward better estimates
        self.q[(tuple(state), action)] = old_q + self.alpha * (
            reward + future_rewards - old_q
        )

    def update(self, state, action, reward, next_state):
        # Wrapper that updates the Q-table after a move
        old_q = self.get_q_value(state, action)
        future = self.best_future_reward(next_state)
        self.update_q_value(state, action, old_q, reward, future)

    def choose_action(self, state, epsilon=True):
        # Decide what to do next from the current state
        actions = list(Nim.available_actions(state))

        if not actions:
            return None

        # Sometimes explore random moves (learning phase)
        if epsilon and random.random() < self.epsilon:
            return random.choice(actions)

        # Otherwise, take the best move we currently know
        return max(actions, key=lambda a: self.get_q_value(state, a))


# TRAIN THE AI BY SELF-PLAY
def train(n):
    # Create a fresh AI agent
    ai = NimAI()

    # Let the AI play against itself n times
    for _ in range(n):
        game = Nim()

        # Track last move of each player so rewards can be assigned properly
        last_move = {0: None, 1: None}

        while True:
            state = game.piles.copy()
            action = ai.choose_action(state)

            # Remember what this player just did
            last_move[game.player] = (state, action)

            game.move(action)
            new_state = game.piles.copy()

            # If the game ends, assign rewards
            if game.winner is not None:
                # Losing move gets -1
                ai.update(state, action, -1, new_state)

                # Winning move gets +1
                ai.update(*last_move[game.player], 1, new_state)
                break
            else:
                # Neutral move – no win or loss yet
                ai.update(state, action, 0, new_state)

    return ai


# HUMAN vs AI GAME LOOP
def play(ai):
    game = Nim()

    while game.winner is None:
        print("\nCurrent piles:", game.piles)

        if game.player == 0:
            # Human turn
            pile = int(input("Choose pile index: "))
            count = int(input("How many to remove: "))
            action = (pile, count)
        else:
            # AI turn (no randomness here – pure logic)
            action = ai.choose_action(game.piles, epsilon=False)
            print(f"AI removes {action[1]} from pile {action[0]}")

        game.move(action)

    print("\nGAME OVER")
    print("Winner:", "Human" if game.winner == 0 else "AI")
