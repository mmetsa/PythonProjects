"""Deck."""

import random
from typing import Optional, List
import requests


class Card:
    """Simple dataclass for holding card information."""

    def __init__(self, value: str, suit: str, code: str):
        """Constructor."""
        self.value = value
        self.suit = suit
        self.code = code
        self.top_down = False

    @property
    def get_card_value(self):
        """Get the value of the card."""
        card_values = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "JACK": 10,
            "QUEEN": 10,
            "KING": 10,
            "ACE": [1, 11]
        }
        val = card_values[self.value]
        return val

    def __str__(self):
        """Str."""
        if not self.top_down:
            return self.code
        else:
            return "??"

    def __repr__(self) -> str:
        """Repr."""
        return self.code

    def __eq__(self, o) -> bool:
        """Eq."""
        if isinstance(o, Card):
            if o.suit == self.suit and o.value == self.value:
                return True
        return False


class Deck:
    """Deck."""

    DECK_BASE_API = "https://deckofcardsapi.com/api/deck/"

    def __init__(self, deck_count: int = 1, shuffle: bool = False):
        """Constructor."""
        self._backup_deck = []
        self.remaining = 52 * deck_count
        self.deck_count = deck_count
        self.is_shuffled = shuffle
        self.deck = self._request(Deck.DECK_BASE_API + "new/?deck_count=" + str(self.deck_count))
        self.deck_id = self.deck.get('deck_id', None)
        for num in range(self.deck_count):
            for elem in self._generate_backup_pile():
                self._backup_deck.append(elem)
        if self.is_shuffled:
            self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the deck."""
        if self.deck_id is None:
            random.shuffle(self._backup_deck)
            return
        try:
            response = requests.get(Deck.DECK_BASE_API + self.deck_id + "/shuffle/")
        except requests.exceptions.ConnectionError as e:
            return e
        if response.status_code == requests.codes.ok and response is not None:
            result = response.json()
            self.deck = result
        random.shuffle(self._backup_deck)

    def draw_card(self, top_down: bool = False) -> Optional[Card]:
        """
        Draw card from the deck.

        :return: card instance.
        """
        result = None
        if self.deck_id:
            response = requests.get(Deck.DECK_BASE_API + self.deck_id + "/draw/?count=1")
            result = response.json()
        if self.remaining == 0:
            return None
        if result is not None and result.get('success', False) is True:
            card = result['cards'][0]
            new_card: Card = Card(card['value'], card['suit'], card['code'])
            if top_down:
                new_card.top_down = True
            if new_card in self._backup_deck:
                self._backup_deck.remove(new_card)
            self.remaining -= 1
            return new_card
        else:
            if self._backup_deck:
                new_card = random.choice(self._backup_deck)
                if top_down:
                    new_card.top_down = True
                self._backup_deck.remove(new_card)
                self.remaining -= 1
                return new_card

    def _request(self, url: str) -> dict:
        """Update deck."""
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return {}
        if response.status_code == requests.codes.ok and response is not None:
            result = response.json()
        else:
            return {}
        return result

    @staticmethod
    def _generate_backup_pile() -> List[Card]:
        """Generate backup pile."""
        suit_dict = {"S": "SPADES", "D": "DIAMONDS", "C": "CLUBS", "H": "HEARTS"}
        list_of_cards = []
        for char in "SDCH":
            if char in suit_dict:
                suit = suit_dict[char]
            list_of_cards.append(Card("ACE", suit, "A" + char))
            for num in range(2, 11):
                list_of_cards.append(Card(str(num), suit, str(num) + char))
            for o_char in "JQK":
                if o_char == "J":
                    value = "JACK"
                elif o_char == "Q":
                    value = "QUEEN"
                elif o_char == "K":
                    value = "KING"
                list_of_cards.append(Card(value, suit, o_char + char))
        return list_of_cards


if __name__ == '__main__':
    d = Deck(shuffle=True)
    print(d.remaining)  # 52
    card1 = d.draw_card()  # Random card
    print(card1)
    print(card1 in d._backup_deck)  # False
    print(d._backup_deck)  # 51 shuffled cards
    d2 = Deck(deck_count=2)
    print(d2._backup_deck)  # 104 ordered cards (deck after deck)
