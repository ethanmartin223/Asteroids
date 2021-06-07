# ---------------#Imports#---------------#
import time, math, random
import keyboard
import tkinter as tk
from winsound import *
from pathlib import Path
# ---------------#window#---------------#
window = tk.Tk()
window.geometry('800x800')
window.minsize(width=800, height=800)
window.maxsize(width=800, height=800)
window.wm_attributes('-topmost', 'True')
'''path = Path("icon.ico") #Darn Exe screws this file so i removed it for install
icon = tk.PhotoImage(f'{path.absolute()}')
window.iconbitmap(icon)'''
window.title('Asteroids')
canvas = tk.Canvas(window, width=800, height=800, bg='black')
canvas.place(x=-2, y=0)
# ---------------#StartScreen#---------------#
sst = 0
def sst_toggle():
    global sst
    sst += 1
canvas.create_text(400, 300, text='Asteroids', font=('ISOCTEUR', 70), fill='white')
canvas.create_text(400, 400, text='The Classic Atari Game remade by Ethan and Trevor', font=('ISOCTEUR', 15),fill='white')
start_button = tk.Button(canvas, text='PLAY', bd=0, bg='black', fg='white', font=('ISOCTEUR', 30), command=sst_toggle)
start_button.place(x=325, y=500)
while True:
    if sst == 1:
        start_button.destroy()
        break
    window.update()
# ---------------#Globals#---------------#
score = 0
dev = False
pause_delay = 0
name = ''
global_speed = 1
sound = False
# ---------------#Classes#---------------#
class Ship:
    ship_angle = 0
    ship_move_angle = 0
    speed = 0
    x = 400
    y = 400
    slope_x = 0
    slope_y = 0
    lives = 5
    cool_down = 0
    end_x = 0
    end_y = 0
    end_x2 = 0
    end_y2 = 0
    end_x3 = 0
    end_y3 = 0
    end_x4 = 0
    end_y4 = 0
    end_x5 = 0
    end_y5 = 0
    end_x6 = 0
    end_y6 = 0
    tick = 0
    destroyed = False
    rotate_speed = 0
    velx = 0
    vely = 0
    thrusting = False
    def move(self):
        if self.destroyed:
            self.lives -= 1
            self.x = 400
            self.y = 400
            self.destroyed = False
        angle_in_radians = self.ship_angle * math.pi / 180
        line_length = 30
        center_x = self.x
        center_y = self.y
        self.end_x = center_x + line_length * math.cos(angle_in_radians)
        self.end_y = center_y + line_length * math.sin(angle_in_radians)
        angle_in_radians = (self.ship_angle + 130) * math.pi / 180
        line_length = 20
        self.end_x2 = center_x + line_length * math.cos(angle_in_radians)
        self.end_y2 = center_y + line_length * math.sin(angle_in_radians)
        angle_in_radians = (self.ship_angle - 130) * math.pi / 180
        line_length = 20
        self.end_x3 = center_x + line_length * math.cos(angle_in_radians)
        self.end_y3 = center_y + line_length * math.sin(angle_in_radians)
        canvas.create_line(self.end_x2, self.end_y2, self.end_x3, self.end_y3, fill='white', width=1)
        canvas.create_line(self.end_x3, self.end_y3, self.end_x, self.end_y, fill='white', width=1)
        canvas.create_line(self.end_x, self.end_y, self.end_x2, self.end_y2, fill='white', width=1)
        line_length = 30
        angle_in_radians = (self.ship_angle + 180) * math.pi / 180
        self.end_x4 = center_x + line_length * math.cos(angle_in_radians)
        self.end_y4 = center_y + line_length * math.sin(angle_in_radians)
        line_length = 18
        angle_in_radians = (self.ship_angle + 140) * math.pi / 180
        self.end_x5 = center_x + line_length * math.cos(angle_in_radians)
        self.end_y5 = center_y + line_length * math.sin(angle_in_radians)
        line_length = 18
        angle_in_radians = (self.ship_angle + 220) * math.pi / 180
        self.end_x6 = center_x + line_length * math.cos(angle_in_radians)
        self.end_y6 = center_y + line_length * math.sin(angle_in_radians)
        if self.thrusting and self.tick % 2 == 0:
            canvas.create_line(self.end_x4, self.end_y4, self.end_x6, self.end_y6, fill='orange', width=1)
            canvas.create_line(self.end_x4, self.end_y4, self.end_x5, self.end_y5, fill='orange', width=1)
        if self.thrusting and self.tick % 2 != 0:
            canvas.create_line(self.end_x4, self.end_y4, self.end_x6, self.end_y6, fill='red', width=1)
            canvas.create_line(self.end_x4, self.end_y4, self.end_x5, self.end_y5, fill='red', width=1)
        self.slope_y = int(self.end_y - center_y)
        self.slope_x = int(self.end_x - center_x)
        if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
            if self.rotate_speed > -2.5:
                self.rotate_speed -= .1
        if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
            if self.rotate_speed < 2.5:
                self.rotate_speed += .1
        if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
            if self.speed < .04:
                self.speed += .001
            self.thrusting = True
            self.tick += 1
        else:
            self.thrusting = False
        if (keyboard.is_pressed('s') and self.cool_down <= 1) or (keyboard.is_pressed('down') and self.cool_down <= 1):
            self.x = random.randint(0,800)
            self.y = random.randint(0,800)
            self.cool_down = 120
        if self.speed < .0001:
            self.speed = 0
            self.velx = 0
            self.vely = 0
        if self.speed != 0:
            self.velx += self.speed * math.cos(self.ship_angle * math.pi / 180)
            self.vely += self.speed * math.sin(self.ship_angle * math.pi / 180)
            self.velx *= .99
            self.vely *= .99
            self.x += self.velx
            self.y += self.vely
        if self.speed > 0:
            self.speed -= .0002
        self.ship_angle += self.rotate_speed
        if self.rotate_speed > 0:
            self.rotate_speed -= .02
        if self.rotate_speed < 0:
            self.rotate_speed += .02
        if self.x > 810:
            self.x = -10
        if self.x < -10:
            self.x = 810
        if self.y > 810:
            self.y = -10
        if self.y < -10:
            self.y = 810
        if self.cool_down > 1:
            self.cool_down -=1
