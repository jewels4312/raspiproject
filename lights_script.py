import time, random
import RPi.GPIO as GPIO
import pynput, playsound


class Light:
    __slots__ = ['__color', '__toggled', '__boardPos']
    
    def __init__(self, color, boardPos):
        GPIO.setup(boardPos, GPIO.OUT)
        self.__color = color
        self.__toggled = False
        self.__boardPos = boardPos
        
    def __repr__(self):
        return f"{self.get_color()} ({str(self.get_board_position())}) Toggled: {str(self.is_toggled())}"
        
    def get_color(self):
        return self.__color
    
    def is_toggled(self):
        return self.__toggled
    
    def get_board_position(self):
        return self.__boardPos
    
    def toggle(self):
        if self.__toggled:
            self.setToggle(False)
        else:
            self.setToggle(True)
    
    def setToggle(self, toggle):
        self.__toggled = toggle
        GPIO.output(self.__boardPos, toggle)
        
class LightBoard:
    __slots__ = ['__lights']
    
    def __init__(self):
        self.__lights = []
        
    def add_light(self, light):
        self.__lights.append(light)
        
    def get_lights(self):
        return self.__lights
        
    def toggle_light(self, color):
        for light in self.__lights:
            if light.get_color() == color:
                light.toggle()
    
    def total_lights(self):
        return len(self.__lights)
    
    def view_lights(self):
        for light in self.__lights:
            print(repr(light))
            
    def toggle_all(self):
        for light in self.__lights:
            light.toggle()
    
    def toggle_all_to(self, toggle):
        for light in self.__lights:
            light.setToggle(toggle)
    
    def is_toggled(self, index):
        if index < 0 or index > len(self.__lights) - 1:
            return False
        else:
            return self.__lights[index].is_toggled()
    
    def toggle_at(self, index, toggle):
        if index < 0 or index > len(self.__lights) - 1:
            return False
        else:
            self.__lights[index].setToggle(toggle)
    
    
    def totalActive(self):
        count = 0
        for i in range(len(self.__lights)):
            if self.__lights[i].is_toggled():
                count += 1
        return count
    
    def wave(self, i, size=3):
        total_lights = self.total_lights() + (size + 5)
        start_index = i % total_lights - (size + 5)
        
        for i in range(len(self.__lights)):
            if i < start_index:
                self.__lights[i].setToggle(False)
                continue
            elif i > start_index + size:
                self.__lights[i].setToggle(False)
            elif i >= start_index:
                self.__lights[i].setToggle(True)
        
                
class Game:
    __slots__ = ['__hits', '__misses', '__startTime', '__endTime', '__timeAllowed', '__currentTime', '__hasEnded', '__moles']        
    
    def __init__(self, timeAllowed, lights):
        self.__hits = 0
        self.__misses = 0
        self.__startTime = time.perf_counter
        self.__timeAllowed = timeAllowed
        self.__currentTime = timeAllowed
        self.__hasEnded = False
        self.__moles = lights
    
    def runGame(self):
        if self.__hasEnded:
            raise Exception("Cannot run game that has ended")
        
        time.sleep(.05)
        self.__currentTime -= .05
        
        self.__spawnMoleEvent()
        
        self.__printMoles()
        
        if self.__currentTime < 0:
            self.__hasEnded = True
            self.__endTime = time.perf_counter
            print("Game completed!")
        
    def __createMole(self):
        
        if self.__moles.totalActive() >= 3:
            return
        
        while True:
            mole_pos = random.randint(0, self.__moles.total_lights())
            if self.__moles.is_toggled(mole_pos):
                continue
            else:
                self.__moles.toggle_at(mole_pos, True)
                break
                
    def __printMoles(self):
        string = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        for mole in self.__moles.get_lights():
            if mole.is_toggled():
                
                string += "■ "
            else:
                string += "_ "
        print(string)
            
        
    def __input(self):
        pass
        
    def get_current_time(self):
        return self.__currentTime
        
    def hasCompleted(self):
        return self.__hasEnded
    
    def __spawnMoleEvent(self): # When player inputs
        chance = random.randint(1, 100)
        if chance < 8:
            self.__createMole()
        pass
        
        
def lights_setup(lights):
    l1 = Light('red', 18)
    l2 = Light('yellow', 23)
    l3 = Light('blue', 24)
    l4 = Light('green', 25)
    
    l5 = Light('red', 12)
    l6 = Light('yellow', 16)
    l7 = Light('blue', 20)
    l8 = Light('green', 21)
    #l9 = Light('red', 16)
    
    # Add lights in correct order.
    
    lights.add_light(l1)
    lights.add_light(l2)
    lights.add_light(l3)
    lights.add_light(l4)
    
    lights.add_light(l5)
    lights.add_light(l6)
    lights.add_light(l7)
    lights.add_light(l8)
        

def main():
    
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)    
    
    lights = LightBoard()
    
    # Lights in order.
    lights_setup(lights)
    
    lights.toggle_all_to(False)
    
    game = Game(10, lights)
    
    
    i = 0
    
    playsound.playsound('./audio/shovel-thwack-1-94135.mp3')
    
    while not game.hasCompleted():
        game.runGame()
        print("Current Time: " + str(game.get_current_time()))
        # lights.toggle_all() # 

        
    
    
            
        
if __name__ == "__main__":
    main()


