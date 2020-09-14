"""Pokemon game."""
import copy
import json
from os import path

import requests


class World:
    """World class."""

    def __init__(self, name, offset, limit):
        """
        Class constructor.

        :param name: name of the pokemon world
        :param offset: offset for api request
        :param limit: limit for api request
        Check if f"{name}_{offset}_{limit}.txt" file exists, if it does, read pokemons in from that file, if not,
        then make an api request to f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}" to get
        pokemons and dump them to f"{name}_{offset}_{limit}.txt" file
        """
        self.pokemons = []
        self.name = name
        self.offset = offset
        self.limit = limit
        file_name = f"{name}_{offset}_{limit}.txt"
        url = f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}"
        if path.exists(file_name):
            with open(file_name, "r") as f:
                for line in f:
                    p = Pokemon(line)
                    self.pokemons.append(p)
        else:
            result = requests.get(url).json()
            for pokemon_data in result['results']:
                pokemon_url = pokemon_data['url']
                p = Pokemon(pokemon_url)
                self.pokemons.append(p)
            self.dump_pokemons_to_file_as_json(f"{name}_{offset}_{limit}.txt")

    def dump_pokemons_to_file_as_json(self, name):
        """
        Dump the pokemons to file as json.

        :param name: name of the .txt file
        Write all self.pokemons separated by a newline to the given filename(if it doesnt exist, then create one)
        PS: Write the pokemon.__str__() version, not __repr__() as only name is useless :)
        """
        with open(name, "w") as f:
            for p in self.pokemons:
                f.write(json.dumps(p.data) + "\n")

    def fight(self):
        """
        A wild brawl between all pokemons where points are assigned to winners.

        Note, every pokemon fights another pokemon only once
        Fight lasts until one pokemon runs out of hp.
        every pokemon hits only 1 time per turn and they take turns when they attack.
        Call choose_which_pokemon_hits_first(pokemon1, pokemon2): to determine which pokemon hits first
        Call pokemon_duel function in this method with the aforementioned pokemons.
        every exception thrown by called sub methods must be caught and dealt with.
        """
        for poke1 in self.pokemons:
            for poke2 in self.pokemons[self.pokemons.index(poke1):len(self.pokemons)]:
                try:
                    pokemons = World.choose_which_pokemon_hits_first(poke1, poke2)
                    self.pokemon_duel(pokemons[0], pokemons[1])
                except PokemonFightResultsInATieException as e:
                    print(e)
                except SamePokemonFightException as e:
                    print(e)

    @staticmethod
    def pokemon_duel(pokemon1, pokemon2):
        """
        Pokemon duel.

        :param pokemon1: pokemon, who attacks first.
        :param pokemon2: pokemon, who attacks second.
        :return winner: pokemon, who won.

        Here 2 pokemons fight.
        To get the attack and defense of the pokemon, call pokemon1.get_pokemon_attack()
        and pokemon1.get_pokemon_defense() respectively.
        Attack is multiplied by the pokemon1.get_attack_multiplier(list(second.data['types'])) multiplier
        Total attack is
        pokemon1.get_pokemon_attack(turn_counter) * multiplier1 - second.get_pokemon_defense(turn_counter)
        [turn counter starts from 1]
        Total attack is subtracted from other pokemons hp.
        Pokemons can not heal during the fight. (when total attack is negative, no damage is dealt)
        If the fight between 2 pokemons lasts more than 100 turns, then PokemonFightResultsInATieException() is thrown.
        If one pokemon runs out of hp, fight ends and the winner gets 1 point, (self.score += 1)
        then both pokemons are healed to full hp.
        """
        start_hp_of_pokemon1 = pokemon1.data['hp']
        start_hp_of_pokemon2 = pokemon2.data['hp']
        for round_number in range(1, 101):
            pokemon2.data['hp'] -= World.get_damage(round_number, pokemon1, pokemon2)
            if pokemon2.data['hp'] <= 0:
                pokemon1.score += 1
                pokemon1.data['hp'] = start_hp_of_pokemon1
                pokemon2.data['hp'] = start_hp_of_pokemon2
                return pokemon1
            pokemon1.data['hp'] -= World.get_damage(round_number, pokemon2, pokemon1)
            if pokemon1.data['hp'] <= 0:
                pokemon2.score += 1
                pokemon2.data['hp'] = start_hp_of_pokemon2
                pokemon1.data['hp'] = start_hp_of_pokemon1
                return pokemon2
        raise PokemonFightResultsInATieException

    @staticmethod
    def get_damage(round_number, attacker, defender):
        """Get the damage dealt amount."""
        damage = attacker.get_pokemon_attack(round_number)
        defense = defender.get_pokemon_defense(round_number)
        damage *= attacker.get_attack_multiplier(list(defender.data['types']))
        damage_dealt = damage - defense
        if damage_dealt < 0:
            return 0
        return damage_dealt

    @staticmethod
    def choose_which_pokemon_hits_first(pokemon1, pokemon2):
        """
        Choose which pokemon hits first.

        :param pokemon1:
        :param pokemon2:
        Pokemon who's speed is higher, goes first. if both pokemons have the same speed, then pokemon who's weight
        is lower goes first, if both pokemons have same weight, then pokemon who's height is lower goes first,
        if both pokemons have the same height, then the pokemon with more abilities goes first, if they have the same
        amount of abilities, then the pokemon with more moves goes first, if the pokemons have the same amount of
        moves, then the pokemon with higher base_experience goes first, if the pokemons have the same
        base_experience then SamePokemonFightException() is thrown
        :return pokemon1 who goes first and pokemon2 who goes second (return pokemon1, pokemon2)
        """
        list_of_attributes = [pokemon1, pokemon2, pokemon1.data['speed'], pokemon2.data['speed'],
                              pokemon2, pokemon1, pokemon1.data['weight'], pokemon2.data['weight'],
                              pokemon2, pokemon1, pokemon1.data['height'], pokemon2.data['height'],
                              pokemon1, pokemon2, len(pokemon1.data['abilities']), len(pokemon2.data['abilities']),
                              pokemon1, pokemon2, len(pokemon1.data['moves']), len(pokemon2.data['moves']),
                              pokemon1, pokemon2, pokemon1.data['base_experience'], pokemon2.data['base_experience']
                              ]
        for i in range(2, len(list_of_attributes), 4):
            if list_of_attributes[i] == list_of_attributes[i + 1]:
                continue
            if list_of_attributes[i] > list_of_attributes[i + 1]:
                return list_of_attributes[i - 2], list_of_attributes[i - 1]
            else:
                return list_of_attributes[i - 1], list_of_attributes[i - 2]
        raise SamePokemonFightException()

    def get_leader_board(self):
        """
        Get Pokemons by given format in a list sorted by the pokemon.score.

        :return: List of leader board. where winners are first
        """
        pokemons_list = copy.deepcopy(self.pokemons)
        pokemon_list = sorted(pokemons_list, key=lambda x: x.data['name'])
        pokemon_list = sorted(pokemon_list, key=lambda x: x.score, reverse=True)
        return pokemon_list

    def get_pokemons_sorted_by_attribute(self, attribute: str):
        """
        Get Pokemons by given format in a list sorted by the pokemon.data[attribute].

        :param attribute:  pokemon data attribute to sort by
        :return: sorted List of pokemons
        """
        pokemons_list = copy.deepcopy(self.pokemons)
        pokemon_list = sorted(pokemons_list, key=lambda x: x.data[attribute])
        return pokemon_list


