from graphics import *
import tkinter as tk
from tkinter import simpledialog, messagebox
from win32api import GetSystemMetrics
import math
import time

# Function to prompt the user for a positive integer
def InputIntegerL(message):
    ROOT = tk.Tk()
    ROOT.withdraw()  # Hide the main Tkinter window
    ROOT.attributes("-topmost", True)  # Ensure it's always on top
    while True:
        try:
            user_input = simpledialog.askstring(title="Input", prompt=message, parent=ROOT)
            if user_input is None:
                messagebox.showinfo('Info', 'Operation Cancelled', parent=ROOT)
                return None
            value = int(user_input)
            if value > 0:
                return value
            else:
                messagebox.showerror("Invalid Input", "Please enter a positive integer.", parent=ROOT)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.", parent=ROOT)

#Function to prompt the user for an integer input without positivity constraints
def InputInteger(message):
    ROOT = tk.Tk()
    ROOT.withdraw()  # Hide the main Tkinter window
    ROOT.attributes("-topmost", True)  # Ensure it's always on top
    while True:
        try:
            user_input = simpledialog.askstring(title="Input", prompt=message, parent=ROOT)
            if user_input is None:
                messagebox.showinfo('Info', 'Operation Cancelled', parent=ROOT)
                return None
            else:
                return int(user_input)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.", parent=ROOT)

#Function to draw a line on the graphics window
def DrawLine(x1, y1, x2, y2, win, width, color):
    line = Line(Point(x1, y1), Point(x2, y2))
    line.setWidth(width)
    line.setFill(color)
    line.draw(win)
    
#Function to draw a circle with specified parametres
def DrawCircle(x, y, radius, win, width, color, color2):
    circle = Circle(Point(x, y), radius)
    circle.setWidth(width)
    circle.setOutline(color)
    circle.setFill(color2)
    circle.draw(win)

#Function to draw the possible solutions for arm's joint positions
def Calculations(x2, y2):
    e = 0.0001 #Small tolerance to avoid division by zero
    c = (y2**2 + x2**2 + L1**2 - L2**2) / 2
    d = 4 * c**2 * y2**2 - 4 * (x2**2 + y2**2) * (c**2 - L1**2 * x2**2)

    if abs(x2) < e:
        ya1 = c / y2
        ya2 = ya1
        xa1 = math.sqrt(L1**2 - (c**2 / y2**2))
        xa2 = -xa1
    else:
        ya1 = (2 * c * y2 + math.sqrt(d)) / (2 * (x2**2 + y2**2))
        ya2 = (2 * c * y2 - math.sqrt(d)) / (2 * (x2**2 + y2**2))
        xa1 = (c - y2 * ya1) / x2
        xa2 = (c - y2 * ya2) / x2
    return xa1, ya1, xa2, ya2

#Function to check if the target point is within the robot's workspace
def Limit(x2, y2):
    distance = math.sqrt(x2**2 + y2**2)
    return abs(L1 - L2) <= distance <= (L1 + L2)

