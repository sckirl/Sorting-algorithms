import pygame
import sys
from math import sqrt
from premade import rick
pygame.init()
win_x, win_y = 800, 460
win = pygame.display.set_mode((win_x, win_y), pygame.RESIZABLE)  # display config

pygame.display.set_caption("Pathfinding Algorithms")
clock = pygame.time.Clock()

class Node(object):
    def __init__(self, parent=None, position=None):
        self.parent = parent  # getting parent nodes, for making nodes of the shortest path
        self.position = position
        # g, h, f value for 'predicting' where to move
        self.g = 0
        self.h = 0
        self.f = 0

        self.value = 0

class Algorithm(object):
    def __init__(self):
        # important variables
        self.Astar_run = False
        self.Dijkstra_run = False
        self.finished = False

        self.open_list = []
        self.closed_list = []
        self.path = []
        self.walls = []

        self.start_node = Node(None, None)
        self.start_node.g = self.start_node.h = self.start_node.f = 0
        self.end_node = Node(None, None)
        self.children = []
        self.open_list.append(self.start_node)
        self.current_node = self.open_list[0]

        self.start_icon = pygame.image.load('Start-icon.png').convert_alpha()
        self.start_icon = pygame.transform.smoothscale(self.start_icon, (20, 20))
        self.target_icon = pygame.image.load('Target-icon.png')
        self.target_icon = pygame.transform.smoothscale(self.target_icon, (20, 20))

        self.build_wall, self.delete_wall = False, False

    def A_star(self):
        infoObject = pygame.display.Info()
        win_x, win_y = infoObject.current_w, infoObject.current_h

        # try:
        # making a loop for A star (can't have two continuous 'while' loop in one program, so the loop is from main loop)
        if len(self.open_list) > 0 and self.Astar_run:
            open_nodes = [open_node.f for open_node in self.open_list]
            self.current_node = self.open_list[open_nodes.index(min(open_nodes))]

            self.open_list.remove(self.current_node)  # remove current node from open list
            self.closed_list.append(self.current_node)  # add current node from closed list

            # find the end node
            if self.current_node.position == self.end_node.position:
                current = self.current_node
                self.finished = True
                self.Astar_run = False
                self.path.append(self.end_node)
                try:
                    while self.current_node is not None:
                        self.path.append(current)
                        current = current.parent
                except: pass

            # generate children
            for new_position in [(0, -20), (0, 20), (-20, 0), (20, 0), (-20, -20), (-20, 20), (20, -20), (20, 20)]: # make square-shaped new positions
                new_child = (self.current_node.position[0] + new_position[0], self.current_node.position[1] + new_position[1])
                # make sure new child don't go through walls
                if new_child in self.walls: continue
                if new_child[0] > win_x - 20 or new_child[1] > win_y - 20 or new_child[0] < 0 or new_child[1] < 0: continue

                self.children.append(Node(self.current_node, new_child))
                # children values are in 'Node' class, important for the next process

            for child in self.children:
                # getting g, h, f values for each children
                child.g = self.current_node.g + 1
                child.h = abs(child.position[0] - self.end_node.position[0]) \
                          + abs(child.position[1] - self.end_node.position[1]) # Manhattan Distance
                child.f = child.g + child.h

                if child not in self.open_list and child not in self.closed_list:
                    self.open_list.append(child)
        '''except:
            print("Note: You need to add start node and end node for A* algorithm")'''

    def Dijkstra(self):
        infoObject = pygame.display.Info()
        win_x, win_y = infoObject.current_w, infoObject.current_h

        try:
            if self.Dijkstra_run:
                for positions in [(20, 0), (-20, 0), (0, 20), (0, -20)]:
                    new_nodes = (
                        (self.current_node.position[0] + positions[0], self.current_node.position[1] + positions[1]))

                    if new_nodes in self.walls: continue
                    if new_nodes[0] > win_x - 20 or new_nodes[1] > win_y - 20 or new_nodes[0] < 0 or new_nodes[1] < 0: continue

                    children_positions = [i.position for i in self.children]
                    if new_nodes not in children_positions:
                        self.children.append(Node(self.current_node, new_nodes))

                for child in self.children:
                    child.value = abs(self.open_list[0].position[0] - child.position[0]) \
                                  + abs(self.open_list[0].position[1] - child.position[1])
                    if child not in self.open_list and child not in self.closed_list:
                        self.open_list.append(child)

                search = [i.value for i in self.open_list]
                self.current_node = self.open_list[search.index(min(search))]

                if len(self.open_list) > 1:
                    self.closed_list.append(self.current_node)
                    self.open_list.remove(self.current_node)

                # find the end node
                if self.current_node.position == self.end_node.position:
                    current = self.current_node
                    self.finished = True
                    self.Dijkstra_run = False
                    self.path.append(self.end_node)
                    try:
                        while self.current_node is not None:
                            self.path.append(current)
                            current = current.parent
                    except: pass
        except:
            print("Note: Put your start node (at the very least)")

    def draw(self):
        if len(self.open_list) > 1:
            for open_nodes in self.open_list:
                pygame.draw.rect(win, [51, 166, 166], (open_nodes.position[0], open_nodes.position[1], 20, 20))

        for closed_nodes in self.closed_list:
            pygame.draw.rect(win, [22, 128, 140], (closed_nodes.position[0], closed_nodes.position[1], 20, 20))

        for wall in self.walls:
            pygame.draw.rect(win, [1, 35, 38], (wall[0], wall[1], 20, 20))

        for nodes in range(1, len(self.path)):
            try: pygame.draw.rect(win, [213, 242, 237], (self.path[nodes].position[0], self.path[nodes].position[1], 20, 20))
            except: pass

        if self.end_node.position is not None: win.blit(self.target_icon, self.end_node.position)
        if self.start_node.position is not None: win.blit(self.start_icon, self.start_node.position)

    def make_walls(self):
        x, y = pygame.mouse.get_pos()
        ix, iy = x // 20, y // 20
        if self.build_wall:
            self.walls.append((ix * 20, iy * 20))
        try:
            if self.delete_wall:
                self.walls.remove((ix * 20, iy * 20))
        except: pass

    def restart(self):
        self.open_list = [self.start_node]
        self.current_node = self.open_list[0]
        self.closed_list.clear()
        self.children.clear()
        self.path.clear()
        self.Astar_run = False
        self.Dijkstra_run = False

