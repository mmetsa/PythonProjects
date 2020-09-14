"""Blackjack."""
import importlib
import os
import pkgutil
from deck import Deck, Card
from game_view import GameView, FancyView, Move
from strategy import Strategy, HumanStrategy, MirrorDealerStrategy


class Hand:
    """A Class that represents a Hand."""

    def __init__(self, cards: list = None):
        """
        Initialise a Hand.

        :param cards: List of cards, None by default.
        By default there are no cards in the hand, but they can be given.
        """
        if cards is not None:
            self.cards = cards
        else:
            self.cards = []
        self.is_double_down = False
        self.is_surrendered = False
        self.is_soft = False
        self.state = ""
        self.is_split_hand = False

    def add_card(self, card: Card) -> None:
        """Add a Card to the Hand.

        Check if card actually is a card before appending.
        :param card: The card to add.
        """
        if isinstance(card, Card):
            self.cards.append(card)

    def double_down(self, card: Card) -> None:
        """Add the card to hand and set Double Down to True.

        Again, check if the card is actually a Card.
        :param card: The card to add.
        """
        if isinstance(card, Card):
            self.cards.append(card)
            self.is_double_down = True

    def split(self):
        """
        Split a Hand if it is possible.

        A Hand is possible to split if the value of the 2 cards in the Hand is the same.
        :return: New hand with one of the cards in it.
        """
        if self.can_split:
            new_card = self.cards[0]
            self.cards.remove(self.cards[0])
            return Hand([new_card])
        else:
            raise ValueError("Invalid hand to split!")

    @property
    def can_split(self) -> bool:
        """
        Check if hand can be split.

        A hand can be split if there's only 2 cards and they are of the same value.
        :return: could split or not
        """
        if len(self.cards) == 2 and self.cards[0].get_card_value == self.cards[1].get_card_value:
            return True
        else:
            return False

    @property
    def is_blackjack(self) -> bool:
        """
        Check if is blackjack.

        Blackjack is when you get a score of 21 with 2 cards. (Ace and a value 10 card).
        :return: is blackjack or not.
        """
        if self.score == 21 and len(self.cards) == 2:
            return True
        else:
            return False

    @property
    def is_soft_hand(self):
        """Check if is soft hand."""
        if self.is_soft:
            return True
        return False

    @property
    def score(self) -> int:
        """
        Get a score of hand.

        :return: total_score
        """
        aces = [
            Card("ACE", "SPADES", "AS"),
            Card("ACE", "HEARTS", "AH"),
            Card("ACE", "CLUBS", "AC"),
            Card("ACE", "DIAMONDS", "AD")
        ]
        total_score = 0
        # Go through all cards that are not aces, add them together.
        for card in self.cards:
            if card not in aces:
                total_score += card.get_card_value
        # Go through all aces, and if the ace value makes the total over 21, the value is 1.
        for card in self.cards:
            if card in aces:
                if total_score + 11 > 21:
                    total_score += 1
                else:
                    # There is an ace that has a value of 11 because it didn't make the total go over 21.
                    self.is_soft = True
                    total_score += 11
        return total_score


class Player:
    """Player."""

    def __init__(self, name: str, strategy: Strategy, coins: int = 100):
        """Initialise a Player."""
        self.name = name
        self.strategy = strategy
        self.coins = coins
        self.hands = []
        strategy.player = self

    def join_table(self):
        """
        Join a table.

        Possible if a Player has enough coins.
        When a Player joins, he is dealt a new Hand.
        """
        if self.coins > GameController.BUY_IN_COST:
            self.coins -= GameController.BUY_IN_COST
            self.hands.append(Hand())

    def play_move(self, hand: Hand) -> Move:
        """
        Play a move.

        Use the strategy that the Player is assigned.
        :return: Move
        """
        return self.strategy.play_move(hand)

    def split_hand(self, hand: Hand) -> None:
        """
        Split a hand.

        Check if the Player has enough coins to split the hand before splitting.
        """
        if self.coins >= GameController.BUY_IN_COST and hand.can_split:
            self.coins -= GameController.BUY_IN_COST
            new_hand = hand.split()
            new_hand.is_split_hand = True
            self.hands.append(new_hand)