# Function to determine if a move is possible between two points
def Possible(nx, ny, x2, y2, L1, L2):
    e = 0.001 #Small tolerance to avoid division by zero
    dx = nx - x2
    dy = ny - y2
    if dx == 0:
        dx = e
    a = dy / dx
    b = y2 - (a * x2)
    d = 4 * (a**2) * (b**2) - 4 * (a**2 + 1) * (b**2 - ((L1 - L2)**2))
    if d < 0:
        return True
    elif d > 0:
        
        xs1 = ((-2*a*b) + math.sqrt(d)) / (2*((a**2)+1))
        xs2 = ((-2*a*b) - math.sqrt(d)) / (2*((a**2)+1))

        ys1 = a*xs1 + b 
        ys2 = a*xs2 + b 
            
        Dp0p1 = math.sqrt(((ny- y2)**2) + ((nx-x2)**2))
        Dp0s1 = math.sqrt(((ys1- y2)**2) + ((xs1-x2)**2))
        Dp0s2 = math.sqrt(((ys2- y2)**2) + ((xs2-x2)**2))
        Dp1s1 = math.sqrt(((ys1- ny)**2) + ((xs1-nx)**2))
        Dp1s2 = math.sqrt(((ys2- ny)**2) + ((xs2-nx)**2))

        Dmin0 = min(Dp0s1,Dp0s2)
        Dmin1 = min(Dp1s1,Dp1s2)
        Dmax = max(Dmin0,Dmin1)
            
        if Dmax > Dp0p1:
            return True        
        else:
            messagebox.showerror('Movement is not possible')
            return False
    
    else:
        if abs(x2)>=abs(L1-L2):
            return True
        else:
            xs1 = ((-2*a*b) + math.sqrt(d)) / (2*((a**2)+1))
            xs2 = ((-2*a*b) - math.sqrt(d)) / (2*((a**2)+1))

            ys1 = math.sqrt(((L1-L2)**2)-(xs1**2))
            ys2 = -math.sqrt(((L1-L2)**2)-(xs2**2))
            
            Dp0p1 = math.sqrt(((ny- y2)**2) + ((nx-x2)**2))
            Dp0s1 = math.sqrt(((ys1- y2)**2) + ((xs1-x2)**2))
            Dp0s2 = math.sqrt(((ys2- y2)**2) + ((xs2-x2)**2))
            Dp1s1 = math.sqrt(((ys1- ny)**2) + ((xs1-nx)**2))
            Dp1s2 = math.sqrt(((ys2- ny)**2) + ((xs2-nx)**2))

            Dmin0 = min(Dp0s1,Dp0s2)
            Dmin1 = min(Dp1s1,Dp1s2)
            Dmax = max(Dmin0,Dmin1)

            if Dmax > Dp0p1:
                return True
            else:
                messagebox.showerror('Movement is not possible')
                return False


# Function to calculate the angle (in radians) based on Cartesian coordinates
def atan2(x,y):
    if x == 0: 
        if y > 0:
            f = 90
        if y < 0:
            f = 270
    else:
        if x > 0:
            if y >= 0:
                f = math.atan(y/x)
            else:
                f = math.atan(y/x)+2*math.pi
        if x < 0:
                f = math.atan(y/x)+math.pi
    return f

# Function to get a valid solution for the joint positions
def GetSolution(x2, y2):
    xa1, ya1, xa2, ya2 = Calculations(x2, y2)
    f1 = atan2(xa1, ya1)
    tangent_x = (x2 - xa1) * math.cos(f1) + (y2 - ya1) * math.sin(f1)
    tangent_y = -(x2 - xa1) * math.sin(f1) + (y2 - ya1) * math.cos(f1)
    f2 = atan2(tangent_x, tangent_y)
    if LR:
        if f2 <= math.pi:
            return xa1, ya1
        else:
            return xa2, ya2
    else:
        if f2 >= math.pi:
            return xa1, ya1
        else:
            return xa2, ya2


# Function to redraw (update and refresh) the workspace boundaries and axes, to be the graphical display up to date with current configuration
def RedrawWorkspace():
    DrawCircle(x_center, y_center, L1 + L2, win, 2, 'blue', 'white')  # Outer workspace boundary
    DrawCircle(x_center, y_center, abs(L1 - L2), win, 2, 'blue', 'yellow')  # Inner workspace boundary
    DrawLine(ScreenWidth * 0.05, ScreenHeight / 2, ScreenWidth * 0.95, ScreenHeight / 2, win, 2, 'green')  # Horizontal axis
    DrawLine(ScreenWidth / 2, ScreenHeight * 0.05, ScreenWidth / 2, ScreenHeight * 0.95, win, 2, 'green')  # Vertical axis



# Function to draw or clear the robot arm
def DrawRobotArm(x2, y2, MyColorArm, MycolorOfElbow, clear=False):
    if Limit(x2, y2):
        x1, y1 = GetSolution(x2, y2)
        x2_screen = x_center + x2
        y2_screen = y_center - y2
        x1_screen = x_center + x1
        y1_screen = y_center - y1

        if clear:
            arm_color = 'white'
        else:
            arm_color = MyColorArm

        if clear:
            elbow_color = 'white'
        else:
            elbow_color = MycolorOfElbow


        # Draw or clear the robot arm
        DrawLine(x_center, y_center, x1_screen, y1_screen, win, 2, arm_color)
        DrawCircle(x1_screen, y1_screen, 3, win, 2, elbow_color, 'white')
        DrawLine(x1_screen, y1_screen, x2_screen, y2_screen, win, 2, arm_color)
        DrawCircle(x2_screen, y2_screen, 3, win, 2, elbow_color, 'white')

        # Redraw workspace boundaries and axes after clearing
        if clear:
            RedrawWorkspace()

