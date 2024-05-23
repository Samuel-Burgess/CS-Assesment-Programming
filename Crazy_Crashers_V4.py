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
            image = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            images[name] = image
    return images


# Load all game assets
road_image1 = pygame.image.load(os.path.join("assets", "road.png")).convert_alpha()
road_image2 = pygame.image.load(os.path.join("assets", "road.png")).convert_alpha()
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
score = 0
spawn_timer = 0
spawn_interval = 100  # Adjust spawn interval
max_cars_per_lane = 3  # Maximum cars per lane


# Define x positions for the four lanes
LANE_X_POSITIONS = [60, 98, 145, 180]

class Car(pygame.sprite.Sprite):
    """A class representing a car on the screen."""

    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        """Draws the car on the screen."""
        screen.blit(self.image, self.rect)

    def update(self):
        """Updates the car's position on the screen."""
        # Move the car down by the scroll speed
        self.rect.y += scroll_speed

        # Check if the car has gone off the screen
        global score
        if self.rect.top > SCREEN_HEIGHT:
            # Remove the car from the obstacle_cars list
            obstacle_cars.remove(self)
            score += 1
            print(score)


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

    # Increment spawn timer
    spawn_timer += 1

    # Increase spawn rate as score increases
    if spawn_timer >= spawn_interval - score // 10:  # Adjust the rate increase
        spawn_timer = 0
        # Shuffle the lane positions to randomize the order
        random.shuffle(LANE_X_POSITIONS)
        for lane_pos in LANE_X_POSITIONS:
            # Count the number of cars in the current lane
            cars_in_lane = sum(1 for car in obstacle_cars if car.rect.centerx == lane_pos)
            # Spawn a new car if there are fewer than the maximum allowed cars in the lane and there's a chance to spawn
            if cars_in_lane < max_cars_per_lane and random.random() < 0.85:  # Adjust the spawn chance
                new_car = Car(car_images[random.choice(list(car_images.keys()))], lane_pos, -SCREEN_HEIGHT // 2)
                obstacle_cars.append(new_car)
                break  # Break the loop after spawning one car per attempt

    # Draw the background images
    SCREEN.blit(road_stretched1, (0, background_pos1))
    SCREEN.blit(road_stretched2, (0, background_pos2))

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

pygame.quit()
