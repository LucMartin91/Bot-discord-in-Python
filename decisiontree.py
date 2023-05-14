class DecisionTree:
    def __init__(self, question=None, yes_branch=None, no_branch=None, answer=None):
        self.question = question
        self.yes_branch = yes_branch
        self.no_branch = no_branch
        self.answer = answer

    def is_leaf(self):
        return self.yes_branch is None and self.no_branch is None