# Function to animate the movement of the robot arm to a new position
def AnimateNewRobotArm(nx, ny, MyColorArm, MycolorOfElbow):
    global x2, y2
    if Possible(nx, ny, x2, y2, L1, L2):
        # Clear the previous black arm and red line
        DrawRobotArm(x2, y2, MyColorArm, MycolorOfElbow, clear=True)

        Duration = 0.5  # Duration of the animation in seconds
        Rate = 30  
        Steps = int(Duration * Rate)
        DelaySec = 1 / Rate

        for i in range(1, Steps + 1):
            xp = float((nx - x2) * i / Steps + x2)
            yp = float((ny - y2) * i / Steps + y2)

            # Draw and clear the arm during animation
            DrawRobotArm(xp, yp, MyColorArm, MycolorOfElbow)  # Draw the current arm
            time.sleep(DelaySec)
            if i != Steps:
                DrawRobotArm(xp, yp, MyColorArm, MycolorOfElbow, clear=True)  # Clear the current arm

        # Draw movement line and update position, when I insert invalid values, draws the wrong arm
        DrawLine(x_center + x2, y_center - y2, x_center + nx, y_center - ny, win, 2, 'white')  # Clear red line
        DrawLine(x_center + x2, y_center - y2, x_center + nx, y_center - ny, win, 2, 'white')
        x2, y2 = nx, ny

ScreenWidth = GetSystemMetrics(0) * 0.85
ScreenHeight = GetSystemMetrics(1) * 0.85

L1 = InputIntegerL('Enter the length of the first arm (L1):')
L2 = InputIntegerL('Enter the length of the second arm (L2):')
x2 = InputInteger('Enter the x-coordinate of the target:')
y2 = InputInteger('Enter the y-coordinate of the target:')

while not ((L1 + L2) < ScreenWidth / 4 and (L1 + L2) < ScreenHeight / 2 and math.sqrt(x2**2 + y2**2) <= L1 + L2):
    messagebox.showerror('Error', 'Invalid input. Ensure:\n1. L1 + L2 is less than half of the screen dimensions.\n2.')
    L1 = InputIntegerL("Enter the length of the first arm (L1):")
    L2 = InputIntegerL("Enter the length of the second arm (L2):")
    x2 = InputInteger("Enter the x-coordinate:")
    y2 = InputInteger("Enter the y-coordinate:")

#Ask if we want the anti-clockwise solution for the arm configuration
result = messagebox.askyesno("Attention", "Do you want the anti-clockwise solution?")
if result == True:
    LR = True
else:
    LR = False

win = GraphWin("Inverse Kinematics", ScreenWidth, ScreenHeight)
win.setBackground('white')
x_center = ScreenWidth / 2
y_center = ScreenHeight / 2

#Draw the workspace boundaries and axis
DrawCircle(x_center, y_center, L1 + L2, win, 2, 'blue','white')
DrawLine(ScreenWidth * 0.05, ScreenHeight / 2, ScreenWidth * 0.95, ScreenHeight / 2, win, 2, 'green')
DrawLine(ScreenWidth / 2, ScreenHeight * 0.05, ScreenWidth / 2, ScreenHeight * 0.95, win, 2, 'green')
DrawCircle(x_center, y_center, abs(L1 - L2), win, 2, 'blue', 'yellow')

x1, y1 = GetSolution(x2, y2)
DrawRobotArm(x2, y2, 'black', 'red')

while True:
    result = messagebox.askyesno("Move", "Do you want to move to another point?")
    if not result:
        break
    nx = InputInteger("Enter the x-coordinate of the new point:")
    ny = InputInteger("Enter the y-coordinate of the new point:")
    
    # Ensure the new point is within the workspace
    while not Limit(nx, ny):
        messagebox.showerror('Error', 'The point is not within the workspace.')
        nx = InputInteger("Enter the x-coordinate of the new point:")
        ny = InputInteger("Enter the y-coordinate of the new point:")
    AnimateNewRobotArm(nx, ny, 'black', 'red')

    # Draw the robot arm in its new position
    DrawRobotArm(nx, ny, 'black', 'red')

win.getMouse()
win.close()