class GameController:
    """Game controller."""

    PLAYER_START_COINS = 200
    BUY_IN_COST = 10

    def __init__(self, view: GameView):
        """Init."""
        self.view = view
        self.house = Hand()
        self.players = []
        self.deck = None
        self.decks_count = 0
        self.playing_players = []

    def start_game(self) -> None:
        """Start game."""
        self.decks_count = self.view.ask_decks_count()
        players_count = self.view.ask_players_count()
        bots_count = self.view.ask_bots_count()
        self.deck = Deck(self.decks_count, True)
        for _i in range(players_count):
            name = self.view.ask_name(_i)
            self.players.append(Player(name, HumanStrategy(self.players, self.house, self.decks_count, self.view),
                                       GameController.PLAYER_START_COINS))
        for _i in range(bots_count):
            self.players.append(Player("Bot", MirrorDealerStrategy(self.players, self.house, self.decks_count),
                                       GameController.PLAYER_START_COINS))

    def start_round(self):
        """
        Start the round.

        House gets a new hand. Then players get new hands.
        All players who can play, get their money reduced and are moved to the playing players list.
        All players get a card, House gets a card, 2x (House's first card is top-down)
        Show the view to the player at the start of the round.
        """
        self.house = Hand()
        self.playing_players = []
        for player in self.players:
            player.hands = []
        for player in self.players:
            if player.coins >= GameController.BUY_IN_COST:
                self.playing_players.append(player)
            player.join_table()
        for player in self.playing_players:
            player.hands[0].add_card(self.deck.draw_card())
        self.house.add_card(self.deck.draw_card(True))
        for player in self.playing_players:
            player.hands[0].add_card(self.deck.draw_card())
        self.house.add_card(self.deck.draw_card())
        # Send the view to the player.
        self.view.show_table(self.playing_players, self.house, player)

    def double_down(self, player, hand):
        """
        Double down check.

        If a Player does Double Down and the new card makes the score go over 21, he's Busted not Double_downed.
        If there's not enough coins, you can't double down.
        """
        if player.coins > GameController.BUY_IN_COST:
            player.coins -= GameController.BUY_IN_COST
            card = self._draw_card()
            hand.add_card(card)
            if hand.score > 21:
                hand.state = "BUSTED"
            else:
                hand.is_double_down = True
                hand.state = "DOUBLE_DOWN"
        else:
            print("Can't Double Down!")

    def moves_loop(self, player, hand):
        """
        The loop of all the moves.

        Restart is how I made it so after splitting, it doesn't take second hand that was split, but the first.
        So if restarts, it still asks a move for the same hand, not the next one.
        """
        restart = True
        while restart:
            if hand.is_split_hand:
                hand.add_card(self._draw_card())
                self.view.show_table(self.playing_players, self.house, player)
            move = player.play_move(hand)
            while move == Move.HIT:
                card = self._draw_card()
                hand.add_card(card)
                if hand.score > 21:
                    hand.state = "BUSTED"
                    self.view.show_table(self.playing_players, self.house, player)
                    restart = False
                    break
                else:
                    self.view.show_table(self.playing_players, self.house, player)
                    move = player.play_move(hand)
                    restart = False
            if move == Move.STAND:
                restart = False
            elif move == Move.SPLIT:
                if hand.can_split:
                    player.split_hand(hand)
                    hand.add_card(self._draw_card())
                self.view.show_table(self.playing_players, self.house, player)
            elif move == Move.DOUBLE_DOWN:
                self.double_down(player, hand)
                restart = False
            elif move == Move.SURRENDER:
                hand.is_surrendered = True
                self.view.show_table(self.playing_players, self.house, player)
                restart = False
        self.view.show_table(self.playing_players, self.house, player)

    def do_house_moves(self, player):
        """Do house moves."""
        while not self.house.is_soft_hand and self.house.score < 17:
            card = self._draw_card()
            self.house.add_card(card)
            self.view.show_table(self.playing_players, self.house, player)
        while self.house.is_soft_hand and self.house.score < 18:
            card = self._draw_card()
            self.house.add_card(card)
            self.view.show_table(self.playing_players, self.house, player)

    def end_round_money(self, player, hand):
        """Give back the money to those who won."""
        if hand.state == "BUSTED":
            return
        if hand.is_surrendered:
            player.coins = round(player.coins + GameController.BUY_IN_COST / 2)
            print(player.coins)
            return
        if hand.is_blackjack:
            player.coins += GameController.BUY_IN_COST
            player.coins += GameController.BUY_IN_COST * 1.5
            print(player.coins)
            return
        if hand.is_double_down:
            if hand.score > self.house.score or self.house.score > 21:
                player.coins += GameController.BUY_IN_COST * 4
            elif hand.score == self.house.score:
                player.coins += GameController.BUY_IN_COST * 2
        elif hand.score > self.house.score or self.house.score > 21:
            player.coins += GameController.BUY_IN_COST * 2
        elif hand.score == self.house.score:
            player.coins += GameController.BUY_IN_COST

    def play_round(self) -> bool:
        """Play round."""
        self.start_round()
        for player in self.playing_players:
            for hand in player.hands:
                self.moves_loop(player, hand)
        self.house.cards[0].top_down = False
        self.do_house_moves(player)
        for player in self.playing_players:
            for hand in player.hands:
                self.end_round_money(player, hand)

    def _draw_card(self, top_down: bool = False) -> Card:
        """Draw card."""
        return self.deck.draw_card(top_down)

    @staticmethod
    def load_strategies() -> list:
        """
        Load strategies.

        @:return list of strategies that are in same package.
        DO NOT EDIT!
        """
        pkg_dir = os.path.dirname(__file__)
        for (module_loader, name, is_pkg) in pkgutil.iter_modules([pkg_dir]):
            importlib.import_module(name)
        return list(filter(lambda x: x.__name__ != HumanStrategy.__name__, Strategy.__subclasses__()))


if __name__ == '__main__':

    game_controller = GameController(FancyView())
    game_controller.start_game()
    while game_controller.play_round():
        pass
