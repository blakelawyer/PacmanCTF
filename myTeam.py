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

    def aStar(self, game, start, goal):

        visited = []  # Visited list to prevent expanding a node multiple times.
        astar_priority_queue = util.PriorityQueue()
        astar_priority_queue.push((start, [], 0), 0)

        while not astar_priority_queue.isEmpty():
            node = astar_priority_queue.pop()
            current_position = node[0]
            path = node[1]
            if current_position == goal:
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
                        if (s[0], s[1]) not in visited:
                            path_history = []
                            path_history.extend(node[1])
                            path_history.extend([s[2]])
                            astar_priority_queue.push(((s[0], s[1]), path_history,
                                                       self.getMazeDistance(current_position, (s[0], s[1]))),
                                                      self.getMazeDistance(current_position, (s[0], s[1])))


    def aStarEat(self, game):

        visited = []  # Visited list to prevent expanding a node multiple times.
        astar_priority_queue = util.PriorityQueue()
        astar_priority_queue.push((game.getAgentPosition(self.index), [], 0), 0)

        while not astar_priority_queue.isEmpty():
            node = astar_priority_queue.pop()
            current_position = node[0]
            path = node[1]
            if self.red:
                if game.getBlueFood()[node[0][0]][node[0][1]]:
                    return path, (node[0][0], node[0][1])
            elif self.blue:
                if game.getRedFood()[node[0][0]][node[0][1]]:
                    return path, (node[0][0], node[0][1])
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
                    if (s[0], s[1]) not in visited:
                        path_history = []
                        path_history.extend(node[1])
                        path_history.extend([s[2]])
                        astar_priority_queue.push(((s[0], s[1]), path_history,
                                                   self.getMazeDistance(current_position, (s[0], s[1]))),
                                                  self.getMazeDistance(current_position, (s[0], s[1])))


    def aStarReturn(self, game, midpoint):

        visited = []  # Visited list to prevent expanding a node multiple times.
        astar_priority_queue = util.PriorityQueue()
        astar_priority_queue.push((game.getAgentPosition(self.index), [], 0), 0)

        while not astar_priority_queue.isEmpty():
            node = astar_priority_queue.pop()
            current_position = node[0]
            path = node[1]
            # if current_position == goal:
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
                        if (s[0], s[1]) not in visited:
                            path_history = []
                            path_history.extend(node[1])
                            path_history.extend([s[2]])
                            astar_priority_queue.push(((s[0], s[1]), path_history,
                                                       self.getMazeDistance(current_position, (s[0], s[1]))),
                                                      self.getMazeDistance(current_position, (s[0], s[1])))


class OffenseAgent(ParentAgent):

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)

        if gameState.isOnRedTeam(self.index):
            self.midpoint = 16
            self.red = True
            self.blue = False
        else:
            self.midpoint = 17
            self.red = False
            self.blue = True

        self.at_midpoint = False
        self.chasing_enemy = False
        self.going_home = False

    def chooseAction(self, gameState):

        x, y = gameState.getAgentPosition(self.index)
        if x == self.midpoint:
            self.at_midpoint = True

        if self.red:
            enemy_indices = gameState.getBlueTeamIndices()
        elif self.blue:
            enemy_indices = gameState.getRedTeamIndices()
        enemy_positions = []
        for i in enemy_indices:
            enemy_positions.append(gameState.getAgentPosition(i))


        if not self.at_midpoint and not self.chasing_enemy:
            path = self.aStarReturn(gameState, self.midpoint)
            if path:
                direction = path[0]
                return direction
        else:
            path, closest_pellet = self.aStarEat(gameState)
            enemy1_path = self.aStar(gameState, enemy_positions[0], closest_pellet)
            enemy2_path = self.aStar(gameState, enemy_positions[1], closest_pellet)
            if (len(path) < len(enemy1_path)) and (len(path) < len(enemy2_path)) and not self.chasing_enemy:
                if path:
                    direction = path[0]
                    print("Going for pellet!")
                    self.going_home = False
                    return direction

            self.chasing_enemy = False
            if self.red:
                if x <= 16:
                    self.at_midpoint = False
                    for enemy in enemy_positions:
                        if enemy[0] <= 16:
                            path = self.aStar(gameState, gameState.getAgentPosition(self.index), enemy)
                            print("Going for enemy!")
                            self.chasing_enemy = True
                            self.going_home = False
                            if path:
                                direction = path[0]
                                return direction
                else:
                    path = self.aStarReturn(gameState, self.midpoint)
                    print("Going for home!")
                    self.going_home = True
                    if path:
                        direction = path[0]
                        return direction
            elif self.blue:
                if x >= 17:
                    self.at_midpoint = False
                    for enemy in enemy_positions:
                        if enemy[0] >= 17:
                            path = self.aStar(gameState, gameState.getAgentPosition(self.index), enemy)
                            print("Going for enemy!")
                            self.chasing_enemy = True
                            self.going_home = False
                            if path:
                                direction = path[0]
                                return direction
                else:
                    path = self.aStarReturn(gameState, self.midpoint)
                    print("Going for home!")
                    self.going_home = True
                    if path:
                        direction = path[0]
                        return direction

        print("Stopping!")
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
