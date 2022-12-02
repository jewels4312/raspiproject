import time
import RPi.GPIO as GPIO



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
    
    def wave(self, i, size=3):
        total_lights = self.total_lights() + (size + 5)
        start_index = i % total_lights - (size + 5)
        
        for i in range(len(self.__lights)):
            if i < start_index:
                self.__lights[i].setToggle(False)
                continue;
            elif i > start_index + size:
                self.__lights[i].setToggle(False)
            elif i >= start_index:
                self.__lights[i].setToggle(True)
        
                
    
        
        

def main():
    
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)    
    
    lights = LightBoard()
    
    # Lights in order.
    
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
    
    i = 0
    
    while True:
        time.sleep(0.1)
        i += 1 
        lights.wave(i) 
        # lights.toggle_all() # 

        
    
    
            
        
if __name__ == "__main__":
    main()


