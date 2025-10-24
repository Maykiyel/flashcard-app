import os
import time
from sessions.base_session import StudySession

class TimedMode(StudySession):
    def __init__(self, deck, timePerCard, shuffled=False):
        super().__init__(deck)
        self.timePerCard = timePerCard
        self.shuffled = shuffled
        self.current_cards = deck.shuffleDeck() if shuffled else deck.cards.copy()
    
    def start(self):
        if not self.current_cards:
            print("No cards in this deck!")
            input("Press Enter to continue...")
            return
        
        self._run_timed()
        
        print("\n" + "="*50)
        print("Finished mode! How do you wish to proceed?:")
        print("1. Retry")
        print("2. Exit")
        print("="*50)
        choice = input("Choice: ").strip()
        
        if choice == "1":
            self.current_cards = self.deck.shuffleDeck() if self.shuffled else self.deck.cards.copy()
            self.start()
    
    def _run_timed(self):
        for idx, card in enumerate(self.current_cards):
            showing_question = True
            time_left = self.timePerCard
            
            while time_left > 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                shuffle_status = "[S]" if self.shuffled else "[NS]"
                face = "[Q]" if showing_question else "[A]"
                
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
                print(f"[{time_left}]".center(50))
                
                time.sleep(1)
                time_left -= 1
            
            # Time's up - show options
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                shuffle_status = "[S]" if self.shuffled else "[NS]"
                face = "[Q]" if showing_question else "[A]"
                
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
                print("1. Proceed")
                print("2. Flip")
                print("3. Exit")
                
                choice = input("\nChoice: ").strip()
                
                if choice == "1":
                    break
                elif choice == "2":
                    showing_question = not showing_question
                elif choice == "3":
                    return