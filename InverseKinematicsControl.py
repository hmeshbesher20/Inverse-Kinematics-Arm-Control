import RoboPiLib_pwm as RPL, math as m, time, stepper_control, sys, termios, tty

RPL.RoboPiInit("/dev/ttyAMA0",115200)

def set_pinMode(dir_pin1, dir_pin2): #you MUST set direction pins to OUTPUT: if you don't, the steppers will not change directions
  RPL.pinMode(6,RPL.OUTPUT)
  RPL.pinMode(2,RPL.OUTPUT)

def get_input():
  fd = sys .stdin.fileno() #sets a filepath for terminal reset
  old_settings = termios.tcgetattr(fd) #gets old terminal settings
  try:
    tty.setraw(fd)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) #returns input to normal settings; terminal can be used again after the program runs
  return ch

def apply_changes(char):
  global x, y
  increment = 1
  if char in ['w','a','s','d']:
    if char == 'w':
      y += increment
    elif char == 's':
      y -= increment
    elif char == 'd':
      x -= increment
    elif char == 'a':
      x += increment

  elif char == '*':
    quit()

def find_ang2(x,y,l1,l2):
    ang2 = pow(x, 2) + pow(y, 2) - pow(l1, 2) - pow(l2, 2)
    ang2 = ang2 / (2 * l1 * l2)
    ang2 = m.acos(ang2)
    return ang2

def find_ang1(x,y,l1,l2,ang2):
    ang1 = l2 * m.sin(ang2)
    ang1 = ang1 / (l1 + (l2 * m.cos(ang2)))
    ang1 = m.atan(ang1)
    ang1 = ang1 + m.atan(y / x)
    return ang1

def move(pul_pin, dir_pin, steps, speed): #speed is dependent on the microsteps you set the controller to: for the ideal speeds, see the Read_Me
  if steps < 0:
    RPL.digitalWrite(dir_pin,0)
  else:
    RPL.digitalWrite(dir_pin,1)
  for i in range(abs(steps)):