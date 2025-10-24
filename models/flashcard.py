class FlashCard:
    def __init__(self, question="(Placeholder)", answer="(Placeholder)"):
        self.question = question
        self.answer = answer
    
    def showQuestion(self):
        return self.question
    
    def showAnswer(self):
        return self.answer
    
    def to_dict(self):
        return {"question": self.question, "answer": self.answer}
    
    @staticmethod
    def from_dict(data):
        return FlashCard(data["question"], data["answer"])