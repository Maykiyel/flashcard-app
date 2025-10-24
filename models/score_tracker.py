class ScoreTracker:
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
    
    def updateScore(self, is_correct):
        if is_correct:
            self.correct += 1
        else:
            self.incorrect += 1
    
    def showStats(self):
        total = self.correct + self.incorrect
        if total == 0:
            return "No questions attempted yet."
        return f"Correct: {self.correct} | Incorrect: {self.incorrect} | Total: {total}"
