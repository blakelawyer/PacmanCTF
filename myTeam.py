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
               first='OffenseAgent', second='OffenseAgent'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


class ParentAgent(CaptureAgent):

    def getMazeDistance(self, pos1, pos2):
        d = self.distancer.getDistance(pos1, pos2)
        return d

    def deadzone_heuristic(self, game, point, deadzones):
        if point in deadzones:
            cost = self.bfsHeuristic(game, point, deadzones)
            return cost
        else:
            return 0

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

    def aStarEat(self, game):

        visited = []  # Visited list to prevent expanding a node multiple times.
        astar_priority_queue = util.PriorityQueue()
        astar_priority_queue.push((game.getAgentPosition(self.index), [], 0), 0)

        while not astar_priority_queue.isEmpty():
            node = astar_priority_queue.pop()
            current_position = node[0]
            path = node[1]
            cost = node[2]
            if self.red:
                if game.getBlueFood()[node[0][0]][node[0][1]]:
                    return path, (node[0][0], node[0][1]), cost
            elif self.blue:
                if game.getRedFood()[node[0][0]][node[0][1]]:
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
                                                   2] + self.deadzone_heuristic(game, (s[0], s[1]), self.deadends)),
                                              self.getMazeDistance(current_position, (s[0], s[1])) + node[
                                                  2] + self.deadzone_heuristic(game, (s[0], s[1]), self.deadends))

        # deadzone heuristic:

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
                if x < 33:
                    if game.hasWall(x + 1, y) and (x + 1, y) not in visited:
                        successors.append((x + 1, y, 'East'))
                if y > 0:
                    if game.hasWall(x, y - 1) and (x, y - 1) not in visited:
                        successors.append((x, y - 1, 'South'))
                if y < 17:
                    if game.hasWall(x, y + 1) and (x, y + 1) not in visited:
                        successors.append((x, y + 1, 'North'))
                for s in successors:
                    path_history = []
                    path_history.extend(node[1])
                    path_history.extend(s[2])
                    bfs_queue.push(((s[0], s[1]), path_history))
        return False

    def bfsHeuristic(self, game, start, deadzones):
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

    def deadends_and_chokepoints(self, game):
        deadends = []
        chokepoints = []
        # For each point that's not a wall.
        for x in range(33):
            for y in range(17):
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
                if x != 0 and x != 33 and y != 0 and y != 17:
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

        if self.red:
            self.midpoint = 16
            self.blue = False
        else:
            self.midpoint = 17
            self.blue = True

        self.at_midpoint = False
        self.chasing_enemy = False
        self.going_home = False
        self.foodcount = 0

    def chooseAction(self, gameState):

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
        if not self.at_midpoint and not self.chasing_enemy:
            path = self.aStarReturn(gameState, self.midpoint)
            if path:
                direction = path[0]
                return direction
        else:
            # Otherwise, get the path the the closest pellet, and the enemies' path the the same pellet.
            path, closest_pellet, cost = self.aStarEat(gameState)
            enemy1_path, enemy1_cost = self.aStar(gameState, enemy_positions[0], closest_pellet)
            enemy2_path, enemy2_cost = self.aStar(gameState, enemy_positions[1], closest_pellet)
            enemy1_distance = self.getMazeDistance(gameState.getAgentPosition(self.index), enemy_positions[0])
            enemy2_distance = self.getMazeDistance(gameState.getAgentPosition(self.index), enemy_positions[1])

            # if (len(path) < len(enemy1_path)) and (len(path) < len(enemy2_path)) and not self.chasing_enemy:
            print(cost, enemy1_cost, enemy2_cost)
            # If we can make it to the pellet before the enemy, and we're not currently chasing, return that direction.
            if (cost < enemy1_cost) and (cost < enemy2_cost) and not self.chasing_enemy or (
                    enemy1_distance > 5 and enemy2_distance > 5):
                if path:
                    direction = path[0]
                    self.going_home = False
                    return direction

            # Set chasing enemy to false, in case we finished the chase. If we're still chasing it'll be set back later.
            self.chasing_enemy = False
            if self.red:
                # If we're on our own side..
                if x <= 16:
                    # Set False so we return to the midpoint afterwards.
                    self.at_midpoint = False
                    # If an enemy is also on our side, go chase it since we're home.
                    for enemy in enemy_positions:
                        if enemy[0] <= 16:
                            path = self.aStar(gameState, gameState.getAgentPosition(self.index), enemy)[0]
                            self.chasing_enemy = True
                            self.going_home = False
                            if path:
                                direction = path[0]
                                return direction
                else:
                    # Return home if there's no pellet safe to eat or enemy
                    path = self.aStarReturn(gameState, self.midpoint)
                    self.going_home = True
                    if path:
                        direction = path[0]
                        return direction
            # Same logic but for blue team.
            elif self.blue:
                if x >= 17:
                    self.at_midpoint = False
                    for enemy in enemy_positions:
                        if enemy[0] >= 17:
                            path = self.aStar(gameState, gameState.getAgentPosition(self.index), enemy)[0]
                            self.chasing_enemy = True
                            self.going_home = False
                            if path:
                                direction = path[0]
                                return direction
                else:
                    path = self.aStarReturn(gameState, self.midpoint)
                    self.going_home = True
                    if path:
                        direction = path[0]
                        return direction
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