class Asteroid:
    x = 0
    y = 0
    slope = (0, 0)
    asteroid_angle = 0
    bullet_distance = 0
    bullet_distance2 = 0
    ship_distance = 0
    destroyed = False
    type = 3
    need_to_set = True
    test = True
    temp1 = 0
    temp2 = 0
    temp3 = 0
    temp4 = 0
    temp5 = 0
    temp6 = 0
    test2 = True
    test3 = True
    def __init__(self):
        self.x = random.randint(0, 800)
        while abs(self.x - ship.x) < 60:
            self.x = random.randint(0, 800)
        self.y = random.randint(0, 800)
        while abs(self.y - ship.y) < 60:
            self.y = random.randint(0, 800)
        self.slope = (*random.sample((-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1), 1),
                      *random.sample((-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1), 1))
    def move(self):
        global dev, global_speed,score,sound
        if self.destroyed:
            if self.test:
                self.temp2 = SmallAsteroid()
                self.temp1 = SmallAsteroid()
                self.temp2.x = self.x
                self.temp2.y = self.y
                self.temp1.x = self.x
                self.temp1.y = self.y
                self.temp1.type = 2
                self.temp2.type = 2
                self.test = False
            else:
                if not self.temp1.destroyed:
                    self.temp1.move()
                if self.temp1.destroyed and self.test2:
                    self.temp3 = SmallAsteroid()
                    self.temp4 = SmallAsteroid()
                    self.temp3.x = self.temp1.x
                    self.temp4.x = self.temp1.x
                    self.temp3.y = self.temp1.y
                    self.temp4.y = self.temp1.y
                    self.temp3.type = 1
                    self.temp4.type = 1
                    self.test2 = False
                if not self.temp2.destroyed:
                    self.temp2.move()
                if self.temp2.destroyed and self.test3:
                    self.temp5 = SmallAsteroid()
                    self.temp6 = SmallAsteroid()
                    self.temp5.x = self.temp2.x
                    self.temp6.x = self.temp2.x
                    self.temp5.y = self.temp2.y
                    self.temp6.y = self.temp2.y
                    self.temp6.type = 1
                    self.temp5.type = 1
                    self.test3 = False
                if self.temp1.destroyed:
                    if not self.temp3.destroyed and self.temp3 != 0: self.temp3.move()
                    if not self.temp4.destroyed and self.temp4 != 0: self.temp4.move()
                if self.temp2.destroyed:
                    if not self.temp5.destroyed and self.temp5 != 0: self.temp5.move()
                    if not self.temp6.destroyed and self.temp6 != 0: self.temp6.move()
        elif not self.destroyed:
            self.asteroid_angle += 1
            self.x += self.slope[0]*global_speed
            self.y += self.slope[1]*global_speed
            if self.x > 800:
                self.x = 0
            elif self.x < 0:
                self.x = 800
            elif self.y > 800:
                self.y = 0
            elif self.y < 0:
                self.y = 800
            locations = (0, 60, 120, 180, 240, 300, 0)
            if self.type == 3:
                lengths = (60, 60, 60, 60, 60, 60, 60)
            elif self.type == 2:
                lengths = (40, 40, 40, 40, 40, 40, 40)
            elif self.type == 1:
                lengths = (20, 20, 20, 20, 20, 20, 20)
            else:
                lengths = (0, 0, 0, 0, 0, 0, 0)
            points = []
            for l, v in enumerate(lengths):
                center_x = int(self.x)
                center_y = int(self.y)
                angle_in_radians = (self.asteroid_angle + locations[l]) * math.pi / 180
                line_length = v
                end_x = center_x + line_length * math.cos(angle_in_radians)
                end_y = center_y + line_length * math.sin(angle_in_radians)
                points.append([end_x, end_y])
                canvas.create_line(points[l][0], points[l][1], points[l - 1][0], points[l - 1][1], fill='white',
                                   width=1)
                self.bullet_distance = math.sqrt(
                    abs(bullet.bullet_x - self.x) ** 2 + abs(bullet.bullet_y - self.y) ** 2)
                self.bullet_distance2 = math.sqrt(
                    abs(bullet.bullet2_x - self.x) ** 2 + abs(bullet.bullet2_y - self.y) ** 2)
                self.ship_distance = math.sqrt(abs(ship.end_x - self.x) ** 2 + abs(ship.end_y - self.y) ** 2)
                if self.ship_distance < lengths[0] and not dev:
                    ship.destroyed = True
                self.ship_distance = math.sqrt(abs(ship.end_x2 - self.x) ** 2 + abs(ship.end_y2 - self.y) ** 2)
                if self.ship_distance < lengths[0] and not dev:
                    ship.destroyed = True
                self.ship_distance = math.sqrt(abs(ship.end_x3 - self.x) ** 2 + abs(ship.end_y3 - self.y) ** 2)
                if self.ship_distance < lengths[0] and not dev:
                    ship.destroyed = True
                if self.bullet_distance < lengths[0]:
                    bullet.currently_fired = False
                    bullet.bullet_x = -80
                    bullet.bullet_y = -80
                    score += 25
                    self.destroyed = True
                    if sound:
                        PlaySound('boom.wav', SND_FILENAME | SND_ASYNC)
                        '''if self.type == 3:
                            PlaySound('bangLarge.wav', SND_FILENAME | SND_ASYNC)
                        if self.type == 2:
                            PlaySound('bangMedium.wav', SND_FILENAME | SND_ASYNC)
                        if self.type == 1:
                            PlaySound('bangSmall.wav', SND_FILENAME | SND_ASYNC)'''
                if self.bullet_distance2 < lengths[0]:
                    bullet.currently_fired2 = False
                    bullet.bullet2_x = -80
                    bullet.bullet2_y = -80
                    score += 25
                    self.destroyed = True
                    if sound:
                        PlaySound('boom.wav', SND_FILENAME | SND_ASYNC)
                        '''if self.type == 3:
                            PlaySound('bangLarge.wav', SND_FILENAME | SND_ASYNC)
                        if self.type == 2:
                            PlaySound('bangMedium.wav', SND_FILENAME | SND_ASYNC)
                        if self.type == 1:
                            PlaySound('bangSmall.wav', SND_FILENAME | SND_ASYNC)'''
class SmallAsteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.slope = (*random.sample((-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1), 1),
                      *random.sample((-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1), 1))
class Bullet:
    bullet_slope = 0
    bullet_angle = 0
    bullet_slope2 = 0
    bullet_angle2 = 0
    bullet_x = -80
    bullet_y = -80
    bullet2_x = -80
    bullet2_y = -80
    currently_fired = 0
    currently_fired2 = 0
    delay = 0
    def move(self):
        global sound
        if self.delay > 0:
            self.delay -=1
        if keyboard.is_pressed('space') and not self.currently_fired:
            if sound:
                PlaySound('fire_trevor.wav',SND_FILENAME | SND_ASYNC)
            self.bullet_slope = (ship.slope_x, ship.slope_y)
            self.bullet_angle = ship.ship_angle
            self.bullet_x = ship.x + ship.slope_x
            self.bullet_y = ship.y + ship.slope_y
            self.currently_fired = True
            self.delay = 50
        elif keyboard.is_pressed('space') and not self.currently_fired2:
            if self.delay < 2:
                if sound:
                    PlaySound('fire_trevor.wav',SND_FILENAME | SND_ASYNC)
                self.bullet_slope2 = (ship.slope_x, ship.slope_y)
                self.bullet_angle2 = ship.ship_angle
                self.bullet2_x = ship.x + ship.slope_x
                self.bullet2_y = ship.y + ship.slope_y
                self.currently_fired2 = True
        if self.currently_fired:
            center_x = self.bullet_x
            center_y = self.bullet_y
            angle_in_radians = self.bullet_angle * math.pi / 180
            line_length = 5
            end_x = center_x + line_length * math.cos(angle_in_radians)
            end_y = center_y + line_length * math.sin(angle_in_radians)
            self.bullet_y += (self.bullet_slope[1]) // 4
            self.bullet_x += (self.bullet_slope[0]) // 4
            if self.bullet_x > 810:
                self.currently_fired = False
                self.bullet_x = -80
                self.bullet_y = -80
            if self.bullet_x < -10:
                self.currently_fired = False
                self.bullet_x = -80
                self.bullet_y = -80
            if self.bullet_y > 810:
                self.currently_fired = False
                self.bullet_x = -80
                self.bullet_y = -80
            if self.bullet_y < -80:
                self.currently_fired = False
                self.bullet_x = -80
                self.bullet_y = -80
            canvas.create_line(center_x, center_y, end_x, end_y, fill='white', width=5)
        if self.currently_fired2:
            center_x = self.bullet2_x
            center_y = self.bullet2_y
            angle_in_radians = self.bullet_angle2 * math.pi / 180
            line_length = 5
            end_x = center_x + line_length * math.cos(angle_in_radians)
            end_y = center_y + line_length * math.sin(angle_in_radians)
            self.bullet2_y += (self.bullet_slope2[1]) // 4
            self.bullet2_x += (self.bullet_slope2[0]) // 4
            if self.bullet2_x > 810:
                self.currently_fired2 = False
                self.bullet2_x = -80
                self.bullet2_y = -80
            if self.bullet2_x < -10:
                self.currently_fired2 = False
                self.bullet2_x = -80
                self.bullet2_y = -80
            if self.bullet2_y > 810:
                self.currently_fired2 = False
                self.bullet2_x = -80
                self.bullet2_y = -80
            if self.bullet2_y < -80:
                self.currently_fired2 = False
                self.bullet2_x = -80
                self.bullet2_y = -80
            canvas.create_line(center_x, center_y, end_x, end_y, fill='white', width=5)
