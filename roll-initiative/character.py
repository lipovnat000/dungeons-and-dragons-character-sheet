import classes
import random
import math
import utils

class Character:
    def __init__(self, name, level, ability_scores, class_name):
        self.name = name
        self.level = level
        self.class_name = class_name
        self.class_data = classes.CLASSES[class_name]

        # Ability scores
        self.str = ability_scores["str"]
        self.dex = ability_scores["dex"]
        self.con = ability_scores["con"]
        self.int = ability_scores["int"]
        self.wis = ability_scores["wis"]
        self.cha = ability_scores["cha"]

        self.hit_die = self.class_data["hit_die"]

        # Proficiencies
        self.skill_proficiencies = []
        self.saving_throw_proficiencies = self.class_data["saving_throws"]

        # Derived stats
        self.max_hp = self.calculate_max_hp()

        # Class features
        self.features = self.get_features_for_level()

        # Mechanical effects
        self.sneak_attack_dice = self.get_sneak_attack_dice()

    # --- Ability Modifiers ---
    @staticmethod
    def ability_mod(score):
        return math.floor((score - 10) / 2)

    @property
    def str_mod(self): return self.ability_mod(self.str)
    @property
    def dex_mod(self): return self.ability_mod(self.dex)
    @property
    def con_mod(self): return self.ability_mod(self.con)
    @property
    def int_mod(self): return self.ability_mod(self.int)
    @property
    def wis_mod(self): return self.ability_mod(self.wis)
    @property
    def cha_mod(self): return self.ability_mod(self.cha)

    # --- Derived Stats ---
    @property
    def proficiency_bonus(self):
        return 2 + ((self.level - 1) // 4)

    @property
    def initiative(self):
        return self.dex_mod

    @property
    def armor_class(self):
        return 10 + self.dex_mod

    # --- HP ---
    def calculate_max_hp(self):
        hp = self.hit_die + self.con_mod
        avg = math.ceil(self.hit_die / 2) + 1
        if self.level > 1:
            hp += (self.level - 1) * (avg + self.con_mod)
        return hp

    # --- Features ---
    def get_features_for_level(self):
        features = []
        for lvl, feats in self.class_data["features"].items():
            if lvl <= self.level:
                features.extend(feats)
        return features

    def get_sneak_attack_dice(self):
        dice = None
        for lvl, feats in self.class_data["features"].items():
            if lvl <= self.level:
                for f in feats:
                    if f["name"] == "Sneak Attack" and f["type"] == "mechanic":
                        dice = list(f["dice_per_level"].values())[0]
        return dice

    # ============================
    #       DIE ROLLER
    # ============================

    def roll_check(self, check_name, advantage=False, disadvantage=False):
        check_name = check_name.lower().strip()

        # Roll logic
        def roll_d20():
            r1 = random.randint(1, 20)
            r2 = random.randint(1, 20)

            if advantage:
                return max(r1, r2), (r1, r2)
            elif disadvantage:
                return min(r1, r2), (r1, r2)
            else:
                return r1, (r1,)

        # --- Saving Throw ---
        if check_name.endswith(" save") or check_name.endswith(" saving throw"):
            ability = check_name.split()[0][:3]
            mod = getattr(self, f"{ability}_mod")
            prof = self.proficiency_bonus if ability in self.saving_throw_proficiencies else 0

            result, rolls = roll_d20()
            total = result + mod + prof

            print(f"\nRolling {ability.upper()} Saving Throw:")
            print(f"  Rolls: {', '.join(str(r) for r in rolls)}")
            print(f"  Chosen: {result}")
            print(f"  Modifier: {mod:+}")
            print(f"  Proficiency: {prof:+}")
            print(f"  Total: {total}")

            if result == 20:
                print("  Critical Success!")
                return
            elif result == 1:
                print("  Critical Failure!")
                return
            return total

        # --- Skill Check ---
        if check_name in utils.SKILLS:
            ability = utils.SKILLS[check_name]
            mod = getattr(self, f"{ability}_mod")
            prof = self.proficiency_bonus if check_name in self.skill_proficiencies else 0

            result, rolls = roll_d20()
            total = result + mod + prof

            print(f"\nRolling {check_name.title()} Check:")
            print(f"  Rolls: {', '.join(str(r) for r in rolls)}")
            print(f"  Chosen: {result}")
            print(f"  Modifier ({ability.upper()}): {mod:+}")
            print(f"  Proficiency: {prof:+}")
            print(f"  Total: {total}")

            if result == 20:
                print("  Critical Success!")
                return
            elif result == 1:
                print("  Critical Failure!")
                return
            return total

        # --- Ability Check ---
        abilities = {}

        for abbr, fullname in utils.STATS.items():
            abilities[abbr] = abbr
            abilities[fullname.lower()] = abbr


        if check_name in abilities:
            ability = abilities[check_name]
            mod = getattr(self, f"{ability}_mod")

            result, rolls = roll_d20()
            total = result + mod

            print(f"\nRolling {check_name.title()} Check:")
            print(f"  Rolls: {', '.join(str(r) for r in rolls)}")
            print(f"  Chosen: {result}")
            print(f"  Modifier: {mod:+}")
            print(f"  Total: {total}")

            if result == 20:
                print("  Critical Success!")
                return
            elif result == 1:
                print("  Critical Failure!")
                return
            return total

        print(f"Unknown check: {check_name}")
        return None

    # --- Display ---
    def summary(self):
        print(f"=== {self.name} (Level {self.level} {self.class_name}) ===")
        print(f"STR {self.str} ({self.str_mod:+})")
        print(f"DEX {self.dex} ({self.dex_mod:+})")
        print(f"CON {self.con} ({self.con_mod:+})")
        print(f"INT {self.int} ({self.int_mod:+})")
        print(f"WIS {self.wis} ({self.wis_mod:+})")
        print(f"CHA {self.cha} ({self.cha_mod:+})")
        print()

        print(f"Proficiency Bonus: {self.proficiency_bonus:+}")
        print(f"Initiative: {self.initiative:+}")
        print(f"Armor Class: {self.armor_class}")
        print(f"Max HP: {self.max_hp}")
        print()

        print("Features:")
        for f in self.features:
            if f["type"] == "text":
                print(f" - {f['name']}")
            else:
                print(f" - {f['name']} ({self.sneak_attack_dice})")
