import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hovering Box")

# Define colors
white = (255, 255, 255)
gray = (128, 128, 128)
hover_color = (0, 255, 0)  # Green for hover

# Define box dimensions
box_x = 100
box_y = 100
box_width = 150
box_height = 50

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check if mouse is hovering over the box
    if box_x <= mouse_x <= box_x + box_width and box_y <= mouse_y <= box_y + box_height:
        box_color = hover_color
    else:
        box_color = gray

    # Fill the screen with white
    screen.fill(white)

    # Draw the box
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()