from models.deck import Deck

class User:
    def __init__(self, userID, name):
        self.userID = userID
        self.name = name
        self.decks = [Deck(f"File {i+1} - (Placeholder)") for i in range(3)]
    
    def viewStats(self):
        print(f"\nUser: {self.name} (ID: {self.userID})")
        for i, deck in enumerate(self.decks):
            print(f"  Deck {i+1}: {deck.deckName} - {len(deck.cards)} cards")
    
    def createDeck(self, index, name):
        if 0 <= index < 3:
            self.decks[index].deckName = name
    
    def selectDeck(self, index):
        if 0 <= index < 3:
            return self.decks[index]
        return None
    
    def to_dict(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "decks": [deck.to_dict() for deck in self.decks]
        }
    
    @staticmethod
    def from_dict(data):
        user = User(data["userID"], data["name"])
        user.decks = [Deck.from_dict(deck_data) for deck_data in data["decks"]]
        return user
