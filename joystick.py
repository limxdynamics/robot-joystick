import os
# Hide the Pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import math
import limxsdk.robot as robot
import limxsdk.datatypes as datatypes

# Initialize Pygame
pygame.init()

# Set window size and colors
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_ACTIVE_COLOR = (255, 100, 100)
D_PAD_COLOR = (100, 100, 100)
D_PAD_ACTIVE_COLOR = (255, 100, 100)

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("RobotJoystick")

# Set window icon
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Define button and joystick positions
BUTTON_WIDTH, BUTTON_HEIGHT = 50, 50

# Define buttons' rectangles
buttons = {
    "Y": pygame.Rect(580, 410, BUTTON_WIDTH, BUTTON_HEIGHT),
    "A": pygame.Rect(580, 510, BUTTON_WIDTH, BUTTON_HEIGHT),
    "X": pygame.Rect(530, 460, BUTTON_WIDTH, BUTTON_HEIGHT),
    "B": pygame.Rect(630, 460, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Define L1 and L2 buttons' rectangles
l1_l2 = {
    "L1": pygame.Rect(128, 110, BUTTON_WIDTH, BUTTON_HEIGHT),
    "L2": pygame.Rect(218, 110, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Define R1 and R2 buttons' rectangles
r1_r2 = {
    "R1": pygame.Rect(530, 110, BUTTON_WIDTH, BUTTON_HEIGHT),
    "R2": pygame.Rect(620, 110, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Define D-Pad buttons' rectangles
dpad = {
    "up": pygame.Rect(170, 410, BUTTON_WIDTH, BUTTON_HEIGHT),
    "down": pygame.Rect(170, 510, BUTTON_WIDTH, BUTTON_HEIGHT),
    "left": pygame.Rect(120, 460, BUTTON_WIDTH, BUTTON_HEIGHT),
    "right": pygame.Rect(220, 460, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Define joystick positions and sizes
joysticks = {
    "left": (200, 280, 100),
    "right": (600, 280, 100),
}

# State records for joystick and buttons
joystick_values = {'left': (0, 0), 'right': (0, 0)}
dpad_states = {key: 0 for key in dpad.keys()}
dragging_joystick = {'left': False, 'right': False}
button_states = {**{key: 0 for key in buttons.keys()},
                 **{key: 0 for key in l1_l2.keys()},
                 **{key: 0 for key in r1_r2.keys()}}

# Instructions text
font = pygame.font.SysFont(None, 24)
key_prompts = [
    "Key Bindings:",
    "D-Pad: W (Up), S (Down), A (Left), D (Right)",
    "Left Joystick: Arrow Keys",
    "Right Joystick: Numpad 8/5/4/6",
    "Y: I",
    "A: K",
    "X: J",
    "B: L",
    "L1: Q",
    "L2: E",
    "R1: I",
    "R2: O"
]

# Function to draw buttons
def draw_buttons():
    for button, rect in buttons.items():
        color = BUTTON_ACTIVE_COLOR if button_states[button] else BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = font.render(button, True, (0, 0, 0))
        screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))

# Function to draw L1 and L2 buttons
def draw_l1_l2():
    for button, rect in l1_l2.items():
        color = BUTTON_ACTIVE_COLOR if button_states.get(button, False) else BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = font.render(button, True, (0, 0, 0))
        screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))

# Function to draw R1 and R2 buttons
def draw_r1_r2():
    for button, rect in r1_r2.items():
        color = BUTTON_ACTIVE_COLOR if button_states.get(button, False) else BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = font.render(button, True, (0, 0, 0))
        screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))

# Function to draw D-Pad
def draw_dpad():
    for direction, rect in dpad.items():
        color = D_PAD_ACTIVE_COLOR if dpad_states[direction] else D_PAD_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        direction_surface = font.render(direction.capitalize(), True, (0, 0, 0))
        screen.blit(direction_surface, (rect.x + (rect.width - direction_surface.get_width()) // 2, rect.y + (rect.height - direction_surface.get_height()) // 2))

# Function to draw joystick
def draw_joystick(center, radius, value):
    pygame.draw.circle(screen, (100, 100, 100), center, radius, 8)
    x = center[0] + value[0] * radius * 0.8
    y = center[1] + value[1] * radius * 0.8
    pygame.draw.circle(screen, (255, 100, 100), (int(x), int(y)), 40)

# Function to draw key prompts
def draw_key_prompts():
    for i, line in enumerate(key_prompts):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + i * 20))

# Initialize the joystick connection
robot_joystick = robot.Joystick("127.0.0.1")

# Main loop flag
running = True

while running:
    # Fill the screen with the background color
    screen.fill(BACKGROUND_COLOR)

    # Process events from the event queue
    for event in pygame.event.get():
        # Check if the quit event has been triggered
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse button down events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
            
            # Check if any buttons were clicked
            for button in buttons:
                if buttons[button].collidepoint(mouse_pos):
                    button_states[button] = 1  # Set button state to pressed
            
            # Check if any D-Pad directions were clicked
            for direction in dpad:
                if dpad[direction].collidepoint(mouse_pos):
                    dpad_states[direction] = 1  # Set D-Pad direction to pressed
            
            # Check if any joystick was clicked
            for joystick in joysticks:
                joystick_center = (joysticks[joystick][0], joysticks[joystick][1])
                radius = joysticks[joystick][2]
                # Check if mouse is within joystick radius
                if math.sqrt((mouse_pos[0] - joystick_center[0]) ** 2 + (mouse_pos[1] - joystick_center[1]) ** 2) <= radius:
                    dragging_joystick[joystick] = True  # Start dragging joystick

        # Check for mouse button up events
        if event.type == pygame.MOUSEBUTTONUP:
            # Reset all button states
            for button in buttons:
                button_states[button] = 0
            
            # Reset all D-Pad states
            for direction in dpad:
                dpad_states[direction] = 0
            
            # Stop dragging any joystick and reset values
            for joystick in dragging_joystick:
                dragging_joystick[joystick] = False
                joystick_values[joystick] = (0, 0)  # Reset joystick values

        # Check for mouse motion events
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()  # Update mouse position
            # Update joystick values if being dragged
            for joystick in joysticks:
                if dragging_joystick[joystick]:
                    joystick_center = (joysticks[joystick][0], joysticks[joystick][1])
                    radius = joysticks[joystick][2]
                    angle = math.atan2(mouse_pos[1] - joystick_center[1], mouse_pos[0] - joystick_center[0])
                    distance = min(radius, math.hypot(mouse_pos[0] - joystick_center[0], mouse_pos[1] - joystick_center[1]))
                    # Update joystick values based on mouse position
                    joystick_values[joystick] = (math.cos(angle) * (distance / radius), math.sin(angle) * (distance / radius))

        # Check for key down events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dpad_states['up'] = 1
            if event.key == pygame.K_s:
                dpad_states['down'] = 1
            if event.key == pygame.K_a:
                dpad_states['left'] = 1
            if event.key == pygame.K_d:
                dpad_states['right'] = 1
            if event.key == pygame.K_i:
                button_states['Y'] = 1
            if event.key == pygame.K_k:
                button_states['A'] = 1
            if event.key == pygame.K_j:
                button_states['X'] = 1
            if event.key == pygame.K_l:
                button_states['B'] = 1
            if event.key == pygame.K_q:
                button_states['L1'] = 1
            if event.key == pygame.K_e:
                button_states['L2'] = 1
            if event.key == pygame.K_u:
                button_states['R1'] = 1
            if event.key == pygame.K_o:
                button_states['R2'] = 1
            if event.key == pygame.K_KP8:
                joystick_values['right'] = (0, -1)
            if event.key == pygame.K_KP5:
                joystick_values['right'] = (0, 1)
            if event.key == pygame.K_KP4:
                joystick_values['right'] = (-1, 0)
            if event.key == pygame.K_KP6:
                joystick_values['right'] = (1, 0)
            if event.key == pygame.K_UP:
                joystick_values['left'] = (0, -1)
            if event.key == pygame.K_DOWN:
                joystick_values['left'] = (0, 1)
            if event.key == pygame.K_LEFT:
                joystick_values['left'] = (-1, 0)
            if event.key == pygame.K_RIGHT:
                joystick_values['left'] = (1, 0)

        # Check for key up events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                dpad_states['up'] = 0
            if event.key == pygame.K_s:
                dpad_states['down'] = 0
            if event.key == pygame.K_a:
                dpad_states['left'] = 0
            if event.key == pygame.K_d:
                dpad_states['right'] = 0
            if event.key == pygame.K_i:
                button_states['Y'] = 0
            if event.key == pygame.K_k:
                button_states['A'] = 0
            if event.key == pygame.K_j:
                button_states['X'] = 0
            if event.key == pygame.K_l:
                button_states['B'] = 0
            if event.key == pygame.K_q:
                button_states['L1'] = 0
            if event.key == pygame.K_e:
                button_states['L2'] = 0
            if event.key == pygame.K_u:
                button_states['R1'] = 0
            if event.key == pygame.K_o:
                button_states['R2'] = 0
            if event.key == pygame.K_KP8 or event.key == pygame.K_KP5 or event.key == pygame.K_KP4 or event.key == pygame.K_KP6:
                joystick_values['right'] = (0, 0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                joystick_values['left'] = (0, 0)

    # Draw UI elements
    draw_buttons()
    draw_l1_l2()
    draw_r1_r2()
    draw_dpad()
    draw_joystick((joysticks["left"][0], joysticks["left"][1]), joysticks["left"][2], joystick_values["left"])
    draw_joystick((joysticks["right"][0], joysticks["right"][1]), joysticks["right"][2], joystick_values["right"])
    draw_key_prompts()

    # SensorJoy message
    joy_msg = datatypes.SensorJoy()
    joy_msg.axes = [
        -joystick_values['left'][0],
        -joystick_values['left'][1],
        -joystick_values['right'][0],
        -joystick_values['right'][1],
    ]
    joy_msg.buttons = [
        button_states['A'],
        button_states['B'],
        button_states['X'],
        button_states['Y'],
        button_states['L1'],
        button_states['R2'],
        button_states['L2'],
        button_states['R1'],
        0, 0, 0, 0,  # Reserved buttons
        dpad_states['up'],
        dpad_states['down'],
        dpad_states['left'],
        dpad_states['right'],
        0, 0,  # Reserved buttons
    ]

    # Publish SensorJoy message
    robot_joystick.publishSensorJoy(joy_msg)

    pygame.display.flip()  # Update the display

pygame.quit()  # Quit pygame
