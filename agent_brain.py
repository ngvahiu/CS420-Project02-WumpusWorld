
from knowledge_base import KnowledgeBase
from agent import Action
from constants import *
class AgentBrain:
    def __init__(self, current_cell, map):
        self.current_cell = current_cell
        self.map = map
        self.KB = KnowledgeBase()
        self.action_list = []
    
    def solve(self):
        if self.current_cell.has_pit():
            self.action_list.append(Action.KILL_BY_PIT)
            return False
        elif self.current_cell.has_wumpus():
            self.action_list.append(Action.KILL_BY_WUMPUS)
            return False
        
        if self.current_cell.has_gold():
            self.action_list.append(Action.GRAB_GOLD)
        
        if self.current_cell.has_breeze():
            self.action_list.append(Action.PERCEIVE_BREEZE)
        if self.current_cell.has_stench():
            self.action_list.append(Action.PERCEIVE_STENCH)
        
        if self.current_cell.visited == False:
            self.current_cell.visited = True
            self.tell_knowledge_base(self.current_cell)
        
        neighbors = self.current_cell.get_neighbors()
        remove_list = []
        for neighbor in neighbors:
            if neighbor == self.current_cell.parent:
                remove_list.append(neighbor)
            elif neighbor.visited == True and neighbor.has_pit():
                remove_list.append(neighbor)
        
        for cell in remove_list:
            neighbors.remove(cell)

        remove_list = []

        if self.current_cell.has_stench():
            for neighbor in neighbors:
                sentence = WUMPUS*100 + neighbor.get_location()
                detect_wumpus = self.KB.ask(sentence)
                if detect_wumpus:
                    turn_action = self.current_cell.get_turn_action(neighbor)
                    self.action_list.append(turn_action)
                    self.action_list.append(Action.SHOOT)
                else:
                    sentence = -1 * (WUMPUS*100 + neighbor.get_location)
                    detect_not_wumpus = self.KB.ask(sentence)
                    if detect_not_wumpus:
                        self.KB.tell(sentence)
                    else:
                        remove_list.add(neighbor)
            if self.current_cell.has_stench():
                for neighbor in neighbors:
                    turn_action = self.current_cell.get_turn_action(neighbor)
                    self.action_list.append(turn_action)
                    self.action_list.append(Action.SHOOT)
                
        if self.current_cell.has_breeze():
            for neighbor in neighbors:
                sentence = PIT*100 + neighbor.get_location()
                detect_pit = self.KB.ask(sentence)
                if detect_pit:
                    #detect pit
                    neighbor.visited = True
                    self.KB.tell(sentence)
                    if neighbor not in remove_list:
                        remove_list.append(neighbor)
                else:
                    sentence  = -1*(PIT*100 + neighbor.get_location())
                    detect_not_pit = self.KB.ask(sentence)
                    if detect_not_pit:
                        self.KB.tell(sentence)
                    else:
                        if neighbor not in remove_list:
                            remove_list.append(neighbor)
        
        for cell in remove_list:
            neighbors.remove(cell)
        
        current_cell = self.current_cell
        
        for neighbor in neighbors:
            turn_action = self.current_cell.get_turn_action(neighbor)
            self.action_list.append(turn_action)
            self.action_list.append(Action.MOVE_FORWARD)
            self.current_cell = neighbor

            result = self.solve()
            if result == False:
                return False

            turn_action = self.current_cell.get_turn_action(current_cell)
            self.action_list.append(turn_action)
            self.action_list.append(Action.MOVE_FORWARD)
            self.current_cell = current_cell
        
        return True



        
    
    def tell_knowledge_base(self, current_cell):
        neighbors = current_cell.get_neighbors()

        if current_cell.has_pit():
            self.KB.tell([PIT*100 + current_cell.get_location()])
        else:
            self.KB.tell([-1 * (PIT*100 + current_cell.get_location())])
            
        if current_cell.has_wumpus():
            self.KB.tell([WUMPUS*100 + current_cell.get_location()])
        else:
            self.KB.tell([-1 * (WUMPUS*100 + current_cell.get_location())])
        
        if current_cell.has_breeze():
            self.KB.tell([BREEZE*100 + current_cell.get_location()])
            sentence = [[-1 * (BREEZE*100 + current_cell.get_location())]]
            for neighbor in neighbors:
                if neighbor.visited == False:
                    sentence.append(PIT*100 + neighbor.get_location())
            self.KB.tell(sentence)
            for neighbor in neighbors:
                self.KB.tell([BREEZE*100 + current_cell.get_location(), -1 * (PIT * 100 + neighbor.get_location())])
        else:
            self.KB.tell([-1 * (BREEZE*100 + current_cell.get_location())])
            for neighbor in neighbors:
                if neighbor.visited == False:
                    self.KB.tell([-1*(PIT*100 + neighbor.get_location)])
        
        if current_cell.has_stench():
            self.KB.tell([STENCH*100 + current_cell.get_location()])
            sentence = [[-1 * (STENCH*100 + current_cell.get_location())]]
            for neighbor in neighbors:
                if neighbor.visited == False:
                    sentence.append(WUMPUS*100 + neighbor.get_location())
            self.KB.tell(sentence)
            for neighbor in neighbors:
                self.KB.tell([STENCH*100 + current_cell.get_location(), -1 * (WUMPUS * 100 + neighbor.get_location())])
        else:
            self.KB.tell([-1 * (STENCH*100 + current_cell.get_location())])
            for neighbor in neighbors:
                if neighbor.visited == False:
                    self.KB.tell([-1*(WUMPUS*100 + neighbor.get_location)])
