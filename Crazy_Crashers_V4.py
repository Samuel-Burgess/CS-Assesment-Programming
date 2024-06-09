"""adjusting the car class. V4"""
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


class Player(pygame.sprite.Sprite):
    """A class for the player car."""

    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.lane = 1  # Default lane is center lane

    def draw(self, screen):
        """Draws the car on the screen."""
        screen.blit(self.image, self.rect)

    def set_lane_position(self):
        """Sets the car's position based on its current lane."""
        print(self.lane)
        if self.lane == 0:
            self.rect.centerx = LANE_X_POSITIONS[0]
        elif self.lane == 1:
            self.rect.centerx = LANE_X_POSITIONS[1]
        elif self.lane == 1:
            self.rect.centerx = LANE_X_POSITIONS[2]
        elif self.lane == 1:
            self.rect.centerx = LANE_X_POSITIONS[3]
        print(self.rect.centerx)

    def move_left(self):
        """Move the car to the left lane if possible."""
        print(self.lane)
        if self.lane > 0:
            self.lane -= 1
            self.set_lane_position()
            print(self.lane)

    def move_right(self):
        """Move the car to the right lane if possible."""
        print(self.lane)
        if self.lane < 3:
            self.lane += 1
            self.set_lane_position()
            print(self.lane)


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


def check_collision(player, obstacles):
    """Check for collision between player and obstacles."""
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            return True
    return False


# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
obstacle_cars = []
player_car = Player(random.choice(list(car_images.values())), LANE_X_POSITIONS[1], SCREEN_HEIGHT - 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_car.move_left()
                player_car.set_lane_position()
                player_car.draw(SCREEN)
                print("Moved left")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_car.move_right()
                player_car.set_lane_position()
                player_car.draw(SCREEN)
                print("Moved right")

    if not game_over:
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

        # Increase scroll speed every 1000 points
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

        # Draw the player car
        player_car.set_lane_position()
        player_car.draw(SCREEN)

        # Draw the obstacle cars
        for car in obstacle_cars:
            car.update()
            car.draw(SCREEN)

        # Check for collisions
        if check_collision(player_car, obstacle_cars):
            game_over = True
            print("Game Over! Your score is:", score)

    clock.tick(60)

    # Update the display
    pygame.display.flip()

pygame.quit()

