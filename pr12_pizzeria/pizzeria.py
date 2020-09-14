"""Pizzeria."""
import math


class Chef:
    """Represent a Chef."""

    def __init__(self, name: str, experience_level: int):
        """Initialise."""
        self.name = name
        self.experience_level = experience_level
        self.money = 0

    def __repr__(self):
        """Print the chef."""
        return "Pizza chef " + str.capitalize(self.name) + " with " + str(self.experience_level) + " XP"


class Pizza:
    """Represent a Pizza."""

    def __init__(self, name: str, diameter: int, toppings: list):
        """Initialise."""
        self.name = name
        self.diameter = diameter
        self.toppings = toppings

    def calculate_complexity(self) -> int:
        """Calculate the pizza's complexity."""
        total_complexity = 0
        for elem in self.toppings:
            total_complexity += len(elem) // 3
        return total_complexity

    def calculate_price(self) -> int:
        """Calculate the price of a pizza."""
        pizza_area = math.pi * (self.diameter / 2) ** 2
        part_1 = pizza_area / 40
        part_2 = len(self.toppings) // 2
        price = math.floor((part_1 + part_2) * 100)
        return price

    def __repr__(self):
        """Print the pizza."""
        return str.capitalize(self.name) + " pizza with a price of " + str(self.calculate_price() / 100)


class Pizzeria:
    """Represent a pizzeria."""

    def __init__(self, name: str, is_fancy: bool, budget: int):
        """Initialise."""
        self.name = name
        self.is_fancy = is_fancy
        self.budget = budget
        self.chefs = []
        self.recipes = []
        self.baked_pizzas = {}

    def __repr__(self):
        """Print the pizzeria."""
        return str.capitalize(self.name) + " with " + str(len(self.chefs)) + " pizza chef(s)."

    def add_chef(self, chef: Chef) -> Chef or None:
        """Add a chef to a pizzeria.

        :param chef: The chef to add.
        """
        if chef not in self.get_chefs():
            if self.is_fancy:
                if chef.experience_level >= 25:
                    self.chefs.append(chef)
                    return chef
                else:
                    return None
            else:
                self.chefs.append(chef)
                return chef
        else:
            return None

    def remove_chef(self, chef: Chef):
        """Remove a chef from the pizzeria.

        :param chef: the chef to remove.
        """
        if chef in self.chefs:
            self.chefs.remove(chef)
        return

    def add_pizza_to_menu(self, pizza: Pizza):
        """Add a pizza recipe to the menu.

        :param pizza: the recipe to add.
        """
        if self.budget - pizza.calculate_price() >= 0:
            if pizza not in self.recipes:
                if len(self.get_chefs()) != 0:
                    self.budget -= pizza.calculate_price()
                    self.recipes.append(pizza)
        return

    def remove_pizza_from_menu(self, pizza: Pizza):
        """Remove a recipe from the menu.

        :param pizza: Pizza to remove.
        """
        if pizza in self.recipes:
            self.recipes.remove(pizza)
        return

    def bake_pizza(self, pizza: Pizza) -> Pizza or None:
        """Bake a pizza.

        :param pizza: Pizza to make.
        """
        best_chef_exp = float('inf')
        best_chef = None
        if pizza in self.recipes:
            for chef in self.get_chefs():
                if pizza.calculate_complexity() <= chef.experience_level < best_chef_exp:
                    best_chef_exp = chef.experience_level
                    best_chef = chef
                else:
                    continue
            if best_chef is not None:
                best_chef.experience_level += len(pizza.name) // 2
                profit = pizza.calculate_price() * 4 + len(pizza.name)
                if profit % 2 == 0:
                    best_chef.money += profit / 2
                    self.budget += profit / 2
                else:
                    profit = profit - 1
                    best_chef.money += profit / 2
                    self.budget += profit / 2
                if pizza in self.baked_pizzas:
                    self.baked_pizzas[pizza] += 1
                else:
                    self.baked_pizzas[pizza] = 1
                return pizza
        return None

    def get_pizza_menu(self) -> list:
        """Get the pizza recipes."""
        pizza_recipes = sorted(self.recipes, key=lambda x: x.calculate_price(), reverse=True)
        return pizza_recipes

    def get_baked_pizzas(self) -> dict:
        """Get the baked pizzas dict."""
        return self.baked_pizzas

    def get_chefs(self) -> list:
        """Get the chefs of the pizzeria."""
        chefs = sorted(self.chefs, key=lambda x: x.experience_level)
        return chefs


if __name__ == '__main__':

    pizzeria2 = Pizzeria("Maranello", False, 10000)

    fernando = Chef("Fernando", 9)
    felipe = Chef("Felipe", 6)
    michael = Chef("Michael", 17)
    rubens = Chef("Rubens", 4)
    eddie = Chef("Eddie", 5)

    pizzeria2.add_chef(fernando)
    pizzeria2.add_chef(felipe)
    pizzeria2.add_chef(michael)
    pizzeria2.add_chef(rubens)
    pizzeria2.add_chef(eddie)

    margherita = Pizza("Margherita", 20, ["Sauce", "Mozzarella", "Basil"])
    smoke = Pizza("Big Smoke", 30, ["nine", "NINE", "six w/dip", "seven", "45", "45 w/cheese", "SODA"])

    pizzeria2.add_pizza_to_menu(margherita)
    pizzeria2.add_pizza_to_menu(smoke)

    print(pizzeria2.get_pizza_menu())  # [Big smoke pizza with a price of 20.67, Margherita pizza with a price of 8.85]
    print(pizzeria2.get_chefs())
    # [Pizza chef Rubens with 4 XP, Pizza chef Eddie with 5 XP, Pizza chef Felipe with 6 XP, Pizza chef Fernando with
    # 9 XP, Pizza chef Michael with 17 XP]

    pizzeria2.bake_pizza(margherita)
    print(pizzeria2.get_chefs())
    # [Pizza chef Rubens with 4 XP, Pizza chef Felipe with 6 XP, Pizza chef Fernando with 9 XP, Pizza chef Eddie with
    # 10 XP, Pizza chef Michael with 17 XP]

    pizzeria2.bake_pizza(smoke)
    print(pizzeria2.get_chefs())
    # [Pizza chef Rubens with 4 XP, Pizza chef Felipe with 6 XP, Pizza chef Fernando with 9 XP, Pizza chef Eddie with
    # 14 XP, Pizza chef Michael with 17 XP]
