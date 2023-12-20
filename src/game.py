import sys
from agent_brain import AgentBrain
import pygame

from agent import *
from constants import *
from map import Map
from notfication import Notification


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.caption = pygame.display.set_caption(TITLE)
        self.font = pygame.font.Font(FONT_STYLE, 30)
        self.font_score = pygame.font.Font(FONT_STYLE, 50)
        self.font_title = pygame.font.Font(FONT_STYLE, 70)

        self.map = None
        self.map_size = None

        self.state = "menu"

        self.agent = Agent()

        self.agent_brain = None

        self.current_step = 0

    def draw_running_screen(self, noti_type: Notification = None):
        self.screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # draw score and gold collected
        score = self.agent.score
        score_text = self.font_score.render(
            "YOUR SCORE: " + str(score), True, (0, 0, 0)
        )
        score_rect = score_text.get_rect()
        score_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 5,
            WINDOW_HEIGHT // 5,
        )
        self.screen.blit(score_text, score_rect)

        gold = self.agent.gold
        gold_text = self.font.render("Gold collected: " + str(gold), True, (0, 0, 0))
        gold_rect = gold_text.get_rect()
        gold_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 5,
            WINDOW_HEIGHT // 4,
        )
        self.screen.blit(gold_text, gold_rect)

        # draw map
        self.map.draw(self.screen)

        # draw notification
        if noti_type:
            self.draw_notification(noti_type)

        pygame.display.update()

    def draw_title(self, rect, title, title_color):
        title_sc = self.font_title.render(title, True, title_color)
        title_rect = title_sc.get_rect()
        title_rect.center = rect.center
        self.screen.blit(title_sc, title_rect)

    def draw_button(self, sc, rect, button_color, text, text_color):
        # draw button
        pygame.draw.rect(sc, button_color, rect)
        # draw text inside button
        text_sc = self.font.render(text, True, text_color)
        text_rect = text_sc.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_sc, text_rect)

    def draw_notification(self, noti_type: Notification):
        if noti_type == Notification.KILL_WUMPUS:
            text = self.font.render("KILL WUMPUS !", True, (23, 127, 117))
            img = pygame.image.load(WUMPUS_IMG).convert_alpha()
        elif noti_type == Notification.DETECT_PIT:
            text = self.font.render("DETECT PIT !", True, (23, 127, 117))
            img = pygame.image.load(PIT_IMG).convert_alpha()
        elif noti_type == Notification.COLLECT_GOLD:
            text = self.font.render("COLLECT GOLD !: +1000", True, (23, 127, 117))
            img = pygame.image.load(CHEST_IMG).convert_alpha()
        elif noti_type == Notification.SHOOT_ARROW:
            text = self.font.render("SHOOT ARROW !: -100", True, (23, 127, 117))
            img = pygame.image.load(ARROW_RIGHT_IMG).convert_alpha()

        # Show text notification
        text_rect = text.get_rect()
        text_rect.center = (
            WINDOW_WIDTH // 2 + CELL_SIZE * 5,
            WINDOW_HEIGHT // 2,
        )
        self.screen.blit(text, text_rect)
        # Show image
        img = pygame.transform.scale(img, (CELL_SIZE * 3, CELL_SIZE * 3))
        self.screen.blit(
            img,
            (
                WINDOW_WIDTH // 2 + CELL_SIZE * 3.5,
                WINDOW_HEIGHT // 1.5,
            ),
        )

        pygame.display.update()
        pygame.time.delay(500)

    def draw_menu_screen(self):
        self.screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 350 <= mouse[0] <= 800 and 150 <= mouse[1] <= 200:
                    self.state = "solving"
                    self.map = Map(MAP_1)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                elif 350 <= mouse[0] <= 800 and 230 <= mouse[1] <= 300:
                    self.state = "solving"
                    self.map = Map(MAP_2)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                elif 350 <= mouse[0] <= 800 and 310 <= mouse[1] <= 360:
                    self.state = "solving"
                    self.map = Map(MAP_3)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                elif 350 <= mouse[0] <= 800 and 390 <= mouse[1] <= 440:
                    self.state = "solving"
                    self.map = Map(MAP_4)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                elif 350 <= mouse[0] <= 800 and 470 <= mouse[1] <= 520:
                    self.state = "solving"
                    self.map = Map(MAP_5)
                    self.map_size = self.map.map_size
                    self.agent.cell = self.map.get_agent_cell()
                    self.agent.map_size = self.map.map_size
                elif 350 <= mouse[0] <= 800 and 550 <= mouse[1] <= 600:
                    pygame.quit()
                    sys.exit()

            # draw title
            self.draw_title(pygame.Rect(200, 40, 800, 50), "Wumpus World", (0, 0, 0))
            # draw buttons
            self.draw_button(
                self.screen,
                pygame.Rect(350, 150, 500, 50),
                (136, 56, 45),
                "MAP 1",
                (255, 255, 255),
            )
            self.draw_button(
                self.screen,
                pygame.Rect(350, 230, 500, 50),
                (136, 56, 45),
                "MAP 2",
                (255, 255, 255),
            )
            self.draw_button(
                self.screen,
                pygame.Rect(350, 310, 500, 50),
                (136, 56, 45),
                "MAP 3",
                (255, 255, 255),
            )
            self.draw_button(
                self.screen,
                pygame.Rect(350, 390, 500, 50),
                (136, 56, 45),
                "MAP 4",
                (255, 255, 255),
            )
            self.draw_button(
                self.screen,
                pygame.Rect(350, 470, 500, 50),
                (136, 56, 45),
                "MAP 5",
                (255, 255, 255),
            )
            self.draw_button(
                self.screen,
                pygame.Rect(350, 550, 500, 50),
                (136, 56, 45),
                "EXIT",
                (255, 255, 255),
            )
            pygame.display.update()

    def draw_success_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        background = pygame.image.load(SUCCESS_IMAGE).convert()
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(background, (0, 0))

        text = self.font_title.render("SUCCESSFUL!!!", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, 50)
        self.screen.blit(text, text_rect)

        score = self.agent.score
        text = self.font_score.render("Your score: " + str(score), True, (0, 0, 0))
        text_rect.center = (WINDOW_WIDTH // 2 + 70, 150)
        self.screen.blit(text, text_rect)

        pygame.display.update()
        pygame.time.delay(3000)
        self.state = "menu"

    def draw_failed_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        background = pygame.image.load(FAILED_IMAGE).convert()
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(background, (0, 0))

        text = self.font_title.render("FAILED !!!", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, 50)
        self.screen.blit(text, text_rect)

        text = self.font.render("Try to solve again :(", True, (255, 255, 255))
        text_rect.center = (WINDOW_WIDTH // 2, 150)
        self.screen.blit(text, text_rect)

        pygame.display.update()
        pygame.time.delay(3000)
        self.state = "menu"

    def run(self):
        while True:
            if self.state == "menu":
                self.draw_menu_screen()
            elif self.state == "solving":
                self.solve()
            elif self.state == 'show_result':
                self.show_result()
            elif self.state == "success":
                self.draw_success_screen()
            elif self.state == "failed":
                self.draw_failed_screen()

    def show_result(self):
        self.draw_running_screen()

        # return if finish the action list
        if self.current_step == len(self.action_list):
            self.state = "success"
            return
        
        # get action
        action = self.action_list[self.current_step]

        # increase the step
        if len(self.action_list) > self.current_step:
            self.current_step +=1
        
        # perform action
        match action:
            case Action.TURN_LEFT:
                self.agent.turn_left()
            case Action.TURN_RIGHT:
                self.agent.turn_right()
            case Action.TURN_UP:
                self.agent.turn_up()
            case Action.TURN_DOWN:
                self.agent.turn_down()
            case Action.MOVE_FORWARD:
                from cell import Cell
                self.agent.move_forward(self.map.grid_cells)
            case Action.GRAB_GOLD:
                self.draw_running_screen(Notification.COLLECT_GOLD)
                self.agent.collect_gold()
            case Action.PERCEIVE_BREEZE:
                print("Perceiving breeze")
            case Action.PERCEIVE_STENCH:
                print("Perceiving stench")
            case Action.SHOOT:
                print("Shooting wumpus")
                arrow_cell = self.agent.shoot_arrow(self.map.grid_cells)
                self.draw_running_screen(Notification.SHOOT_ARROW)
            case Action.KILL_WUMPUS:
                print("Killing Wumpus")
            case Action.KILL_NO_WUMPUS:
                print("Killing, but no Wumpus found")
            case Action.KILL_BY_WUMPUS:
                print("Killed by Wumpus")
            case Action.KILL_BY_PIT:
                print("Killed by Pit")
            case Action.CLIMB_OUT_OF_THE_CAVE:
                print("Climbing out of the cave")
            case Action.DETECT_PIT:
                pit_cell = self.agent_brain.action_cells[self.current_step - 1]
                pit_x, pit_y = pit_cell.x, pit_cell.y
                print("Detect pit at:", pit_x, pit_y)
                pit_cell.visited = True
            case Action.DETECT_WUMPUS:
                wumpus_cell = self.agent_brain.action_cells[self.current_step - 1]
                wumpus_x, wumpus_y = wumpus_cell.x, wumpus_cell.y
                print("Detect wumpus at:", wumpus_x, wumpus_y)
                wumpus_cell.visited = True
            case Action.DETECT_NO_PIT:
                pit_cell = self.agent_brain.action_cells[self.current_step - 1]
                pit_x, pit_y = pit_cell.x, pit_cell.y
                print("Detect no pit at:", pit_x, pit_y)
            case Action.DETECT_NO_WUMPUS:
                wumpus_cell = self.agent_brain.action_cells[self.current_step - 1]
                wumpus_x, wumpus_y = wumpus_cell.x, wumpus_cell.y
                print("Detect no wumpus at:", wumpus_x, wumpus_y)
            case Action.INFER_PIT:
                print("Inferring pit")
            case Action.INFER_WUMPUS:
                print("Inferring Wumpus")
            case Action.REMOVE_KNOWLEDGE_RELATED_TO_WUMPUS:
                print("Remove knowledge related to killed wumpus")
            case Action.SHOOT_RANDOMLY:
                print("Start shooting randomly")
            case Action.FAIL_TO_INFER:
                infer_cell = self.agent_brain.action_cells[self.current_step - 1]
                infer_cell_x, infer_cell_y = infer_cell.x, infer_cell.y
                print("Fail to infer cell:", infer_cell_x, infer_cell_y)
            case _:
                print("Unknown action")
        self.draw_running_screen()
        pygame.time.delay(100)
    
    def solve(self):
        agent_cell = self.agent.cell
        self.agent_brain = AgentBrain(self.agent.cell, self.map.grid_cells)
        self.agent_brain.solve()
        self.action_list = self.agent_brain.action_list
        # if agent is at the exist, just climb out
        if self.agent.cell.x == 0 and self.agent.cell.y == self.agent.cell.map_size - 1:
            self.action_list.append(Action.TURN_DOWN)
            self.action_list.append(Action.CLIMB_OUT_OF_THE_CAVE)
        else:
            # find the exist cell
            exist_cell = None
            for cell in self.map.grid_cells:
                if cell.x == 0 and cell.y == cell.map_size - 1:
                    exist_cell = cell
            
            # find way out for agent
            if exist_cell.visited:
                for cell in self.map.grid_cells:
                    cell.visited = False
                self.agent_brain.action_list = []
                self.agent_brain.find_exist()
                self.action_list.extend(self.agent_brain.action_list)
            # if exist cell has not been visited before => can not go to exist cell
            else:
                print("Agent can not find way out")

        # reset the visited list to render in UI later
        for cell in self.map.grid_cells:
            cell.visited = False
        agent_cell.visited = True
        self.state = 'show_result'
