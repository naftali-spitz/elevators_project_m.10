import pygame
from queue import Queue

class MyBuildingElevators:
    
    def __init__(self, floors, num_elevators):
        self.building_floors = []
        self.elevators = []
        
        
        for floor in floors:
            self.building_floors[floor] = Floor.__init__(floor)
            
        for elv in num_elevators:
            self.elevators[elv] = Elevator.__init__(elv)
        
        pygame.init()
        color1 = [255, 255, 255]
        box_len = 800
        box_hight = 600
        screen = pygame.display.set_mode((box_len, box_hight))
        screen.fill(color1)
        pygame.display.flip()
        pygame.display.set_caption("ELOVATOR PROJECT")
        exit = False

        while not exit: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    exit = True
            pygame.display.update() 
        

class Elevator:
    
    def __init__(self, number_of_elevators):
        self.elevator = (0, 0)
        # initiate elevators
        # 1 elevator image
        # 2 
    
    def __elevator__(self, floor):
        calls.Queue = []
        self.call = calls.Queue.insert()
        self.time_avalibility = 


class Floor:  
          
    def __init__(self, floor_num):
            # initiate floor
            # 1 floor rect with backround
            # 2 level num
            # 3 control panel
            # (4 countdown elv arrival)
        self.floor_num = floor_num
        
    def __floor__(self, floor_num):
        
class elv_call(self, des_floor):
    
    elevator_avillability = [] * len(MyBuildingElevators.elevators)
    for elevator in elevators:
        time_avalebility = 
        if elevator.avalebility > 0:
            elevator_avillability[elevator] += 2
    
    return elevator_avillability.index(min(elevator_avillability))