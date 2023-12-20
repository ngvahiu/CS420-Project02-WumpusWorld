
from knowledge_base import KnowledgeBase
from agent import Action
from constants import *
class AgentBrain:
    def __init__(self, current_cell, grid_cells):
        self.current_cell = current_cell
        self.grid_cells = grid_cells
        self.KB = KnowledgeBase()
        self.action_list = []
        self.action_cells = {}
        self.found_exit = False
        self.remain_cells = []
    
    def solve(self):
        if self.current_cell.has_pit():
            self.action_list.append(Action.KILL_BY_PIT)
            return False
        elif self.current_cell.has_wumpus() and self.current_cell.is_safe == False:
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
        
        neighbors = self.current_cell.get_neighbors(self.grid_cells)
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
                self.action_list.append(Action.INFER_WUMPUS)
                sentence = WUMPUS*100 + neighbor.get_location()
                detect_wumpus = self.KB.ask([[-1*sentence]])
                self.action_cells[len(self.action_list)] = neighbor
                if detect_wumpus:
                    self.action_list.append(Action.DETECT_WUMPUS)
                    turn_action = self.current_cell.get_turn_action(neighbor)
                    self.action_list.append(turn_action)
                    self.action_list.append(Action.SHOOT)
                    self.action_list.append(Action.KILL_WUMPUS)
                    neighbor.remove_stench(self.grid_cells)
                    self.remove_wumpus(neighbor)
                    self.KB.tell([-1*(PIT*100 + neighbor.get_location())])
                    self.action_list.append(Action.REMOVE_KNOWLEDGE_RELATED_TO_WUMPUS)
                else:
                    sentence = -1 * (WUMPUS*100 + neighbor.get_location())
                    detect_not_wumpus = self.KB.ask([[-1*sentence]])
                    if detect_not_wumpus:
                        self.action_list.append(Action.DETECT_NO_WUMPUS)
                        self.KB.tell([sentence])
                    else:
                        self.action_list.append(Action.FAIL_TO_INFER)
                        remove_list.append(neighbor)
            if self.current_cell.has_stench():
                self.action_list.append(Action.SHOOT_RANDOMLY)
                for neighbor in neighbors:
                    turn_action = self.current_cell.get_turn_action(neighbor)
                    self.action_list.append(turn_action)
                    self.action_list.append(Action.SHOOT)
                    if neighbor.have_wumpus():
                        self.action_list.append(Action.KILL_WUMPUS)
                        neighbor.remove_stench(self.grid_cells)
                        self.remove_wumpus(neighbor)
                        self.action_list.append(Action.REMOVE_KNOWLEDGE_RELATED_TO_WUMPUS)
                    else:
                        self.action_list.append(Action.KILL_NO_WUMPUS)
                
        if self.current_cell.has_breeze():
            for neighbor in neighbors:
                self.action_list.append(Action.INFER_PIT)
                sentence = PIT*100 + neighbor.get_location()
                detect_pit = self.KB.ask([[-1*sentence]])
                self.action_cells[len(self.action_list)] = neighbor
                if detect_pit:
                    neighbor.visited = True
                    self.action_list.append(Action.DETECT_PIT)
                    self.KB.tell([sentence])
                    if neighbor not in remove_list:
                        remove_list.append(neighbor)
                else:
                    sentence  = -1*(PIT*100 + neighbor.get_location())
                    detect_not_pit = self.KB.ask([[-1*sentence]])
                    if detect_not_pit:
                        self.action_list.append(Action.DETECT_NO_PIT)
                        self.KB.tell([sentence])
                    else:
                        self.action_list.append(Action.FAIL_TO_INFER)
                        if neighbor not in remove_list:
                            remove_list.append(neighbor)
        
        for cell in remove_list:
            neighbors.remove(cell)
        
        
        current_cell = self.current_cell

        for cell in neighbors:
            if cell not in self.remain_cells and not cell.visited:
                self.remain_cells.append(cell)

        for neighbor in neighbors:
            if neighbor in self.remain_cells:
                self.remain_cells.remove(neighbor)
            if neighbor.visited == False:
                turn_action = self.current_cell.get_turn_action(neighbor)
                self.action_list.append(turn_action)
                self.action_list.append(Action.MOVE_FORWARD)
                self.current_cell = neighbor
                
                self.current_cell.parent = current_cell

                result = self.solve()
                if result == False:
                    return False

                if len(self.remain_cells) == 0:
                    return True

                turn_action = self.current_cell.get_turn_action(current_cell)
                self.action_list.append(turn_action)
                self.action_list.append(Action.MOVE_FORWARD)
                self.current_cell = current_cell
            
        return True

    def find_exit(self):
        self.current_cell.visited = True
        if self.found_exit:
            return
        if self.current_cell.x == 0 and self.current_cell.y == self.current_cell.map_size -1:
            self.found_exit = True
            return 
        neighbors = self.current_cell.get_neighbors(self.grid_cells)
        remove_list = []
        for neighbor in neighbors:
            if neighbor.is_safe == False or neighbor.visited:
                remove_list.append(neighbor)
        for cell in remove_list:
            neighbors.remove(cell)
        neighbors.sort()
        current_cell = self.current_cell
        for neighbor in neighbors:
            turn_action = self.current_cell.get_turn_action(neighbor)
            self.action_list.append(turn_action)
            self.action_list.append(Action.MOVE_FORWARD)
            self.current_cell = neighbor

            self.find_exit()
            if self.found_exit:
                return

            turn_action = self.current_cell.get_turn_action(current_cell)
            self.action_list.append(turn_action)
            self.action_list.append(Action.MOVE_FORWARD)
            self.current_cell = current_cell
        
    
    def tell_knowledge_base(self, current_cell):
        neighbors = current_cell.get_neighbors(self.grid_cells)

        if current_cell.has_pit():
            self.KB.tell([PIT*100 + current_cell.get_location()])
        else:
            self.KB.tell([-1 * (PIT*100 + current_cell.get_location())])
            
        if current_cell.has_wumpus() and not current_cell.is_safe:
            self.KB.tell([WUMPUS*100 + current_cell.get_location()])
        else:
            self.KB.tell([-1 * (WUMPUS*100 + current_cell.get_location())])
        
        if current_cell.has_breeze():
            self.KB.tell([BREEZE*100 + current_cell.get_location()])
            sentence = [-1 * (BREEZE*100 + current_cell.get_location())]
            for neighbor in neighbors:
                sentence.append(PIT*100 + neighbor.get_location())
            self.KB.tell(sentence)
            for neighbor in neighbors:
                self.KB.tell([BREEZE*100 + current_cell.get_location(), -1 * (PIT * 100 + neighbor.get_location())])
        else:
            self.KB.tell([-1 * (BREEZE*100 + current_cell.get_location())])
            for neighbor in neighbors:
                self.KB.tell([-1*(PIT*100 + neighbor.get_location())])
        
        if current_cell.has_stench():
            self.KB.tell([STENCH*100 + current_cell.get_location()])
            sentence = [-1 * (STENCH*100 + current_cell.get_location())]
            for neighbor in neighbors:
                sentence.append(WUMPUS*100 + neighbor.get_location())
            self.KB.tell(sentence)
            for neighbor in neighbors:
                self.KB.tell([STENCH*100 + current_cell.get_location(), -1 * (WUMPUS * 100 + neighbor.get_location())])
        else:
            self.KB.tell([-1 * (STENCH*100 + current_cell.get_location())])
            for neighbor in neighbors:
                self.KB.tell([-1*(WUMPUS*100 + neighbor.get_location())])
    
    def remove_wumpus(self, cell):
        symbol = WUMPUS*100 + cell.get_location()
        remove_list = []
        for sentence in self.KB.sentences:
            if symbol in sentence or -1*symbol in sentence:
                remove_list.append(sentence)
        
        for sentence in remove_list:
            self.KB.sentences.remove(sentence)