class UFO:
    x = 0
    y = 0
    spawned = False
    bullet_slope = 0
    bullet_angle = 0
    bullet_x = -80
    bullet_y = -80
    currently_fired = 0
    duration = 0
    direction = 0
    target_distance = 0
    center_dist = 0
    right_dist = 0
    left_dist = 0
    def __init___(self):
        self.x = 0
        self.y = random.randint(0, 800)
        self.spawned = False

    def move(self):
        global global_speed,score
        det = random.randint(0, 800)
        if not self.spawned:
            self.y = random.randint(0, 800)
            self.x = 0
        if det == 1:
            self.spawned = True
        if self.spawned:
            if self.duration <= 0:
                self.direction = int(random.choice([-1, 0, 1]))
                self.duration = random.randint(20, 100)
            self.y += self.direction
            self.duration -= 1
            self.x += 1
            self.center_dist = math.sqrt(abs(bullet.bullet_x - self.x) ** 2 + abs(bullet.bullet_y - self.y) ** 2)
            self.right_dist = math.sqrt(abs(bullet.bullet_x - self.x + 20) ** 2 + abs(bullet.bullet_y - self.y + 20) ** 2)
            self.left_dist = math.sqrt(abs(bullet.bullet_x - self.x - 20) ** 2 + abs(bullet.bullet_y - self.y - 20) ** 2)
            if self.center_dist < 20:
                self.spawned = False
                bullet.currently_fired = False
                score += 250
            elif self.right_dist < 15:
                self.spawned = False
                bullet.currently_fired = False
                score += 250
            elif self.left_dist < 15:
                self.spawned = False
                bullet.currently_fired = False
                score += 250
            self.center_dist = math.sqrt(abs(bullet.bullet2_x - self.x) ** 2 + abs(bullet.bullet2_y - self.y) ** 2)
            self.right_dist = math.sqrt(abs(bullet.bullet2_x - self.x + 20) ** 2 + abs(bullet.bullet2_y - self.y + 20) ** 2)
            self.left_dist = math.sqrt(abs(bullet.bullet2_x - self.x - 20) ** 2 + abs(bullet.bullet2_y - self.y - 20) ** 2)
            if self.center_dist < 20:
                self.spawned = False
                bullet.currently_fired2 = False
                score += 250
            elif self.right_dist < 15:
                self.spawned = False
                bullet.currently_fired2 = False
                score += 250
            elif self.left_dist < 15:
                self.spawned = False
                bullet.currently_fired2 = False
                score+=250
            if self.x > 820:
                self.x = -20
            if self.x < -20:
                self.x = 820
            if self.y > 820:
                self.y = -20
            if self.y < -20:
                self.y = 820
            if not self.currently_fired:
                self.target_distance = math.sqrt(abs(ship.x - self.x) ** 2 + abs(ship.y - self.y) ** 2)
                self.bullet_slope = (ship.x - self.x, ship.y - self.y)
                self.bullet_angle = math.atan(self.bullet_slope[1] / self.bullet_slope[0])
                self.bullet_x = self.x
                self.bullet_y = self.y
                self.currently_fired = True
            elif self.currently_fired:
                bullet_distance = math.sqrt(abs(ship.x - self.bullet_x) ** 2 + abs(ship.y - self.bullet_y) ** 2)
                center_x = self.bullet_x
                center_y = self.bullet_y
                angle_in_radians = self.bullet_angle * math.pi / 180
                line_length = 5
                end_x = center_x + line_length * math.cos(angle_in_radians)
                end_y = center_y + line_length * math.sin(angle_in_radians)
                self.bullet_y += ((self.bullet_slope[1])/(self.target_distance/5-global_speed))
                self.bullet_x += ((self.bullet_slope[0])/(self.target_distance/5-global_speed))
                if bullet_distance < 20:
                    ship.destroyed = True
                    self.currently_fired = False
                if self.bullet_x > 810:
                    self.currently_fired = False
                    self.bullet_x = -80
                    self.bullet_y = -80
                if self.bullet_x < -10:
                    self.currently_fired = False
                    self.bullet_x = -80
                    self.bullet_y = -80
                if self.bullet_y > 810:
                    self.currently_fired = False
                    self.bullet_x = -80
                    self.bullet_y = -80
                if self.bullet_y < -80:
                    self.currently_fired = False
                    self.bullet_x = -80
                    self.bullet_y = -80
                canvas.create_line(center_x, center_y, end_x, end_y, fill='white', width=5)
            canvas.create_line(self.x - 30, self.y - 10, self.x + 30, self.y - 10, fill='white', width=1)
            canvas.create_line(self.x - 30, self.y - 10, self.x - 40, self.y, fill='white', width=1)
            canvas.create_line(self.x + 30, self.y - 10, self.x + 40, self.y, fill='white', width=1)
            canvas.create_line(self.x - 30, self.y + 10, self.x - 40, self.y, fill='white', width=1)
            canvas.create_line(self.x + 30, self.y + 10, self.x + 40, self.y, fill='white', width=1)
            canvas.create_line(self.x - 30, self.y + 10, self.x + 30, self.y + 10, fill='white', width=1)
            canvas.create_line(self.x - 30, self.y - 10, self.x - 40, self.y, fill='white', width=1)
            canvas.create_line(self.x - 10, self.y - 20, self.x + 10, self.y - 20, fill='white', width=1)
            canvas.create_line(self.x - 10, self.y - 20, self.x - 20, self.y - 10, fill='white', width=1)
            canvas.create_line(self.x - 10, self.y - 20, self.x - 20, self.y - 10, fill='white', width=1)
            canvas.create_line(self.x + 10, self.y - 20, self.x + 20, self.y - 10, fill='white', width=1)
            canvas.create_line(self.x + 20, self.y + 10, self.x + 10, self.y + 15, fill='white', width=1)
            canvas.create_line(self.x - 20, self.y + 10, self.x - 10, self.y + 15, fill='white', width=1)
            canvas.create_line(self.x + 10, self.y + 15, self.x - 10, self.y + 15, fill='white', width=1)
