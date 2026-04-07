import utils
from classes import CLASSES
from character import Character
import random


class CharacterCreator:
    def __init__(self):
        self.name = None
        self.class_name = None
        self.level = 1
        self.ability_scores = {}

    # -----------------------------
    #   PUBLIC ENTRY POINT
    # -----------------------------
    def create(self):
        self.ask_name()
        self.ask_class()
        self.choose_ability_scores()
        return self.finalize()

    # -----------------------------
    #   STEP 1 — NAME
    # -----------------------------
    def ask_name(self):
        print("Hello, welcome to the character creator!")
        print("What is your character's name?")
        self.name = input().strip()

    # -----------------------------
    #   STEP 2 — CLASS
    # -----------------------------
    def ask_class(self):
        print("Great! What is your character's class?")
        while True:
            choice = input().strip()
            if choice in CLASSES:
                self.class_name = choice
                break
            print("Sorry, that's not a valid class. Please try again.")

    # -----------------------------
    #   STEP 3 — ABILITY SCORES
    # -----------------------------
    def choose_ability_scores(self):
        print("By default we start at level 1.")
        print("Choose how to generate ability scores:")
        print("1. Randomly generate")
        print("2. Roll a set of scores (4d6 drop lowest)")
        print("3. Point buy")

        while True:
            choice = input().strip()
            if choice == "1":
                self.random_scores()
                return
            elif choice == "2":
                self.arranged_scores()
                return
            elif choice == "3":
                self.point_buy()
                return
            else:
                print("Please choose 1, 2, or 3.")

    def random_scores(self):
        while True:
            ability_scores = {
                "str": random.randint(3, 18),
                "dex": random.randint(3, 18),
                "con": random.randint(3, 18),
                "int": random.randint(3, 18),
                "wis": random.randint(3, 18),
                "cha": random.randint(3, 18)
            }

            print("Here are your ability scores:")
            for k, v in ability_scores.items():
                print(f"{k.upper()}: {v}")

            print("Is this okay? (y/n)")
            if input().lower() == "y":
                self.ability_scores = ability_scores
                return

    def score_roller(self):
        score_set = []
        calculate_score = []
        for i in range(6):
            for i in range(4):
                calculate_score.append(utils.d6.roll())
            calculate_score.sort()
            calculate_score.pop(0)
            score_set.append(sum(calculate_score))
            calculate_score = []
        return score_set

    def arranged_scores(self):
        while True:
            ability_scores = {
                "str": None,
                "dex": None,
                "con": None,
                "int": None,
                "wis": None,
                "cha": None
            }
            score_set = self.score_roller()
            print("Great! Here is your set of ability scores: ")
            for score in score_set:
                print(score)

            for ability in ["str", "dex", "con", "int", "wis", "cha"]:
                print(f"What would you like your {utils.STATS[ability]} to be?")
                valid_score = False
                while not valid_score:
                    score_choice = int(input())
                    if score_choice not in score_set:
                        print("Please choose one of the remaining score options.")
                    else:
                        ability_scores[ability.lower()] = score_choice
                        for score in score_set:
                            if score == score_choice:
                                score_set.remove(score)
                                break
                        
                        print(f"Your {ability} is {score_choice}")
                        print("----------------------------------")


                        for score in score_set:
                            print(score)

                        valid_score = True




            print("Great! Here are your ability scores: ")

            for ability in ability_scores:
                print(f"{utils.STATS[ability]}: {ability_scores[ability]}")

            print("Is this okay? (y/n)")
            confirm = input()
            if confirm == "y":
                self.ability_scores = ability_scores
                return

    def point_buy(self):
        costs = {
            1: 9,
            2: 10,
            3: 11,
            4: 12,
            5: 13,
            7: 14,
            9: 15
        }
        while True:
            ability_scores = {
                "str": 8,
                "dex": 8,
                "con": 8,
                "int": 8,
                "wis": 8,
                "cha": 8
            }
            ability_points = 27
            remaining_scores = ["str", "dex", "con", "int", "wis", "cha"]

            print("Great! Each of your ability scores start at 8 and you can increase them with 27 total points.")
            print("Here are the costs for increasing any individual score:")
            print("Score    Cost")
            print("-------------")
            for j, k in costs.items():
                print(f"{j}        {k}")


            while ability_points > 0:
                print(f"You have {ability_points} ability points remaining.")
                print("Which ability would you like to increase?")
                for i in remaining_scores:
                    print(f"{remaining_scores[i]}")

                ability = input()
                if ability not in ability_scores:
                    print("Please choose a valid ability.")
                else:
                    print(f"How many points would you like to spend on {ability}?")
                    points = input()
                    if int(points) > ability_points:
                        print("You don't have enough points.")
                    else:
                        ability_points -= int(points)
                        ability_scores[ability] += int(costs[int(points)])
                        remaining_scores.remove(ability)
                    

            print("Great! Here are your ability scores: ")
            print(f"STR: {ability_scores['str']}")
            print(f"DEX: {ability_scores['dex']}")
            print(f"CON: {ability_scores['con']}")
            print(f"INT: {ability_scores['int']}")
            print(f"WIS: {ability_scores['wis']}")
            print(f"CHA: {ability_scores['cha']}")

            print("Is this okay? (y/n)")
            confirm = input()
            if confirm == "y":
                self.ability_scores = ability_scores
                return

    # -----------------------------
    #   FINALIZE CHARACTER
    # -----------------------------
    def finalize(self):
        return Character(
            self.name,
            self.level,
            self.ability_scores,
            self.class_name
        )
