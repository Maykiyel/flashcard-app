import os
from storage.user_repository import UserRepository
from models.user import User
from models.flashcard import FlashCard
from sessions.quiz_mode import QuizMode
from sessions.timed_mode import TimedMode
from sessions.review_mode import ReviewMode

class AppController:
    def __init__(self):
        self.userRepo = UserRepository()
        self.current_user = None
    
    def run(self):
        while True:
            self.homepage()
    
    def homepage(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*50)
        print("           FLASHCARD APP - HOMEPAGE")
        print("="*50)
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("="*50)
        
        choice = input("Choice: ").strip()
        
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            print("Thank you for using FlashCard App!")
            exit()
    
    def login(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*50)
        print("                    LOGIN")
        print("="*50)
        name = input("Enter Username: ").strip()
        
        # Find user by name
        user = None
        for uid, u in self.userRepo.users.items():
            if u.name.lower() == name.lower():
                user = u
                break
        
        if user:
            self.current_user = user
            print(f"\nWelcome back, {user.name}!")
            input("Press Enter to continue...")
            self.deck_selection_menu()
        else:
            print("\nUser not found!")
            input("Press Enter to continue...")
    
    def register(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*50)
        print("                  REGISTER")
        print("="*50)
        name = input("Enter Username: ").strip()
        
        # Check if username already exists
        for uid, u in self.userRepo.users.items():
            if u.name.lower() == name.lower():
                print("\nUsername already exists!")
                input("Press Enter to continue...")
                return
        
        # Generate a unique userID
        userID = str(len(self.userRepo.users) + 1).zfill(4)
        while self.userRepo.user_exists(userID):
            userID = str(int(userID) + 1).zfill(4)
        
        user = User(userID, name)
        self.userRepo.add_user(user)
        
        print(f"\nUser {name} registered successfully!")
        print(f"Your UserID is: {userID}")
        input("Press Enter to continue...")
    
    def deck_selection_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*50)
            print("                 CHOOSE DECK")
            print("="*50)
            
            for i, deck in enumerate(self.current_user.decks):
                print(f"   {i+1}. {deck.deckName} - {len(deck.cards)} cards")
            
            print("="*50)
            print("1. Rename a file")
            print("2. Edit Deck")
            print("3. Play With Deck")
            print("4. Logout")
            print("="*50)
            
            choice = input("Choice: ").strip()
            
            if choice == "1":
                self.rename_deck()
            elif choice == "2":
                self.edit_deck()
            elif choice == "3":
                self.play_deck()
            elif choice == "4":
                self.userRepo.save()
                self.current_user = None
                print("\nLogged out successfully!")
                input("Press Enter to continue...")
                break
    
    def rename_deck(self):
        deck_num = input("\nWhich deck to rename (1-3)? ").strip()
        try:
            deck_idx = int(deck_num) - 1
            if 0 <= deck_idx < 3:
                new_name = input("Enter new name: ").strip()
                self.current_user.createDeck(deck_idx, f"File {deck_idx+1} - {new_name}")
                self.userRepo.save()
                print("\nDeck renamed successfully!")
            else:
                print("\nInvalid deck number!")
        except ValueError:
            print("\nInvalid input!")
        
        input("Press Enter to continue...")
    
    def edit_deck(self):
        deck_num = input("\nWhich deck to edit (1-3)? ").strip()
        try:
            deck_idx = int(deck_num) - 1
            if 0 <= deck_idx < 3:
                deck = self.current_user.selectDeck(deck_idx)
                self.edit_deck_interface(deck)
            else:
                print("\nInvalid deck number!")
                input("Press Enter to continue...")
        except ValueError:
            print("\nInvalid input!")
            input("Press Enter to continue...")
    
    def edit_deck_interface(self, deck):
        if not deck.cards:
            deck.addCards(FlashCard())
        
        current_idx = 0
        showing_question = True
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            face = "[Q]" if showing_question else "[A]"
            card = deck.cards[current_idx]
            
            # Header with proper spacing
            counter = f"[{current_idx+1}/{len(deck.cards)}]"
            print(f"{counter}".ljust(45) + face)
            print("="*50)
            print()
            
            # Center the content
            content = card.showQuestion() if showing_question else card.showAnswer()
            lines = content.split('\n')
            for line in lines:
                print(line.center(50))
            
            print()
            print("="*50)
            print("1. Exit".ljust(25) + "2. Save")
            print("3. + card".ljust(25) + "4. - card")
            print("5. Edit".ljust(25) + "6. Flip")
            print("7. Prev".ljust(25) + "8. Next")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "1":  # Exit
                self.userRepo.save()
                break
            elif choice == "2":  # Save
                self.userRepo.save()
                print("\nDeck saved!")
                input("Press Enter to continue...")
            elif choice == "3":  # + card
                new_card = FlashCard()
                deck.addCards(new_card)
                current_idx = len(deck.cards) - 1
                showing_question = True
                print("\nNew card added!")
                input("Press Enter to continue...")
            elif choice == "4":  # - card
                if len(deck.cards) > 1:
                    deck.removeCards(current_idx)
                    if current_idx >= len(deck.cards):
                        current_idx = len(deck.cards) - 1
                    showing_question = True
                    print("\nCard deleted!")
                else:
                    print("\nCannot delete the last card!")
                input("Press Enter to continue...")
            elif choice == "5":  # Edit
                new_content = input(f"\nEnter new {'question' if showing_question else 'answer'}: ").strip()
                if showing_question:
                    card.question = new_content
                else:
                    card.answer = new_content
                print("\nCard updated!")
                input("Press Enter to continue...")
            elif choice == "6":  # Flip
                showing_question = not showing_question
            elif choice == "7":  # Prev
                if current_idx > 0:
                    current_idx -= 1
                    showing_question = True
            elif choice == "8":  # Next
                if current_idx < len(deck.cards) - 1:
                    current_idx += 1
                    showing_question = True
    
    def play_deck(self):
        deck_num = input("\nWhich deck to play (1-3)? ").strip()
        try:
            deck_idx = int(deck_num) - 1
            if 0 <= deck_idx < 3:
                deck = self.current_user.selectDeck(deck_idx)
                if not deck.cards:
                    print("\nThis deck is empty! Add cards first.")
                    input("Press Enter to continue...")
                    return
                self.chooseMode(deck)
            else:
                print("\nInvalid deck number!")
                input("Press Enter to continue...")
        except ValueError:
            print("\nInvalid input!")
            input("Press Enter to continue...")
    
    def chooseMode(self, deck):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*50)
        print("              CHOOSE GAMEMODE")
        print("="*50)
        print("1. Quiz Mode")
        print("2. Timed Mode")
        print("3. Review Mode")
        print("="*50)
        
        mode_choice = input("Choice: ").strip()
        
        # Ask shuffle
        shuffle_input = input("\nShuffle cards (Y/N): ").strip().upper()
        shuffled = shuffle_input == 'Y'
        
        # Ask start
        start_input = input("Start Session (Y/N): ").strip().upper()
        if start_input != 'Y':
            return
        
        self.startSession(deck, mode_choice, shuffled)
    
    def startSession(self, deck, mode, shuffled):
        if mode == "1":
            session = QuizMode(deck, shuffled)
            session.start()
        elif mode == "2":
            try:
                time_per_card = int(input("\nHow many seconds per card?: ").strip())
                session = TimedMode(deck, time_per_card, shuffled)
                session.start()
            except ValueError:
                print("\nInvalid time input!")
                input("Press Enter to continue...")
        elif mode == "3":
            session = ReviewMode(deck, shuffled)
            session.start()