def add_nodes():
    x, y = pygame.mouse.get_pos()
    ix, iy = x // 20, y // 20
    return (ix * 20, iy * 20)

Pathfinding = Algorithm()

blockSize = 20 #Set the size of the grid block
def drawgrid():
    infoObject = pygame.display.Info()
    win_x, win_y = infoObject.current_w, infoObject.current_h
    for i in range(0, win_x, blockSize):
        x, y = i, i
        pygame.draw.line(win, (100, 100, 100), (x, 0), (x, win_y))
        pygame.draw.line(win, (100, 100, 100), (0, y), (win_x, y))

def redraw():
    win.fill((255, 255, 255))
    drawgrid()
    Pathfinding.draw()
    pygame.display.update()

def main():
    while 1:

        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Pathfinding.restart()
                    Pathfinding.Astar_run = True
                if event.key == pygame.K_2:
                    Pathfinding.restart()
                    Pathfinding.Dijkstra_run = True

                if event.key == pygame.K_TAB:
                    Pathfinding.end_node.position = add_nodes()

                if event.key == pygame.K_w:
                    Pathfinding.build_wall = True
                if event.key == pygame.K_q:
                    Pathfinding.delete_wall = True
                if event.key == pygame.K_c:
                    Pathfinding.walls.clear()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    Pathfinding.build_wall = False
                if event.key == pygame.K_q:
                    Pathfinding.delete_wall = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pathfinding.restart()
                Pathfinding.start_node.position = add_nodes()

        Pathfinding.Dijkstra()
        Pathfinding.make_walls()
        Pathfinding.A_star()
        redraw()

if __name__ == '__main__':
    main()