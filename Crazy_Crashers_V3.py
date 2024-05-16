"""Version 3 of Crazy Crasher game. Creating the car class."""

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
road_image1 = pygame.image.load(os.path.join("assets", "road.png")) \
    .convert_alpha()
road_image2 = pygame.image.load(os.path.join("assets", "road.png")) \
    .convert_alpha()
assets_path_cars = os.path.join("assets", "cars")
car_images = load_images(assets_path_cars)
assets_path_bikes = os.path.join("assets", "bikes")
bike_images = load_images(assets_path_bikes)
assets_path_trucks = os.path.join("assets", "trucks")
truck_images = load_images(assets_path_trucks)

# Stretch the road image to fit the screen
road_stretched1 = pygame.transform.scale(road_image1, (SCREEN_WIDTH, SCREEN_HEIGHT))
road_stretched2 = pygame.transform.scale(road_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define variables for background positions
background_pos1 = 0
background_pos2 = -SCREEN_HEIGHT  # Start the second image offscreen

# Choose a random car image from the dictionary
random_car_name = random.choice(list(car_images.keys()))
scroll_timer = 0
scroll_speed = 1


class Car(pygame.sprite.Sprite):
    """A class representing a car on the screen."""

    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        """Draws the car on the screen."""
        screen.blit(self.image, self.rect)


# Main game loop
clock = pygame.time.Clock()
running = True
obstacle_cars = []

while running:
    # Update background positions
    background_pos1 += scroll_speed  # Adjust for desired scrolling speed
    background_pos2 += scroll_speed
    scroll_timer += 1

    # Check if the first image needs to reset
    if background_pos1 >= SCREEN_HEIGHT:
        background_pos1 = -SCREEN_HEIGHT

    # Check if the second image needs to reset
    if background_pos2 >= SCREEN_HEIGHT:
        background_pos2 = -SCREEN_HEIGHT

    # Increase scroll speed every 100 points
    if scroll_timer % 1000 == 0:
        scroll_speed += 1

    # Print for debugging purposes
    print(scroll_timer)

    # Draw the background images
    SCREEN.blit(road_stretched1, (0, background_pos1))
    SCREEN.blit(road_stretched2, (0, background_pos2))

    # Add a new obstacle car with a random chance
    if random.randint(1, 5) == 1:  # Adjust the probability of adding a new car
        # Choose a random lane for the car
        lane_pos = random.randint(0, SCREEN_WIDTH - car_images[random_car_name].get_width())
        # Create a new obstacle car and add it to the list
        new_car = Car(car_images[random.choice(list(car_images.keys()))], lane_pos, -SCREEN_HEIGHT)
        obstacle_cars.append(new_car)
        print("car made")

    # Rest of your game logic (drawing cars, handling collisions, etc.)
    # Draw the obstacle cars
    for car in obstacle_cars:
        car.update()
        car.draw(SCREEN)  # Call the draw method on each car
    # Handle events (like clicking the X button)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

    # Update the display
    pygame.display.flip()

