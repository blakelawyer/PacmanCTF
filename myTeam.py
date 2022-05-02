# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import capture
from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game



def createTeam(firstIndex, secondIndex, isRed,
               first='OffenseAgent', second='DefenseAgent'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


class ParentAgent(CaptureAgent):

    def getMazeDistance(self, pos1, pos2):
        d = self.distancer.getDistance(pos1, pos2)
        return d

    def deadzone_heuristic(self, game, point, deadzones):
        cost1 = 0
        cost2 = 0
        if point in deadzones:
            cost1 = self.bfsHeuristicDZ(game, point, deadzones)
        #if inside_chokepoint:
            #cost2 = self.bfsHeuristicCP(game, point, outside_chokepoint)
        #return cost1 + cost2
        return cost1 * 2


    def aStar(self, game, start, goal):

        visited = []  # Visited list to prevent expanding a node multiple times.
        astar_priority_queue = util.PriorityQueue()
        astar_priority_queue.push((start, [], 0), 0)

        while not astar_priority_queue.isEmpty():
            node = astar_priority_queue.pop()
            current_position = node[0]
            path = node[1]
            cost = node[2]
            if current_position == goal:
                return path, cost
            else:
                if current_position not in visited:
                    visited.append(current_position)
                    successors = []
                    x, y = node[0]
                    if not game.hasWall(x - 1, y) and (x - 1, y) not in visited:
                        successors.append((x - 1, y, 'West'))
                    if not game.hasWall(x + 1, y) and (x + 1, y) not in visited:
                        successors.append((x + 1, y, 'East'))
                    if not game.hasWall(x, y - 1) and (x, y - 1) not in visited:
                        successors.append((x, y - 1, 'South'))
                    if not game.hasWall(x, y + 1) and (x, y + 1) not in visited:
                        successors.append((x, y + 1, 'North'))
                    for s in successors:
                        path_history = []
                        path_history.extend(node[1])
                        path_history.extend([s[2]])
                        astar_priority_queue.push(((s[0], s[1]), path_history,
                                                   self.getMazeDistance(current_position, (s[0], s[1])) + node[2]),
                                                  self.getMazeDistance(current_position, (s[0], s[1])) + node[2])

    def aStarEatHeuristic(self, game, goal, deadzones):

        visited = []  # Visited list to prevent expanding a node multiple times.
        astar_priority_queue = util.PriorityQueue()
        astar_priority_queue.push((game.getAgentPosition(self.index), [], 0), 0)

        while not astar_priority_queue.isEmpty():
            node = astar_priority_queue.pop()
            current_position = node[0]
            path = node[1]
            cost = node[2]
            if node[0] == goal:
                    return path, (node[0][0], node[0][1]), cost
            if current_position not in visited:
                visited.append(current_position)
                successors = []
                x, y = node[0]
                if not game.hasWall(x - 1, y) and (x - 1, y) not in visited:
                    successors.append((x - 1, y, 'West'))
                if not game.hasWall(x + 1, y) and (x + 1, y) not in visited:
                    successors.append((x + 1, y, 'East'))
                if not game.hasWall(x, y - 1) and (x, y - 1) not in visited:
                    successors.append((x, y - 1, 'South'))
                if not game.hasWall(x, y + 1) and (x, y + 1) not in visited:
                    successors.append((x, y + 1, 'North'))
                for s in successors:
                    path_history = []
                    path_history.extend(node[1])
                    path_history.extend([s[2]])
                    astar_priority_queue.push(((s[0], s[1]), path_history,
                                               self.getMazeDistance(current_position, (s[0], s[1])) + node[
                                                   2] + self.deadzone_heuristic(game, (s[0], s[1]), deadzones)),
                                              self.getMazeDistance(current_position, (s[0], s[1])) + node[
                                                  2] + self.deadzone_heuristic(game, (s[0], s[1]), deadzones))

    def aStarReturn(self, game, midpoint):

        visited = []  # Visited list to prevent expanding a node multiple times.
        astar_priority_queue = util.PriorityQueue()
        astar_priority_queue.push((game.getAgentPosition(self.index), [], 0), 0)

        while not astar_priority_queue.isEmpty():
            node = astar_priority_queue.pop()
            current_position = node[0]
            path = node[1]
            if node[0][0] == midpoint:
                return path
            else:
                if current_position not in visited:
                    visited.append(current_position)
                    successors = []
                    x, y = node[0]
                    if not game.hasWall(x - 1, y) and (x - 1, y) not in visited:
                        successors.append((x - 1, y, 'West'))
                    if not game.hasWall(x + 1, y) and (x + 1, y) not in visited:
                        successors.append((x + 1, y, 'East'))
                    if not game.hasWall(x, y - 1) and (x, y - 1) not in visited:
                        successors.append((x, y - 1, 'South'))
                    if not game.hasWall(x, y + 1) and (x, y + 1) not in visited:
                        successors.append((x, y + 1, 'North'))
                    for s in successors:
                        path_history = []
                        path_history.extend(node[1])
                        path_history.extend([s[2]])
                        astar_priority_queue.push(((s[0], s[1]), path_history,
                                                   self.getMazeDistance(current_position, (s[0], s[1])) + node[2]),
                                                  self.getMazeDistance(current_position, (s[0], s[1])) + node[2])

    def breadthFirstSearch(self, game, start, goal):
        visited = []
        bfs_queue = util.Queue()
        bfs_queue.push((start, []))

        while not bfs_queue.isEmpty():
            node = bfs_queue.pop()
            if node[0] == goal:
                return True
            if node[0] not in visited:
                visited.append(node[0])
                successors = []
                x, y = node[0]
                if x > 0:
                    if game.hasWall(x - 1, y) and (x - 1, y) not in visited:
                        successors.append((x - 1, y, 'West'))
                if x < game.data.layout.width - 1:
                    if game.hasWall(x + 1, y) and (x + 1, y) not in visited:
                        successors.append((x + 1, y, 'East'))
                if y > 0:
                    if game.hasWall(x, y - 1) and (x, y - 1) not in visited:
                        successors.append((x, y - 1, 'South'))
                if y < game.data.layout.height - 1:
                    if game.hasWall(x, y + 1) and (x, y + 1) not in visited:
                        successors.append((x, y + 1, 'North'))
                for s in successors:
                    path_history = []
                    path_history.extend(node[1])
                    path_history.extend(s[2])
                    bfs_queue.push(((s[0], s[1]), path_history))
        return False

    def bfsHeuristicDZ(self, game, start, deadzones):

        visited = []
        bfs_queue = util.Queue()
        bfs_queue.push((start, [], 0))

        while not bfs_queue.isEmpty():
            node = bfs_queue.pop()
            if node[0] != start and node[0] not in deadzones:
                return node[2]
            if node[0] not in visited:
                visited.append(node[0])
                successors = []
                x, y = node[0]
                if not game.hasWall(x - 1, y) and (x - 1, y) not in visited:
                    successors.append((x - 1, y, 'West'))
                if not game.hasWall(x + 1, y) and (x + 1, y) not in visited:
                    successors.append((x + 1, y, 'East'))
                if not game.hasWall(x, y - 1) and (x, y - 1) not in visited:
                    successors.append((x, y - 1, 'South'))
                if not game.hasWall(x, y + 1) and (x, y + 1) not in visited:
                    successors.append((x, y + 1, 'North'))
                for s in successors:
                    path_history = []
                    path_history.extend(node[1])
                    path_history.extend(s[2])
                    bfs_queue.push(((s[0], s[1]), path_history,
                                    self.getMazeDistance(node[0], (s[0], s[1])) + node[2]))
        return 0

    def bfsHeuristicCP(self, game, start, outside_chokepoint):

        visited = []
        bfs_queue = util.Queue()
        bfs_queue.push((start, [], 0))

        while not bfs_queue.isEmpty():
            node = bfs_queue.pop()
            if node[0] == outside_chokepoint:
                return node[2]
            if node[0] not in visited:
                visited.append(node[0])
                successors = []
                x, y = node[0]
                if not game.hasWall(x - 1, y) and (x - 1, y) not in visited:
                    successors.append((x - 1, y, 'West'))
                if not game.hasWall(x + 1, y) and (x + 1, y) not in visited:
                    successors.append((x + 1, y, 'East'))
                if not game.hasWall(x, y - 1) and (x, y - 1) not in visited:
                    successors.append((x, y - 1, 'South'))
                if not game.hasWall(x, y + 1) and (x, y + 1) not in visited:
                    successors.append((x, y + 1, 'North'))
                for s in successors:
                    path_history = []
                    path_history.extend(node[1])
                    path_history.extend(s[2])
                    bfs_queue.push(((s[0], s[1]), path_history,
                                    self.getMazeDistance(node[0], (s[0], s[1])) + node[2]))
        return 0

    def deadends_and_chokepoints(self, game):
        deadends = []
        chokepoints = []
        # For each point that's not a wall.
        for x in range(game.data.layout.width):
            for y in range(game.data.layout.height):
                if not game.hasWall(x, y):
                    wall_count = 0
                    if game.hasWall(x - 1, y):
                        wall_count += 1
                    if game.hasWall(x + 1, y):
                        wall_count += 1
                    if game.hasWall(x, y - 1):
                        wall_count += 1
                    if game.hasWall(x, y + 1):
                        wall_count += 1
                    # If the point is surrounded by 3 walls, it's the start of a deadzone.
                    if wall_count == 3:
                        if (x, y) not in deadends:
                            deadends.append((x, y))
                        if not game.hasWall(x - 1, y):
                            x2 = -1
                            y2 = 0
                        elif not game.hasWall(x + 1, y):
                            x2 = 1
                            y2 = 0
                        elif not game.hasWall(x, y - 1):
                            x2 = 0
                            y2 = -1
                        elif not game.hasWall(x, y + 1):
                            x2 = 0
                            y2 = 1
                        num_open = 0
                        a = x
                        b = y
                        # In the direction out of the deadzone, add to the DZ until enough open space.
                        while num_open != 3:
                            a = a + x2
                            b = b + y2
                            point = (a, b)
                            w = 0
                            if game.hasWall(point[0], point[1]):
                                break
                            if not game.hasWall(point[0] + 1, point[1]):
                                w += 1
                            if not game.hasWall(point[0] - 1, point[1]):
                                w += 1
                            if not game.hasWall(point[0], point[1] + 1):
                                w += 1
                            if not game.hasWall(point[0], point[1] - 1):
                                w += 1
                            if w >= 3:
                                num_open = 3
                            else:
                                if point not in deadends and not game.hasWall(point[0], point[1]):
                                    deadends.append(point)
                if x != 0 and x != game.data.layout.width - 1 and y != 0 and y != game.data.layout.height - 1:
                    start = 0
                    end = 0
                    # If the point is the potential start of a chokepoint.
                    if game.hasWall(x, y + 1) and game.hasWall(x, y - 1):
                        start = (x, y + 1)
                        end = (x, y - 1)
                    elif game.hasWall(x - 1, y) and game.hasWall(x + 1, y):
                        start = (x - 1, y)
                        end = (x + 1, y)
                    if start != 0 and end != 0:
                        if not game.hasWall(x, y):
                            # Check for a path of walls that connects the position above and below the point.
                            if self.breadthFirstSearch(game, start, end) and x != 1 and x != 32:
                                chokepoints.append((x, y))
        chokepoints2 = []
        for cp in chokepoints:
            if cp not in deadends:
                chokepoints2.append(cp)
        return deadends, chokepoints2


class OffenseAgent(ParentAgent):

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)

        # Find deadends and chokepoints.
        self.deadends, self.chokepoints = self.deadends_and_chokepoints(gameState)

        # DEBUG: SHOW DEADENDS AND CHOKEPOINTS ON SCREEN
        for deadend in self.deadends:
            self.debugDraw(deadend, [1, 0, 0], clear=False)
        for chokepoint in self.chokepoints:
            self.debugDraw(chokepoint, [0, 1, 0], clear=False)

        # Set the midpoint depending on color.
        if self.red:
            self.midpoint = 16
            self.blue = False
        else:
            self.midpoint = 17
            self.blue = True

        self.inside_chokepoint = False
        self.outside_chokepoint = (-1, -1)

        self.food_to_eat = []
        for x in range(gameState.data.layout.width - 1):
            for y in range(gameState.data.layout.height - 1):
                if gameState.hasFood(x, y):
                    if x >= 17 and self.red:
                        self.food_to_eat.append((x, y))
                    if x <= 16 and self.blue:
                        self.food_to_eat.append((x, y))

        self.at_midpoint = False
        self.foodcount = 0

    def chooseAction(self, gameState):

        current_position = gameState.getAgentPosition(self.index)

        if current_position == (1, 1) or current_position == (1, 2) or current_position == (
        32, 16) or current_position == (32, 15):
            self.inside_chokepoint = False
            self.outside_chokepoint = (-1, -1)

        if self.inside_chokepoint:
            if current_position == self.outside_chokepoint:
                self.inside_chokepoint = False
                self.outside_chokepoint = (-1, -1)
                self.at_midpoint = False

        if current_position in self.chokepoints:
            if (self.red and current_position[0] >= 17) or (
                    self.blue and current_position[0] <= 16):
                if not self.inside_chokepoint:
                    self.inside_chokepoint = True
                    self.outside_chokepoint = gameState.getAgentPosition(self.index)

        self.food_to_eat = []
        self.food_costs = []
        self.camppoints = []
        for x in range(gameState.data.layout.width - 1):
            empty_points = []
            empty_count = 0
            for y in range(gameState.data.layout.height - 1):
                if gameState.hasFood(x, y):
                    if x >= 17 and self.red:
                        self.food_to_eat.append((x, y))
                        self.food_costs.append(self.getMazeDistance(gameState.getAgentPosition(self.index), (x, y)))
                    if x <= 16 and self.blue:
                        self.food_to_eat.append((x, y))
                        self.food_costs.append(self.getMazeDistance(gameState.getAgentPosition(self.index), (x, y)))
                if not gameState.hasWall(x, y):
                    empty_count += 1
                    empty_points.append((x, y))
            if empty_count == 2:
                self.camppoints.append((empty_points[0], empty_points[1]))
            elif empty_count == 1:
                self.camppoints.append(empty_points[0])
        self.sorted_food = [x for _,x in sorted(zip(self.food_costs, self.food_to_eat))]
        # self.debugDraw(self.sorted_food[0], [0, 0, 1], clear=False)


        # Get agent  x and y for easy access later.
        x, y = gameState.getAgentPosition(self.index)
        # Check if we're at the midpoint to move on to attacking.
        if x == self.midpoint:
            self.at_midpoint = True

        # Get enemy indices and positions.
        if self.red:
            enemy_indices = gameState.getBlueTeamIndices()
        elif self.blue:
            enemy_indices = gameState.getRedTeamIndices()
        enemy_positions = []
        for i in enemy_indices:
            enemy_positions.append(gameState.getAgentPosition(i))

        # If we're not at the midpoint and not chasing an enemy, go to the midpoint.
        if not self.at_midpoint and ((self.red and x <= 16) or (self.blue and x >= 17)):
            path = self.aStarReturn(gameState, self.midpoint)
            if path:
                direction = path[0]
                return direction
        else:
            food_checked = 0
            for food in self.sorted_food:
                if food_checked == 5:
                    break
                path, closest_pellet, cost = self.aStarEatHeuristic(gameState, food, self.deadends)
                enemy1_path, enemy1_cost = self.aStar(gameState, enemy_positions[0], closest_pellet)
                enemy2_path, enemy2_cost = self.aStar(gameState, enemy_positions[1], closest_pellet)
                # enemy1_distance = self.getMazeDistance(gameState.getAgentPosition(self.index), enemy_positions[0])
                # enemy2_distance = self.getMazeDistance(gameState.getAgentPosition(self.index), enemy_positions[1])
                # or (enemy1_distance > 2 and enemy2_distance > 2):
                if (cost < enemy1_cost) and (cost < enemy2_cost):
                    if path:
                        direction = path[0]
                        self.going_home = False
                        #self.debugDraw(food, [0, 0, 1], clear=True)
                        return direction
                food_checked += 1

            path = []
            # Set chasing enemy to false, in case we finished the chase. If we're still chasing it'll be set back later.
            if self.red:
                # If we're on our own side..
                if x <= 16:
                    # Set False so we return to the midpoint afterwards.
                    self.at_midpoint = False
                    # If an enemy is also on our side, go chase it since we're home.
                else:
                    # Return home if there's no pellet safe to eat or enemy
                    path = self.aStarReturn(gameState, self.midpoint)
            # Same logic but for blue team.
            elif self.blue:
                if x >= 17:
                    self.at_midpoint = False
                else:
                    path = self.aStarReturn(gameState, self.midpoint)

            # If we're trying to return home.
            if path:
                direction = path[0]
                if direction == 'North':
                    a = 0
                    b = 1
                elif direction == 'South':
                    a = 0
                    b = -1
                elif direction == 'East':
                    a = 1
                    b = 0
                elif direction == 'West':
                    a = -1
                    b = 0
                position = (x + a, y + b)
                if self.getMazeDistance(position, enemy_positions[0]) > 1 and self.getMazeDistance(position, enemy_positions[1]) > 1:
                    return direction
                else:
                    actions = []
                    # check for walls
                    escape_north = (x, y + 1)
                    if not gameState.hasWall(escape_north[0], escape_north[1]):
                        actions.append(("North", escape_north))
                    escape_south = (x, y - 1)
                    if not gameState.hasWall(escape_south[0], escape_south[1]):
                        actions.append(("South", escape_south))
                    escape_east = (x + 1, y)
                    if not gameState.hasWall(escape_east[0], escape_east[1]):
                        actions.append(("East", escape_east))
                    escape_west = (x - 1, y)
                    if not gameState.hasWall(escape_west[0], escape_west[1]):
                        actions.append(("West", escape_west))
                    if actions:
                        random.shuffle(actions)
                        for a in actions:
                            if self.getMazeDistance(a[1], enemy_positions[0]) > 1 and self.getMazeDistance(a[1], enemy_positions[1]) > 1:
                                if a[0] not in self.deadends:
                                    return a[0]

        actions = []
        repo_north = (x, y + 1)
        if not gameState.hasWall(repo_north[0], repo_north[1]):
            actions.append(("North", repo_north))
        repo_south = (x, y - 1)
        if not gameState.hasWall(repo_south[0], repo_south[1]):
            actions.append(("South", repo_south))
        repo_east = (x + 1, y)
        if not gameState.hasWall(repo_east[0], repo_east[1]):
            actions.append(("East", repo_east))
        repo_west = (x - 1, y)
        if not gameState.hasWall(repo_west[0], repo_west[1]):
            actions.append(("West", repo_west))
        if actions:
            random.shuffle(actions)
            for a in actions:
                if (self.red and a[1][0] <= 16) or (self.blue and a[1][0] >= 17):
                    return a[0]

        # Agent will stop if no other actions we're appropriate to take.
        return 'Stop'


class DefenseAgent(ParentAgent):

    def registerInitialState(self, gameState):

        CaptureAgent.registerInitialState(self, gameState)
        # Initialize here.

        if gameState.isOnRedTeam(self.index):
            self.midpoint = 16
        else:
            self.midpoint = 17

    def chooseAction(self, gameState):


        actions = gameState.getLegalActions(self.index)
        return 'Stop'
        # return random.choice(actions)

        collected_pellets = 0
        # game.getRedFood()[node[0][0]][node[0][1]]:
        x, y = gameState.getAgentPosition(self.index)
        if gameState.getAgentState(self.index).numCarrying == 5:
            path = self.aStarReturn(gameState, self.midpoint)
        else:
            path = self.aStarEat(gameState)
        if path:
            direction = path[0]
            return direction
        else:
            return random.choice(actions)