# ---------------#Objects#---------------#
ship = Ship()
a = Asteroid()
b = Asteroid()
c = Asteroid()
e = Asteroid()
f = Asteroid()
g = Asteroid()
ufo = UFO()
ufo.__init___()
bullet = Bullet()
#----------------#CheckAll#----------------#
def are_asteroids_left(instance):
    error = 0
    if not instance.destroyed:
        error += 1
    if instance.temp1 != 0:
        if not instance.temp1.destroyed:
            error +=1
    if instance.temp2 != 0:
        if not instance.temp2.destroyed:
            error +=1
    if instance.temp3 != 0:
        if not instance.temp3.destroyed:
            error +=1
    if instance.temp4 != 0:
        if not instance.temp4.destroyed:
            error +=1
    if instance.temp5 != 0:
        if not instance.temp5.destroyed:
            error +=1
    if instance.temp6 != 0:
        if not instance.temp6.destroyed:
            error +=1
    if error == 0:
        return True
    else:
        return False
# ---------------#Game Loop# --------------#
while True:
    while True:
        canvas.create_text(70, 50, text=(str('0' * (5 - len(str(score))))) + str(score), fill='white',
                           font=('ISOCTEUR', 25))
        m = 25
        for i in range(ship.lives):
            canvas.create_text(m, 20, text='A', fill='white', font=('ISOCTEUR', 25))
            m += 25
        if ship.lives == 0:
            break
        ufo.move()
        a.move()
        b.move()
        c.move()
        e.move()
        bullet.move()
        ship.move()
        if are_asteroids_left(a) and are_asteroids_left(b) and are_asteroids_left(c) and are_asteroids_left(e):
            a = Asteroid()
            b = Asteroid()
            c = Asteroid()
            e = Asteroid()
            global_speed += .1
        window.update()
        time.sleep(0.001)
        canvas.delete('all')
    # ---------------#Death#---------------#
    canvas.delete('all')
    if ship.lives == 0:
        defult_text =[['---', 0], ['---', 0], ['---', 0], ['---', 0], ['---', 0]]
        try:
            high_scores = open('high_score.py', 'r')
        except FileNotFoundError:
            high_scores = open('high_score.py', 'w')
            high_scores.write('scores = ' + str(defult_text))
            high_scores.close()
            high_scores = open('high_score.py', 'r')
        finally:
            high_scores.close()
        import high_score

        temp = high_score.scores

        def get_value(value):
            return value[1]

        temp.sort(key=get_value, reverse=True)
        for i, v in enumerate(temp):
            if v[1] < score:
                def get_entry():
                    global entry,name
                    name = entry.get()

                entry = tk.Entry(bg='#0a0a0a', bd=0, fg='white', width=15,font=('ISOCTEUR',40))
                text = tk.Label(bg='#000000',text='You got a Highscore!\n Enter your name to continue:', bd=0, fg='white', font=('ISOCTEUR', 25))
                text.place(x=50,y=300)
                entry.place(x=80, y=400)
                accept = tk.Button(bg='#0a0a0a', bd=0, fg='white',font=('ISOCTEUR',25),text='ENTER',command=get_entry)
                accept.place(x=580,y=400)
                name = ''
                while True:
                    window.update()
                    if keyboard.is_pressed('enter'):
                        get_entry()
                        break
                    if name != '':
                        break
                entry.destroy()
                accept.destroy()
                text.destroy()
                temp.insert(i, [name, score])
                temp.sort(key=get_value, reverse=True)
                if len(temp) > 5:
                    del temp[5]
                break
        high_score = open('high_score.py', 'w')
        high_score.write('scores = ' + str(temp))
        high_score.close()
        import high_score
        temp_data = high_score.scores
        canvas.delete('all')
        canvas.create_text(400, 120, text='GAME OVER', font=('ISOCTEUR', 70), fill='white')
        canvas.create_text(400, 200, text=f'Your Final Score is {score}', font=('ISOCTEUR', 20), fill='white')
        canvas.create_text(400, 300, text='Highscores', font=('ISOCTEUR', 40), fill='white')
        table = f'''
            1. {temp_data[0][0]}-{temp_data[0][1]}
            2. {temp_data[1][0]}-{temp_data[1][1]}
            3. {temp_data[2][0]}-{temp_data[2][1]}
            4. {temp_data[3][0]}-{temp_data[3][1]}
            5. {temp_data[4][0]}-{temp_data[4][1]}'''
        canvas.create_text(180, 500, text=table, font=('ISOCTEUR', 40), fill='white')
    flag = False
    def toggle():
        global flag
        flag = True
    accept = tk.Button(bg='#000000', bd=0, fg='white', font=('ISOCTEUR', 30), text='PLAY AGAIN', command=toggle)
    accept.place(x=250, y=700)
    while True:
        window.update()
        if flag:
            score = 0
            ship = Ship()
            a = Asteroid()
            b = Asteroid()
            c = Asteroid()
            e = Asteroid()
            f = Asteroid()
            g = Asteroid()
            ufo = UFO()
            ufo.__init___()
            flag = False
            accept.destroy()
            break
