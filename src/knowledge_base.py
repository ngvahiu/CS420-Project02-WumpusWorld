import copy
from dpll import SATSolver
class KnowledgeBase:
    def __init__(self):
        self.sentences = []


    @staticmethod
    def standardize_sentence(sentence):
        return sorted(list(set(sentence)))


    def tell(self, sentence):
        sentence = self.standardize_sentence(sentence)
        if sentence not in self.sentences:
            self.sentences.append(sentence)


    def delete_sentence(self, sentence):
        sentence = self.standardize_sentence(sentence)
        if sentence in self.sentences:
            self.sentences.remove(sentence)


    def ask(self, sentence):
        clause_list = copy.deepcopy(self.sentences)
        clause_list.extend(sentence)
        g = SATSolver(clause_list)
        sol = g.solve()
        if sol:
            return False
        return True