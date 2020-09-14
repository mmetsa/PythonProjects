"""Dungeons and Pythons."""
import math


class Adventurer:
    """Represent an Adventurer."""

    def __init__(self, name: str, class_type: str, power: int, experience=0):
        """Initialise.

        :param name: The name of the Adventurer.
        :param class_type: Adventurer's class: Possible class types are ['Fighter', 'Druid', 'Wizard', 'Paladin'].
        :param power: The Power of the Adventurer.
        :param experience: How much Experience the Adventurer has. (Starts with 0).
        """
        self.name = name
        if class_type in ["Fighter", "Druid", "Wizard", "Paladin"]:
            self.class_type = class_type
        else:  # All other class_type's are invalid, so they are converted to 'Fighter'.
            self.class_type = "Fighter"
        self.power = power
        self.experience = experience

    def add_experience(self, exp: int):
        """Add experience to the Adventurer.

        :param exp: Experience to add.
        """
        self.experience += exp
        return

    def add_power(self, power: int):
        """Add power to the Adventurer.

        :param power: Power to add.
        """
        self.power += power
        return

    def __repr__(self):
        """Print the Adventurer."""
        return f"{self.name}, the {self.class_type}, Power: {self.power}, Experience: {self.experience}."


class Monster:
    """Represent a Monster."""

    def __init__(self, name: str, mon_type: str, power=0):
        """Initialise a Monster.

        :param name: The name of the Monster.
        :param mon_type: The type of the Monster.
        :param power: The power of the Monster.
        """
        self.mon_type = mon_type
        self.power = power
        self.name = name

    @property
    def monster_name(self):
        """The name of the monster."""
        # If the Monster is a Zombie, they have "Undead" in front of their name.
        if self.mon_type == "Zombie":
            return f"Undead {self.name}"
        else:
            return self.name

    def __repr__(self):
        """Print the monster."""
        return f"{self.monster_name} of type {self.mon_type}, Power: {self.power}."


