import copy
from dpll import SATSolver
class KnowledgeBase:
    def __init__(self):
        self.sentences = []

    def standardize_sentence(self, sentence):
        return sorted(list(set(sentence)))


    def tell(self, sentence):
        sentence = self.standardize_sentence(sentence)
        if sentence not in self.sentences:
            self.sentences.append(sentence)


    def delete_sentence(self, sentence):
        sentence = self.standardize_sentence(sentence)
        if sentence in self.sentences:
            self.sentences.remove(sentence)


    def ask(self, neg_sentence):
        clause_list = copy.deepcopy(self.sentences)
        clause_list.extend(neg_sentence)
        g = SATSolver(clause_list)
        satisfiable = g.solve()
        if satisfiable:
            return False
        return True