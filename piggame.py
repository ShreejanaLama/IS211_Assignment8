import random
import argparse
import time

# This is a Die class. It rolls numbers between 1 to 6 like a normal dice.
class Die:
    def __init__(self):
        random.seed(0)  # makes it so the dice rolls same numbers for testin
    
    def roll(self):
        return random.randint(1, 6)  # roll dice


# This is the main player class
class Player:
    def __init__(self, name):
        self.name = name  # player name
        self.score = 0    # score starts at zero
    
    def reset_score(self):
        self.score = 0  # reset score when game restart

    # human players takes their turn
    def take_turn(self, die):
        turn_total = 0
        print(f"{self.name}'s turn! Current score: {self.score}")
        while True:
            choice = input("Enter 'r' to roll or 'h' to hold: ").strip().lower()
            if choice == 'r':
                roll = die.roll()
                print(f"Rolled: {roll}")
                if roll == 1:
                    print("Oops! Rolled a 1. No points for this turn.")
                    return 0
                else:
                    turn_total += roll
                    print(f"Turn total: {turn_total}, Total score if held: {self.score + turn_total}")
            elif choice == 'h':
                return turn_total
            else:
                print("Invalid input. Try again!")


# Computer player class. It uses simple strategy.
class ComputerPlayer(Player):
    def take_turn(self, die):
        turn_total = 0
        print(f"{self.name}'s turn! (Computer) Current score: {self.score}")
        while True:
            roll = die.roll()
            print(f"Rolled: {roll}")
            if roll == 1:
                print("Oops! Rolled a 1. No points for this turn.")
                return 0
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}, Total score if held: {self.score + turn_total}")
                # computer will hold at 25 or if it would win the game
                if turn_total >= min(25, 100 - self.score):
                    print(f"{self.name} holds.")
                    return turn_total


# Factory class makes the player (human or computer)
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")


# This is the main Pig game class
class PigGame:
    def __init__(self, player1, player2):
        self.die = Die()
        self.players = [player1, player2]
        self.current_player_index = 0
        self.winning_score = 100

    # switch to next player's turn
    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % 2

    # play one turn
    def play_turn(self):
        player = self.players[self.current_player_index]
        turn_points = player.take_turn(self.die)
        player.score += turn_points
        print(f"{player.name} ends turn with score: {player.score}")
        self.switch_turn()

    # main game loop
    def play_game(self):
        print("Welcome to the Pig Game!")
        while all(p.score < self.winning_score for p in self.players):
            self.play_turn()

        winner = max(self.players, key=lambda p: p.score)
        print(f"{winner.name} wins with a score of {winner.score}!")
        self.reset_game()

    # reset game for another round
    def reset_game(self):
        for player in self.players:
            player.reset_score()
        self.current_player_index = 0
        print("Game reset. Ready for a new round!")

# this class is for the time version of the game
# it stops the game if it takes more than 1 min
class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.time_limit = 60  # time in seconds, 1 min

    def play_game(self):
        print("Timed Pig Game! You have 1 minute.")
        start_time = time.time()  # remember when game start

        # keep playing while no one won and time not run out
        while all(p.score < self.game.winning_score for p in self.game.players):
            elapsed = time.time() - start_time  # check how much time gone
            if elapsed > self.time_limit:
                print("Time's up!")  # oops too late
                break

            # get the current player and show how much time is left
            current_player = self.game.players[self.game.current_player_index]
            print(f"\n{current_player.name}'s turn (Time left: {int(self.time_limit - elapsed)}s)")
            turn_start = time.time()  # (not really using this but still)

            # let player do there turn
            turn_points = current_player.take_turn(self.game.die)

            # after turn, check time again
            elapsed = time.time() - start_time
            if elapsed > self.time_limit:
                print("Time's up during the turn!")  # late again lol
                break

            # add points they got in this turn
            current_player.score += turn_points
            print(f"{current_player.name} ends turn with score: {current_player.score}")
            self.game.switch_turn()  # now other player go

        # game is over, pick the winner (most points)
        winner = max(self.game.players, key=lambda p: p.score)
        print(f"\n{winner.name} wins with a score of {winner.score}!")  # yay winner
        self.game.reset_game()  # start over if play again


# main game part
if __name__ == "__main__":
    # not using CLI stuff, just setting players myself
    player1 = PlayerFactory.create_player("human", "Player 1")
    player2 = PlayerFactory.create_player("computer", "Player 2")

    # set to True if you want the timer on
    use_timed = True

    base_game = PigGame(player1, player2)
    game = TimedGameProxy(base_game) if use_timed else base_game

    # loop to play again if player wants to
    while True:
        game.play_game()
        play_again = input("Do you want to play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")  # bye!
            break
