import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Translucent Rectangle")

# Define the translucent rectangle's color (RGBA)
rect_color = (255, 0, 0, 128)  # Red with 50% transparency

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw the translucent rectangle
    pygame.draw.rect(screen, rect_color, (50, 50, 200, 100))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()