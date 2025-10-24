import os
from sessions.base_session import StudySession
from models.score_tracker import ScoreTracker

class QuizMode(StudySession):
    def __init__(self, deck, shuffled=False):
        super().__init__(deck)
        self.indexWrongs = []
        self.shuffled = shuffled
        self.current_cards = deck.shuffleDeck() if shuffled else deck.cards.copy()
    
    def markCorrect(self):
        self.score.updateScore(True)
        self.questionsAttempted += 1
    
    def markWrong(self, index):
        self.score.updateScore(False)
        self.questionsAttempted += 1
        self.indexWrongs.append(index)
    
    def recurWrongs(self):
        if not self.indexWrongs:
            return []
        wrong_cards = [self.current_cards[i] for i in self.indexWrongs]
        self.indexWrongs = []
        return wrong_cards
    
    def start(self):
        if not self.current_cards:
            print("No cards in this deck!")
            input("Press Enter to continue...")
            return
        
        self._run_quiz(self.current_cards)
        
        while self.indexWrongs:
            wrong_count = len(self.indexWrongs)
            print(f"\nYou have {wrong_count} wrong answer(s), do you wish to redeem yourself? (Y/N): ", end="")
            choice = input().strip().upper()
            
            if choice == 'Y':
                wrong_cards = self.recurWrongs()
                self._run_quiz(wrong_cards)
            else:
                break
        
        if not self.indexWrongs:
            print("\n" + "="*50)
            print("Congrats! No more wrong answers.")
            print("How do you wish to proceed?:")
            print("1. Retry")
            print("2. Back to Save Menu")
            print("="*50)
            choice = input("Choice: ").strip()
            
            if choice == "1":
                self.score = ScoreTracker()
                self.questionsAttempted = 0
                self.indexWrongs = []
                self.current_cards = self.deck.shuffleDeck() if self.shuffled else self.deck.cards.copy()
                self.start()
    
    def _run_quiz(self, cards):
        for idx, card in enumerate(cards):
            showing_question = True
            
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                shuffle_status = "[S]" if self.shuffled else "[NS]"
                face = "[Q]" if showing_question else "[A]"
                
                # Header with proper spacing
                counter = f"[{idx+1}/{len(cards)}]"
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
                print("1. Flip")
                print("2. Correct")
                print("3. Incorrect")
                
                choice = input("\nChoice: ").strip()
                
                if choice == "1":
                    showing_question = not showing_question
                elif choice == "2":
                    self.markCorrect()
                    break
                elif choice == "3":
                    self.markWrong(idx)
                    break
