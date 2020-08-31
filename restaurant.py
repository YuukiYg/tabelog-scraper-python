# coding: utf-8

class Restaurant():
    def __init__(self):
        self.name = "-"
        self.genre = "-"
        self.dinner_budget = "-"
        self.lunch_budget = "-"
        self.address = "-"
        self.url = "-"

    @property
    def score(self):
        return self.score

    @score.setter
    def score(self, score):
        if score < 0:
            self.score = score
            return
        else:
            raise ValueError("score must be a positive number.")
