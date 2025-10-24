import os
from sessions.base_session import StudySession

class ReviewMode(StudySession):
    def __init__(self, deck, shuffled=False):
        super().__init__(deck)
        self.shuffled = shuffled
        self.current_cards = deck.shuffleDeck() if shuffled else deck.cards.copy()
    
    def start(self):
        if not self.current_cards:
            print("No cards in this deck!")
            input("Press Enter to continue...")
            return
        
        idx = 0
        showing_question = True
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            shuffle_status = "[S]" if self.shuffled else "[NS]"
            face = "[Q]" if showing_question else "[A]"
            card = self.current_cards[idx]
            
            # Header with proper spacing
            counter = f"[{idx+1}/{len(self.current_cards)}]"
            print(f"{counter} {shuffle_status}".ljust(45) + face)
            print("="*50)
            print()
            
            # Center the content
            content = card.showQuestion() if showing_question else card.showAnswer()
            lines = content.split('\n')
            for line in lines:
                print(line.center(50))
            
            print()
            print("="*50)
            print("1. Back".ljust(25) + "2. Proceed")
            print("3. Flip".ljust(25) + "4. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "1":  # Back
                if idx > 0:
                    idx -= 1
                    showing_question = True
            elif choice == "2":  # Proceed
                if idx < len(self.current_cards) - 1:
                    idx += 1
                    showing_question = True
                else:
                    print("\nYou've reached the end of the deck!")
                    input("Press Enter to continue...")
            elif choice == "3":  # Flip
                showing_question = not showing_question
            elif choice == "4":  # Exit
                break