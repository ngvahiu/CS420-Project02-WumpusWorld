import math
from enum import Enum
from agent import Action
import pygame

from constants import *


class Cell:
    def __init__(self, x, y, type: str) -> None:
        self.x = x
        self.y = y
        self.visited = False
        self.type: str = type
        self.map_size = None
        self.img_list = {
            "arrow": None,
            "gold": None,
            "obstacle": None,  # agent, gold, pit, wumpus
            "agent": None,
            "breeze": None,
            "stench": None,
        }
        self.parent = None
        self.is_safe = True
        if 'W' in type or 'P' in type:
            self.is_safe = False
    
    def __eq__(self, other) -> bool:
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x+abs(self.y-(self.map_size-1)) <= other.x + abs(other.y-(self.map_size-1))

    def init_img_list(self):
        if self.type == "-":
            return
        for c in self.type:
            if c == "A":
                img = pygame.image.load(AGENT_RIGHT_IMG).convert_alpha()
                self.img_list["agent"] = img
            elif c == "G":
                img = pygame.image.load(CHEST_IMG).convert_alpha()
                self.img_list["gold"] = img
            elif c == "P":
                img = pygame.image.load(PIT_IMG).convert_alpha()
                self.img_list["obstacle"] = img
            elif c == "W":
                img = pygame.image.load(WUMPUS_IMG).convert_alpha()
                self.img_list["obstacle"] = img
            elif c == "S":
                img = pygame.image.load(STENCH_IMG).convert_alpha()
                self.img_list["stench"] = img
            elif c == "B":
                img = pygame.image.load(BREEZE_IMG).convert_alpha()
                self.img_list["breeze"] = img

    def check_cell(self, x, y, grid_cells: list):
        if not self.map_size:
            self.map_size = int(math.sqrt(len(grid_cells)))
        find_index = lambda x, y: x + y * self.map_size

        if x < 0 or y < 0 or x > self.map_size - 1 or y > self.map_size - 1:
            return False
        return grid_cells[find_index(x, y)]

    def get_neighbors(self, grid_cells: list):
        neighbors = []

        top = self.check_cell(self.x, self.y - 1, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        left = self.check_cell(self.x - 1, self.y, grid_cells)
        right = self.check_cell(self.x + 1, self.y, grid_cells)

        if right:
            neighbors.append(right)
        if left:
            neighbors.append(left)
        if top:
            neighbors.append(top)
        if bottom:
            neighbors.append(bottom)

        return neighbors

    def draw(self, screen):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE

        if not self.img_list["arrow"] and not self.visited:
            pygame.draw.rect(
                screen, pygame.Color(173, 116, 96), (x, y, CELL_SIZE, CELL_SIZE)
            )
        elif self.img_list["arrow"] and not self.visited:
            pygame.draw.rect(
                screen, pygame.Color(173, 116, 96), (x, y, CELL_SIZE, CELL_SIZE)
            )
            self.img_list["arrow"] = pygame.transform.scale(
                self.img_list["arrow"], (CELL_SIZE, CELL_SIZE)
            )
            screen.blit(
                self.img_list["arrow"],
                (
                    self.x * CELL_SIZE,
                    self.y * CELL_SIZE,
                ),
            )

            # if the cell containing a arrow has any pit or Wumpus -> set this cell's VISITED = True
            self.visited = True
            self.img_list["arrow"] = None
        elif self.visited:
            pygame.draw.rect(
                screen, pygame.Color(136, 56, 45), (x, y, CELL_SIZE, CELL_SIZE)
            )
            self.draw_image_cell(screen)

        pygame.draw.line(screen, pygame.Color(0, 0, 0), (x, y), (x + CELL_SIZE, y), 2)
        pygame.draw.line(
            screen,
            pygame.Color(0, 0, 0),
            (x + CELL_SIZE, y),
            (x + CELL_SIZE, y + CELL_SIZE),
            2,
        )
        pygame.draw.line(screen, pygame.Color(0, 0, 0), (x, y + CELL_SIZE), (x, y), 2)
        if not (self.x == 0 and self.y == self.map_size - 1):
            pygame.draw.line(
                screen,
                pygame.Color(0, 0, 0),
                (x + CELL_SIZE, y + CELL_SIZE),
                (x, y + CELL_SIZE),
                2,
            )
        else:  # Exit room
            pygame.draw.line(
                screen,
                pygame.Color(0, 0, 0),
                (0, y + CELL_SIZE),
                (CELL_SIZE // 4, y + CELL_SIZE),
                4,
            )
            pygame.draw.line(
                screen,
                pygame.Color(0, 0, 0),
                (CELL_SIZE * 3 // 4, y + CELL_SIZE),
                (CELL_SIZE, y + CELL_SIZE),
                4,
            )
            exit_sc = pygame.font.Font(FONT_STYLE, 15).render("EXIT", True, (0, 0, 0))
            exit_rect = exit_sc.get_rect()
            exit_rect.center = pygame.Rect(
                x, y + CELL_SIZE, CELL_SIZE, CELL_SIZE // 2
            ).center
            screen.blit(exit_sc, exit_rect)

    def draw_image_cell(self, screen):
        if self.type == "-":
            return
        breeze_stench_count = 0
        for c in self.type:
            if c == "B" or c == "S":
                breeze_stench_count += 1

        if self.img_list["gold"]:
            self.img_list["gold"] = pygame.transform.scale(
                self.img_list["gold"], (CELL_SIZE // 1.2, CELL_SIZE // 1.2)
            )
            screen.blit(
                self.img_list["gold"],
                (
                    self.x * CELL_SIZE + CELL_SIZE // 10,
                    self.y * CELL_SIZE + CELL_SIZE // 10,
                ),
            )
        if self.img_list["obstacle"]:
            self.img_list["obstacle"] = pygame.transform.scale(
                self.img_list["obstacle"], (CELL_SIZE // 1.2, CELL_SIZE // 1.2)
            )
            screen.blit(
                self.img_list["obstacle"],
                (
                    self.x * CELL_SIZE + CELL_SIZE // 10,
                    self.y * CELL_SIZE + CELL_SIZE // 10,
                ),
            )
        if self.img_list["agent"]:
            self.img_list["agent"] = pygame.transform.scale(
                self.img_list["agent"], (CELL_SIZE // 1.2, CELL_SIZE // 1.2)
            )
            screen.blit(
                self.img_list["agent"],
                (
                    self.x * CELL_SIZE + CELL_SIZE // 10,
                    self.y * CELL_SIZE + CELL_SIZE // 10,
                ),
            )
        if self.img_list["breeze"]:
            self.img_list["breeze"] = pygame.transform.scale(
                self.img_list["breeze"], (CELL_SIZE // breeze_stench_count, CELL_SIZE)
            )
            screen.blit(
                self.img_list["breeze"],
                (
                    self.x * CELL_SIZE,
                    self.y * CELL_SIZE,
                ),
            )
        if self.img_list["stench"]:
            if breeze_stench_count == 1:
                self.img_list["stench"] = pygame.transform.scale(
                    self.img_list["stench"],
                    (CELL_SIZE // breeze_stench_count, CELL_SIZE),
                )
                screen.blit(
                    self.img_list["stench"],
                    (
                        self.x * CELL_SIZE,
                        self.y * CELL_SIZE,
                    ),
                )
            elif breeze_stench_count == 2:
                self.img_list["stench"] = pygame.transform.scale(
                    self.img_list["stench"],
                    (CELL_SIZE // breeze_stench_count, CELL_SIZE),
                )
                screen.blit(
                    self.img_list["stench"],
                    (
                        self.x * CELL_SIZE + CELL_SIZE // breeze_stench_count,
                        self.y * CELL_SIZE,
                    ),
                )
    def has_pit(self):
        return 'P' in self.type
    
    def has_stench(self):
        return 'S' in self.type
    
    def has_wumpus(self):
        return 'W' in self.type
    
    def has_breeze(self):
        return 'B' in self.type
    
    def has_gold(self):
        return 'G' in self.type

    def get_location(self):
        return self.x * 10 + self.y

    def get_turn_action(self, other):
        if self.y == other.y:
            if self.x < other.x:
                return Action.TURN_RIGHT
            else:
                return Action.TURN_LEFT
        elif self.y < other.y:
            return Action.TURN_DOWN
        elif self.y > other.y:
            return Action.TURN_UP
    

    
    def remove_stench(self, grid_cells):
        if not self.has_wumpus():
            return
        self.is_safe = True
        neighbors = self.get_neighbors(grid_cells)
        for neighbor in neighbors:
            is_delete_stench = True
            neighbors_of_neighbor = neighbor.get_neighbors(grid_cells)
            if self in neighbors_of_neighbor:
                neighbors_of_neighbor.remove(self)
            for cell in neighbors_of_neighbor:
                if cell.has_wumpus() and cell.is_safe == False:
                    is_delete_stench = False
            if is_delete_stench:
                neighbor.type = neighbor.type[:neighbor.type.index('S')] + neighbor.type[neighbor.type.index('S') + 1:]
                if neighbor.type == '':
                    neighbor.type = '-'


        
