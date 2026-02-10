import math
import random

import pygame
import itertools


def getDistance(spot1, spot2):
    # Given two coordinates in a plane return the distance between those two points.
    dist = math.sqrt((spot1[0] - spot2[0]) ** 2 + (spot2[1] - spot2[1]) ** 2)
    return dist


def getPathDistance(places: list):
    # Given a list of x,y coordinates return the distance it would take to go to each coordinate
    # in order and then back to the start.
    dist = 0
    indices = range(0, len(places) - 1)  # last index is covered in second to last iteration
    for i in indices:
        current_cords = places[i]
        next_cords = places[i + 1]
        dist += getDistance(current_cords, next_cords)  # find the distance to the next point, and add it
    dist += getDistance(places[0],places[-1]) # go back to the start node
    return dist


def increment_full_tsp(path: list):
    last_index = len(path) - 1
    path[last_index - 1] += 1  # increment second to last index, last is always 0
    rev_indices = range(last_index - 1, 0,
                        -1)  # starts at high goes to every number from high before -1, decrementing by one every time
    # does not have to handle the 0th index, as if that is too high, it signifies all permutations have been incremented through
    cap = 0
    for i in rev_indices:  # carry the one, repeatedly
        if path[i] > cap:  # eg; last is 0, second last is 1, etc
            path[i] = 0
            path[i - 1] += 1
        else:  # no 1 to be carried
            # if there is a 1 that needs to be carried further up in the list, other than the 0th index, there has been a logic error
            break  # nothing else needs to be carred over, so increment complete
        cap += 1


def full_TSP(places: list):
    # Check the distance of all possible different paths one could take over a set of x,y coordiantes
    # and return the path with the shortest distance
    # Print out the number of distance calculations you had to do.
    calculations = 0
    best_path = []
    for place in places:
        best_path.append(place)
    current_nodes = []
    last_place_index = len(places) - 1
    for i in places:
        current_nodes.append(0)  # first index of remaining nodes, always 0
    while current_nodes[0] <= last_place_index:  # until all permutations have been completed
        calculations += 1
        all_places = places.copy()
        current_path = []
        for node in current_nodes:
            # print(f"node in current_nodes = \'{node}\', current nodes = \'{current_nodes}\', remaining_places = \'{all_places}\'\n")
            place = all_places.pop(node)
            # print(f"place = \'{place}\', remaining_places = \'{all_places}\'\n")
            current_path.append(place)
            # print(f"current path = \'{current_path}\'")
        # print(f"current_path = {current_path},  best_path = {best_path}\n\n")
        current_path_dist = getPathDistance(current_path)
        best_path_dist = getPathDistance(best_path)
        # print(f"current path distance = \'{current_path_dist}\', best route distance\'{best_path_dist}\'")
        if current_path_dist < best_path_dist:
            best_path = current_path
        increment_full_tsp(current_nodes)
    print(f"there were {calculations} calculations for full TSP")
    return best_path

def find_closest_index(place, list: list):
    closest = 0
    for i in range(1, len(list)):
        if getDistance(place, list[i]) < getDistance(list[closest]):
            closest = i
    return i

def heuristic_TSP(places: list):

    # off by one error somewhere
    # first node picked twice
    # last node ignored (offset by one due to first node * 2, never recovers)

    # Perform a heuristic calculation for traveling salesman.
    # For each node find the closest node to it and assume it is next node then repeat until you have your path.
    # Return the path. and print out the number of distance calculations you did.
    calculations = 0
    current_path = [places[0]]
    mut_places = places.copy()
    for i in range(1, len(places)): # starts at node 0
        # closest_node = 0  # 0 is assumed to be closest, and compared against
        # for node in range(1, len(mut_places)): # each iteration until something better is found, or it proves to be closest
        #     place = mut_places[node]
        last_place = current_path[len(current_path) - 1]
        #     print(f"place: \'{place}\', last_place = \'{last_place}\'")
        #     dist = getDistance(place, last_place)
        #     calculations += 1
        #     if dist < getDistance(last_place, mut_places[closest_node]):
        #         # if node is the new closest node
        #         closest_node = node
        closest_node = find_closest_index(last_place, mut_places)
        current_path.append(mut_places.pop(closest_node))
    print(f"there were {calculations} calculations for heuristic TSP")
    return current_path


def generatePermutations(places: list):
    # a function that given a list will return all possible permutations of the list.
    return list(itertools.permutations(places))


def generate_RandomCoordinates(n):
    # Creates a list of random coordinates
    newPlaces = []
    for i in range(n):
        newPlaces.append([random.randint(10, 790), random.randint(10, 590)])
    return newPlaces


places = [[80, 75], [100, 520], [530, 300], [280, 200], [350, 150], [700, 120], [400, 500]]


def DrawExample(places):
    # Draws the TSP showcase to the screen.
    TSP = full_TSP(places.copy())
    heuristic = heuristic_TSP(places.copy())
    # Initialize Pygame
    pygame.init()
    print(TSP)
    print(heuristic)
    # Set up the game window
    screen = pygame.display.set_mode((800, 800))
    # Game loop
    running = True
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    text_surface = font.render('Hello, Pygame!', True, (0, 0, 0))
    text_surface.set_colorkey((0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (300, 700)  # Center the text on the screen
    # Arguments: text string, antialias boolean (True for smooth edges), text color, optional background color
    text_surface = font.render('Hello, Pygame!', True, (255, 255, 255))  # White text
    while running:
        screen.fill((255, 255, 255))
        for i in range(len(TSP) - 1):
            pygame.draw.line(screen, (255, 0, 0), (TSP[i][0], TSP[i][1]), (TSP[i + 1][0], TSP[i + 1][1]), width=8)
        if len(TSP) >= 1: pygame.draw.line(screen, (255, 0, 0), (TSP[0][0], TSP[0][1]), (TSP[-1][0], TSP[-1][1]),
                                           width=8)
        for i in range(len(heuristic) - 1):
            pygame.draw.line(screen, (0, 0, 255), (heuristic[i][0], heuristic[i][1]),
                             (heuristic[i + 1][0], heuristic[i + 1][1]), width=4)
        if len(heuristic) >= 1: pygame.draw.line(screen, (0, 0, 255), (heuristic[0][0], heuristic[0][1]),
                                                 (heuristic[-1][0], heuristic[-1][1]), width=4)
        for spot in places:
            pygame.draw.circle(screen, (0, 0, 0), (spot[0], spot[1]), 10)
        text_surface = font.render('Red is full TSP Blue is Heuristic', True, (0, 0, 0))
        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    # Quit Pygame


# DrawExample(places)
# # DrawExample(generate_RandomCoordinates(11))# DO NOT run more than 9 or 10
# pygame.quit()