import random

# Define a player
class Player:
    def __init__(self, name):
        self.name = name
        self.speed = 5
        self.power = 5
        self.accuracy = 5
        self.strategy = 5
        self.energy = 100

    def train(self, skill):
        if self.energy >= 10:
            setattr(self, skill, getattr(self, skill) + random.randint(1, 3))
            self.energy -= 10
            print(f"{self.name} trained {skill}! {skill.capitalize()} is now {getattr(self, skill)}.")
        else:
            print(f"{self.name} is too tired to train. Rest needed!")

    def rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"{self.name} rested. Energy is now {self.energy}.")

# Define a match
def match(player, opponent_name):
    print(f"A match begins between {player.name} and {opponent_name}!")
    player_score = player.accuracy + random.randint(-5, 5)
    opponent_score = random.randint(5, 15)

    if player_score > opponent_score:
        print(f"{player.name} wins with a score of {player_score} to {opponent_score}!")
    else:
        print(f"{opponent_name} wins with a score of {opponent_score} to {player_score}. Keep training!")

# Main game loop
def main():
    print("Welcome to Blue Lock!")
    name = input("Enter your player's name: ")
    player = Player(name)

    while True:
        print("\nWhat do you want to do?")
        print("1. Train")
        print("2. Rest")
        print("3. Play a match")
        print("4. Quit")
        choice = input("> ")

        if choice == "1":
            skill = input("Which skill to train? (speed/power/accuracy/strategy): ")
            if skill in ["speed", "power", "accuracy", "strategy"]:
                player.train(skill)
            else:
                print("Invalid skill!")
        elif choice == "2":
            player.rest()
        elif choice == "3":
            opponent_name = f"Player{random.randint(1, 100)}"
            match(player, opponent_name)
        elif choice == "4":
            print("Thanks for playing Blue Lock!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
