import random
from models.flashcard import FlashCard

class Deck:
    def __init__(self, deckName="Placeholder"):
        self.deckName = deckName
        self.cards = []
    
    def addCards(self, card):
        self.cards.append(card)
    
    def removeCards(self, index):
        if 0 <= index < len(self.cards):
            self.cards.pop(index)
    
    def shuffleDeck(self):
        random.shuffle(self.cards)
        return self.cards.copy()
    
    def to_dict(self):
        return {
            "deckName": self.deckName,
            "cards": [card.to_dict() for card in self.cards]
        }
    
    @staticmethod
    def from_dict(data):
        deck = Deck(data["deckName"])
        deck.cards = [FlashCard.from_dict(card_data) for card_data in data["cards"]]
        return deck