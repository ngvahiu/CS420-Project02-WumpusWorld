import copy
from pysat.solvers import Glucose3
class KnowledgeBase:
    def __init__(self):
        self.sentences = []


    @staticmethod
    def standardize_sentence(sentence):
        return sorted(list(set(sentence)))


    def tell(self, sentence):
        sentence = self.standardize_clause(sentence)
        if sentence not in self.sentences:
            self.sentences.append(sentence)


    def delete_sentence(self, sentence):
        sentence = self.standardize_sentence(sentence)
        if sentence in self.sentences:
            self.sentences.remove(sentence)


    def ask(self, sentence):
        g = Glucose3()
        clause_list = copy.deepcopy(self.sentences)
        not_sentence = -1 * sentence
        for it in clause_list:
            g.add_clause(it)
        for it in not_sentence:
            g.add_clause(it)
        sol = g.solve()
        if sol:
            return False
        return True