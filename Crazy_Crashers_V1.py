"""Crazy Crashers game V1. Setting up game basis,
and creating a function to load all images from assets folder."""

import pygame
import random
import os


# Initialize pygame
pygame.init()

# Define phone screen size (adjust width and height for your target device)
SCREEN_WIDTH = 240  # Adjust for phone screen width
SCREEN_HEIGHT = 400  # Adjust for phone screen height in portrait mode

# Create the game screen with the desired dimensions
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window title
pygame.display.set_caption("Crazy Crashers")


def load_images(folder_path):
    """Loads all images from a folder and returns a dictionary."""
    images = {}
    for filename in os.listdir(folder_path):
        # Check if it's an image file
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Get filename without extension
            name, _ = os.path.splitext(filename)
            # Load the image and add it to the dictionary
            image = pygame.image.load(os.path.join(folder_path, filename)) \
                .convert_alpha()
            images[name] = image
    return images


# Load all game assets
road_image = pygame.image.load(os.path.join("assets", "road.png")) \
    .convert_alpha()
assets_path_cars = os.path.join("assets", "cars")
car_images = load_images(assets_path_cars)


# Fill the screen with white color
SCREEN.fill((255, 255, 255))  # White color in RGB format

# Stretch the road image to fit the screen
road_stretched = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Blit the stretched road image onto the screen
SCREEN.blit(road_stretched, (0, 0))
# Choose a random car image from the dictionary
random_car_name = random.choice(list(car_images.keys()))
SCREEN.blit(car_images[random_car_name], (0, 0))


# Update the display to show the changes
pygame.display.flip()
# Keep the window open until closed by the user
running = True
while running:
    # Handle events (like clicking the X button)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update the display (not strictly necessary here, but good practice)
    pygame.display.flip()