class Pokemon:
    """Class for Pokemon."""

    multipliers = None

    def __init__(self, url_or_path_name: str):
        """
        Class constructor.

        :param url_or_path_name: url or json object.
        If it is url, then parse information from request to proper
        json file and save it to self.data.
        If it is a string representation of a json object, then parse it into json object and save to self.data
        """
        self.score = 0
        self.data = {}
        if url_or_path_name.startswith("http"):
            self.parse_json_to_pokemon_information(url_or_path_name)
        else:
            self.data = json.loads(url_or_path_name)

    def parse_json_to_pokemon_information(self, url):
        """
        Parse json to info.

        :param url: url where the information is requested.
        Called from constructor and this method requests data from url to parse it into proper json object
        and then saved under self.data example done previously
        """
        result = requests.get(url).json()
        # Save the name, height and base_exp to the data dict.
        self.data['name'] = result['forms'][0]['name']
        self.data['height'] = result['height']
        self.data['base_experience'] = result['base_experience']
        self.data['weight'] = result['weight']
        # Save stats to data.
        for i in range(len(result['stats'])):
            self.data[result['stats'][i]['stat']['name']] = result['stats'][i]['base_stat']
        self.data['types'] = []
        self.data['abilities'] = []
        self.data['forms'] = []
        self.data['moves'] = []
        # Save Types
        for i in range(len(result['types'])):
            self.data['types'].append(result['types'][i]['type']['name'])
        # Save abilities
        for i in range(len(result['abilities'])):
            self.data['abilities'].append(result['abilities'][i]['ability']['name'])
        # Save Forms
        for i in range(len(result['forms'])):
            self.data['forms'].append(result['forms'][i]['name'])
        # Save Moves
        for i in range(len(result['moves'])):
            self.data['moves'].append(result['moves'][i]['move']['name'])

    def get_attack_multiplier(self, other: list):
        """
        self.pokemon is attacking, other is defending.

        :param other: list of other pokemon2.data['types']
        Calculate Pokemons attack multiplier against others types and take the best result.
        get the initial multiplier from Fighting Multiplier matrix.
        For example if self.type == ['fire'] and other == ['ground']: return fighting_multipliers['fire']['ground']
        if the defendant has dual types, then multiply the multipliers together.
        if the attacker has dual-types, then the best option is
        chosen(attack can only be of 1 type, choose better[higher multiplier])
        :return: Multiplier.
        """
        if Pokemon.multipliers is None:
            Pokemon.multipliers = []
            with open("multipliers", "r") as f:
                Pokemon.multipliers = [line.strip().split() for line in f]
        multipliers = []
        for type_num in range(len(self.data['types'])):
            x_index = Pokemon.multipliers[0].index(self.data['types'][type_num])
            y_index = Pokemon.multipliers[0].index(other[0])
            multiplier = float(Pokemon.multipliers[x_index][y_index - 1])
            multipliers.append(multiplier)
            if len(other) == 2:
                y_index = Pokemon.multipliers[0].index(other[1])
                multiplier = float(Pokemon.multipliers[x_index][y_index - 1])
                multipliers[type_num] = multipliers[type_num] * multiplier
        return max(multipliers)

    def get_pokemon_attack(self, turn_counter):
        """
        Get the pokemon attack.

        :param turn_counter: every third round the attack is empowered. (return self.data['special-attack'])
        otherwise basic attack is returned (self.data['attack'])
        """
        if turn_counter % 3 == 0:
            return self.data['special-attack']
        else:
            return self.data['attack']

    def get_pokemon_defense(self, turn_counter):
        """
        Get the pokemon defense.

        Note: whatever the result is returned, return half of it instead (for example return self.data['defense'] / 2)
        :param turn_counter: every second round the defense is empowered. (return self.data['special-defense'])
        otherwise basic defense is returned (self.data['defense'])
        """
        if turn_counter % 2 == 0:
            return self.data['special-defense'] / 2
        else:
            return self.data['defense'] / 2

    def __str__(self):
        """
        String representation of json(self.data) object.

        One way to accomplish this is to use json.dumps functionality
        :return: string version of json file with necessary information
        """
        return json.dumps(self.data)

    def __repr__(self):
        """
        Object representation.

        :return: Pokemon's name in string format and his score, for example: "garchomp-mega 892"
        """
        return str(self.data['name']) + " " + str(self.score)


class SamePokemonFightException(Exception):
    """Custom exception thrown when same pokemons are fighting."""

    pass


class PokemonFightResultsInATieException(Exception):
    """Custom exception thrown when the fight lasts longer than 100 rounds."""

    pass


if __name__ == '__main__':
    world = World("PokeLand", 15, 4)
    world.fight()
    print(world.get_leader_board())
