from abc import ABC, abstractmethod
from models.score_tracker import ScoreTracker

class StudySession(ABC):
    def __init__(self, deck):
        self.deck = deck
        self.score = ScoreTracker()
        self.questionsAttempted = 0
    
    @abstractmethod
    def start(self):
        pass
    
    def end(self):
        print("\n" + "="*50)
        print("SESSION ENDED")
        print(self.score.showStats())
        print("="*50)
