import time, random
import RPi.GPIO as GPIO
from pynput import keyboard
import pygame


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
    __slots__ = ['__score', '__scoreRequired','__playerPos','__startTime', '__currentTime', '__endTime', '__timeAllowed', '__hasEnded', '__coinPos', '__lights', '__win']        
    
    def __init__(self, timeAllowed, scoreRequired, lights):
        self.__score = 0
        self.__scoreRequired = scoreRequired
        self.__startTime = time.perf_counter()
        self.__timeAllowed = timeAllowed
        self.__lights = lights
        self.__playerPos = 0
        self.__coinPos = 4 + random.randint(1,3)
        self.__hasEnded = False
        
        self.__lights.toggle_at(self.__coinPos, True)
        self.__lights.toggle_at(self.__playerPos, True)
        pygame.mixer.init()
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.__run_event()
        if self.__win:
            my_sound = pygame.mixer.Sound('audio/smb_stage_clear.wav')
            my_sound.play()
            print("\n\n\n\n\nYou won the game!")
            print(f"Time elapsed: {str(((self.__endTime - self.__startTime) // .01 )/ 100)}s")
            i = 0
            while i < 300:
                time.sleep(0.02)
                i+=1
                self.__lights.wave(i)
            self.__lights.toggle_all_to(False)
        else:
            my_sound = pygame.mixer.Sound('audio/smb_mariodie.wav')
            my_sound.play()
            print("You lost! :(")
            print(f"You collected {str(self.__score)}/25 coins in {str(((self.__endTime - self.__startTime) // .01 )/ 100)}s")
        
    def __createCoin(self):
        if self.__lights.totalActive() >= 1:
            return
        
        while True:
            coin_pos = random.randint(0, self.__lights.total_lights())
            if self.__lights.is_toggled(coin_pos):
                continue
            else:
                self.__lights.toggle_at(coin_pos, True)
                break
                
    def __printBoard(self):
        string = f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nTime elapsed: {str(((self.__currentTime - self.__startTime) // .01 )/ 100)}s / 60s"
        #for i in range(len(self.__lights.get_lights())):
        #    if self.__lights.get_lights()[i].is_toggled():
        #        string += "\u25a0 "
        #        if self.__playerPos == i:
        #            string2 += "P "
        #        elif self.__coinPos == i:
        #            string2 += "C "
        #        else:
        #            pass
        #    else:
        #        string += "_ "
        #        string2 += "  "
        print(string)
        
            
        
    def __input(self):
        pass
        
    def get_current_time(self):
        return self.__currentTime
        
    def hasCompleted(self):
        return self.__hasEnded
    
    def __run_event(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        return False
    
    def on_press(self, key):
        
        # Handle the player movement
        self.__currentTime = time.perf_counter()
        self.__lights.toggle_at(self.__playerPos, False)
        if key == keyboard.Key.right:
            if self.__playerPos == self.__lights.total_lights() - 1:
                self.__lights.toggle_at(self.__playerPos, True)
                pass
            else:
                self.__playerPos += 1
                self.__lights.toggle_at(self.__playerPos, True)

        elif key == keyboard.Key.left:
            if self.__playerPos == 0:
                self.__lights.toggle_at(self.__playerPos, True)
                pass
            else:
                self.__playerPos -= 1
                self.__lights.toggle_at(self.__playerPos, True)
        else:
            self.__lights.toggle_at(self.__playerPos, True)

        # Check if the player is at coin position.
        
        if self.__playerPos == self.__coinPos:
            self.__lights.toggle_at(self.__playerPos, True)
            my_sound = pygame.mixer.Sound('audio/smw_coin.wav')
            my_sound.play()
            pygame.time.wait(int((my_sound.get_length() * 1000)/2))
            if self.__coinPos < 3:
                self.__coinPos = 4 + random.randint(1,3)
            elif self.__coinPos > 3:
                self.__coinPos = random.randint(0,2)
            self.__lights.toggle_at(self.__coinPos, True)
            self.__score += 1
            
            if time.perf_counter() - self.__startTime > self.__timeAllowed:
                self.__endTime = time.perf_counter()
                self.__win = False
                # play lose sound
                return False
            
            if self.__score == self.__scoreRequired:
                self.__win = True
                # play win sound
                self.__endTime = time.perf_counter()
                return False
            
        self.__printBoard()
            #self.__time = 0

    def on_release(self, key):
        self.__printBoard()
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
    #game = Game(10, lights)
    
    time_allowed = int(input("\n\n\n\n\n\n\n\n\n\n\n\n\n\nHow many seconds to you want to play? (enter 0 for default settings)"))
    if time_allowed == 0:
        game = Game(30, 25, lights)
    else:
        score_required = int(input("How many coins will you attempt to collect?")) 
        game = Game(time_allowed, score_required, lights)
            
if __name__ == "__main__":
    main()