class World:
    """Represent the World."""

    def __init__(self, PM: str):
        """Initialise the World.

        :param PM: The Python Master.
        """
        self.PM = PM
        self.has_necromancers = False
        self.adventurerlist = []
        self.monsterlist = []
        self.graveyard = []
        self.active_adventurers = []
        self.active_monsters = []

    def change_necromancer(self, bool):
        """Change the status of the necromancers.

        :param bool: The boolean to change the status to.
        """
        self.has_necromancers = bool
        return

    def revive_graveyard(self):
        """Revive the graveyard.

        The graveyard can only be revived when there are necromancers in the World.
        """
        if not self.has_necromancers:
            return
        for elem in self.graveyard:
            if isinstance(elem, Monster):
                # All Monsters go to the monsterlist as Zombies.
                if elem.mon_type != "Zombie":
                    elem.mon_type = "Zombie"
                    elem.name = "Undead " + elem.name
                self.monsterlist.append(elem)
            elif isinstance(elem, Adventurer):
                # All Adventurers go to the monsterlist as Zombie + class_type's.
                monster = Monster("Undead " + elem.name, "Zombie " + elem.class_type, elem.power)
                self.monsterlist.append(monster)
        self.has_necromancers = False
        # Graveyard has to be empty.
        self.graveyard.clear()

    def get_adventurerlist(self):
        """Get the adventurer list.

        This does not take active adventurers into account.
        """
        adventurer_list = []
        for elem in self.adventurerlist:
            if elem in self.active_adventurers:
                continue
            adventurer_list.append(elem)
        return adventurer_list

    def add_strongest(self, class_type: str):
        """Add the strongest Adventurer to the adventurer list by class_type.

        :param class_type: The class of the Adventurer.
        """
        strongest = 0
        strongest_index = 0
        for elem in self.adventurerlist:
            if elem.class_type == class_type and elem not in self.active_adventurers:
                if elem.power > strongest:
                    strongest = elem.power
                    strongest_index = self.adventurerlist.index(elem)
        self.active_adventurers.append(self.adventurerlist[strongest_index])
        self.adventurerlist.pop(strongest_index)
        return

    def add_weakest(self, class_type: str):
        """Add the weakest Adventurer to the adventurer list by class_type."""
        weakest = float('inf')
        weakest_index = 0
        for elem in self.adventurerlist:
            if elem.class_type == class_type and elem not in self.active_adventurers:
                if elem.power < weakest:
                    weakest = elem.power
                    weakest_index = self.adventurerlist.index(elem)
        self.active_adventurers.append(self.adventurerlist[weakest_index])
        self.adventurerlist.pop(weakest_index)

    def add_most_experience(self, class_type):
        """Add the most experienced Adventurer to the adventurer list by class_type."""
        most_experience = 0
        most_experience_index = 0
        for elem in self.adventurerlist:
            if elem.class_type == class_type and elem not in self.active_adventurers:
                if elem.experience > most_experience:
                    most_experience = elem.experience
                    most_experience_index = self.adventurerlist.index(elem)
        self.active_adventurers.append(self.adventurerlist[most_experience_index])
        self.adventurerlist.pop(most_experience_index)

    def add_least_experience(self, class_type):
        """Add the most experienced Adventurer to the adventurer list by class_type."""
        least_experience = float('inf')
        least_experience_index = 0
        for elem in self.adventurerlist:
            if elem.class_type == class_type and elem not in self.active_adventurers:
                if elem.experience < least_experience:
                    least_experience = elem.experience
                    least_experience_index = self.adventurerlist.index(elem)
        self.active_adventurers.append(self.adventurerlist[least_experience_index])
        self.adventurerlist.pop(least_experience_index)

    def add_by_name(self, name: str):
        """Add the Adventurer by name."""
        for elem in self.adventurerlist:
            if elem.name == name and elem not in self.active_adventurers:
                self.active_adventurers.append(elem)
                self.adventurerlist.remove(elem)
                return

    def add_all_of_class_type(self, class_type):
        """Add all Adventurers of class_type."""
        temp_list = []
        for elem in self.adventurerlist:
            if elem.class_type == class_type and elem not in self.active_adventurers:
                self.active_adventurers.append(elem)
                temp_list.append(elem)
        for elem in temp_list:
            if elem in self.adventurerlist:
                self.adventurerlist.remove(elem)
        return

    def add_all(self):
        """Add all adventurers to active list."""
        for elem in self.adventurerlist:
            if elem not in self.active_adventurers:
                self.active_adventurers.append(elem)
        for elem in self.active_adventurers:
            if elem in self.adventurerlist:
                self.adventurerlist.remove(elem)
        return

    def get_active_adventurers(self):
        """Get all the active adventurers.

        Sort them by experience descending
        """
        adventurers = sorted(self.active_adventurers, key=lambda x: x.experience, reverse=True)
        return adventurers

    def add_monster_by_name(self, name: str):
        """Add the strongest Monster to active list by name."""
        for elem in self.monsterlist:
            if elem.name == name and elem not in self.active_monsters:
                self.active_monsters.append(elem)
                self.monsterlist.remove(elem)
                return

    def add_strongest_monster(self):
        """Add the strongest Monster to active list."""
        strongest = 0
        strongest_index = 0
        for elem in self.monsterlist:
            if elem not in self.active_adventurers:
                if elem.power > strongest:
                    strongest = elem.power
                    strongest_index = self.monsterlist.index(elem)
        self.active_monsters.append(self.monsterlist[strongest_index])
        self.monsterlist.pop(strongest_index)
        return

    def add_weakest_monster(self):
        """Add the weakest Monster to active list."""
        weakest = float('inf')
        weakest_index = 0
        for elem in self.monsterlist:
            if elem not in self.active_adventurers:
                if elem.power < weakest:
                    weakest = elem.power
                    weakest_index = self.monsterlist.index(elem)
        self.active_monsters.append(self.monsterlist[weakest_index])
        self.monsterlist.pop(weakest_index)
        return

    def add_all_of_type(self, mon_type):
        """Add all same type monsters to active list."""
        for elem in self.monsterlist:
            if elem.mon_type == mon_type and elem not in self.active_monsters:
                self.active_monsters.append(elem)
        for elem in self.active_monsters:
            if elem in self.monsterlist:
                self.monsterlist.remove(elem)
        return

    def add_all_monsters(self):
        """Add all the monsters to the active list."""
        for elem in self.monsterlist:
            if elem not in self.active_monsters:
                self.active_monsters.append(elem)
        for elem in self.active_monsters:
            if elem in self.monsterlist:
                self.monsterlist.remove(elem)
        return

    def get_active_monsters(self):
        """Get all the active monsters.

        Sort by their power descending.
        """
        active_list = sorted(self.active_monsters, key=lambda x: x.power, reverse=True)
        return active_list

    def remove_character(self, name: str):
        """Remove a character from the world."""
        for elem in self.adventurerlist:
            if elem.name == name:
                self.adventurerlist.remove(elem)
                return
        for elem in self.monsterlist:
            if elem.monster_name == name:
                self.monsterlist.remove(elem)
                return
        for elem in self.graveyard:
            if isinstance(elem, Adventurer):
                if elem.name == name:
                    self.graveyard.remove(elem)
                    return
            elif isinstance(elem, Monster):
                if elem.monster_name == name:
                    self.graveyard.remove(elem)
                    return
        return

    def get_python_master(self):
        """Get the python master."""
        return self.PM

    def get_monsterlist(self):
        """Get the Monster list."""
        return self.monsterlist

    def add_adventurer(self, adventurer: Adventurer):
        """Add an adventurer to the adventurer list."""
        if isinstance(adventurer, Adventurer):
            self.adventurerlist.append(adventurer)
        return

    def add_monster(self, monster: Monster):
        """Add a Monster to the monster list."""
        if isinstance(monster, Monster):
            self.monsterlist.append(monster)
        return

    def get_graveyard(self):
        """Get the Graveyard list."""
        return self.graveyard

    def has_druids(self):
        """Check if active adventurers have druids."""
        for elem in self.active_adventurers:
            if elem.class_type == "Druid":
                return True
        return False

    def remove_animals_and_ents(self):
        """Remove all Animals and Ents."""
        list_of_monsters = []
        for elem in self.active_monsters:
            if elem.mon_type == "Animal" or elem.mon_type == "Ent":
                list_of_monsters.append(elem)
        for elem in list_of_monsters:
            if elem in self.active_monsters:
                self.active_monsters.remove(elem)
                self.monsterlist.append(elem)
        return

    def has_zombies(self):
        """Check if there are Zombies in active monsters."""
        for elem in self.active_monsters:
            if elem.mon_type == "Zombie" or elem.mon_type == "Zombie Fighter" or elem.mon_type == "Zombie Druid" \
                    or elem.mon_type == "Zombie Paladin" or elem.mon_type == "Zombie Wizard":
                return True
        return False

    def double_paladin_power(self):
        """Double the power of paladin adventurers."""
        for elem in self.active_adventurers:
            if elem.class_type == "Paladin":
                elem.power *= 2
        return

    def total_adventurer_power(self):
        """Calculate the power of the adventurers."""
        total_power = 0
        for elem in self.active_adventurers:
            total_power += elem.power
        return total_power

    def total_monster_power(self):
        """Calculate the power of the monsters."""
        total_power = 0
        for elem in self.active_monsters:
            total_power += elem.power
        return total_power

    def add_experience(self, experience):
        """Add experience to adventurers."""
        for elem in self.active_adventurers:
            elem.experience += experience
        return

    def clear_active_lists(self):
        """Clear active adventurers."""
        for elem in self.active_adventurers:
            self.adventurerlist.append(elem)
        self.active_adventurers.clear()
        if self.active_monsters:
            for elem in self.active_monsters:
                self.monsterlist.append(elem)
            self.active_monsters.clear()
        return

    def go_adventure(self, deadly=False):
        """Go on an adventure."""
        tied = False
        if self.has_druids():
            self.remove_animals_and_ents()

        if self.has_zombies():
            self.double_paladin_power()

        total_mon_power = self.total_monster_power()

        if self.total_adventurer_power() > self.total_monster_power() and deadly:
            # Deadly fight and Adventurers won so active monsters go to the graveyard.
            for elem in self.active_monsters:
                self.graveyard.append(elem)
            self.active_monsters.clear()
        elif self.total_adventurer_power() < self.total_monster_power() and deadly:
            # Deadly fight and Monsters won so active adventurers go to the graveyard.
            for elem in self.active_adventurers:
                self.graveyard.append(elem)
            self.active_adventurers.clear()
        else:
            # The game was tied.
            tied = True
        if self.active_adventurers:
            # If the active adventurers list is not empty, they won or it was a draw So give them exp.
            num_of_adventurers = len(self.active_adventurers)
            experience = total_mon_power / num_of_adventurers
            if deadly:
                experience *= 2
            if tied:
                experience = experience / 2
            experience = math.floor(experience)
            print(experience)
            self.add_experience(experience)
            self.clear_active_lists()


if __name__ == "__main__":
    print("Kord oli maailm.")
    Maailm = World("Sõber")
    print(Maailm.get_python_master())  # -> "Sõber"
    print(Maailm.get_graveyard())  # -> []
    print()
    print("Tutvustame tegelasi.")
    Kangelane = Adventurer("Sander", "Paladin", 50)
    Tüütu_Sõber = Adventurer("XxX_Eepiline_Sõdalane_XxX", "Tulevikurändaja ja ninja", 999999)
    Lahe_Sõber = Adventurer("Peep", "Druid", 25)
    Teine_Sõber = Adventurer("Toots", "Wizard", 40)

    print(Kangelane)  # -> "Sander, the Paladin, Power: 50, Experience: 0."
    # Ei, tüütu sõber, sa ei saa olla tulevikurändaja ja ninja, nüüd sa pead fighter olema.
    print(Tüütu_Sõber)  # -> "XxX_Eepiline_Sõdalane_XxX, the Fighter, Power: 999999, Experience: 0."

    print("Sa ei tohiks kohe alguses ka nii tugev olla.")
    Tüütu_Sõber.add_power(-999959)
    print(Tüütu_Sõber)  # -> XxX_Eepiline_Sõdalane_XxX, the Fighter, Power: 40, Experience: 0.
    print()
    print(Lahe_Sõber)  # -> "Peep, the Druid, Power: 25, Experience: 0."
    print(Teine_Sõber)  # -> "Toots, the Wizard, Power: 40, Experience: 0."
    print()
    Lahe_Sõber.add_power(20)
    print("Sa tundud kuidagi nõrk, ma lisasin sulle natukene tugevust.")
    print(Lahe_Sõber)  # -> "Peep, the Druid, Power: 45, Experience: 0."

    Maailm.add_adventurer(Kangelane)
    Maailm.add_adventurer(Lahe_Sõber)
    Maailm.add_adventurer(Teine_Sõber)
    print(Maailm.get_adventurerlist())  # -> Sander, Peep ja Toots

    Maailm.add_monster(Tüütu_Sõber)
    # Ei, tüütu sõber, sa ei saa olla vaenlane.
    print(Maailm.get_monsterlist())  # -> []
    Maailm.add_adventurer(Tüütu_Sõber)

    print()
    print()
    print("Oodake veidikene, ma tekitan natukene kolle.")
    Zombie = Monster("Rat", "Zombie", 10)
    GoblinSpear = Monster("Goblin Spearman", "Goblin", 45)
    GoblinArc = Monster("Goblin Archer", "Goblin", 5)
    BigOgre = Monster("Big Ogre", "Ogre", 120)
    GargantuanBadger = Monster("Massive Badger", "Animal", 1590)

    print(BigOgre)  # -> "Big Ogre of type Ogre, Power: 120."
    print(Zombie)  # -> "Undead Rat of type Zombie, Power: 10."

    Maailm.add_monster(GoblinSpear)

    print()
    print()
    print("Mängime esimese kakluse läbi!")

    Maailm.add_strongest("Druid")
    Maailm.add_strongest_monster()
    print(Maailm.get_active_adventurers())  # -> Peep
    print(Maailm.get_active_monsters())  # -> [Goblin Spearman of type Goblin, Power: 10.]

    Maailm.go_adventure(True)

    Maailm.add_strongest("Druid")
    print(Maailm.get_active_adventurers())  # -> [Peep, the Druid, Power: 45, Experience: 20.]
    print("Surnuaias peaks üks goblin olema.")
    print(Maailm.get_graveyard())  # ->[Goblin Spearman of type Goblin, Power: 10.]

    Maailm.add_monster(GargantuanBadger)
    Maailm.add_strongest_monster()

    Maailm.go_adventure(True)
    # Druid on loomade sõber, ja ajab massiivse mägra ära.
    print(Maailm.get_adventurerlist())  # -> Kõik 4 mängijat.
    print(Maailm.get_monsterlist())  # -> [Massive Badger of type Animal, Power: 1590.]

    Maailm.remove_character("Massive Badger")
    print(Maailm.get_monsterlist())  # -> []

    print(
        "Su sõber ütleb: \"Kui kõik need testid andsid sinu koodiga sama tulemuse mille ma siin ette kirjutasin, peaks"
        " kõik okei olema, proovi testerisse pushida! \" ")
