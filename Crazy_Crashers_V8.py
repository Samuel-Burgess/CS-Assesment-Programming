"""Crazy Crashers V9. Nearly Finished."""

import pygame
import random
import os

# Initialize pygame
pygame.init()
# Initialize the screen
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crazy Crashers")
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Font for displaying text
font_title = pygame.font.Font(None, 40)
font_subtitle = pygame.font.Font(None, 30)
font_text = pygame.font.Font(None, 20)
# High score file
HIGH_SCORE_FILE = "high_score.txt"


def load_images(folder_path):
    images = {}
    for filename in os.listdir(folder_path):
        # Check if it's an image file
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Get filename without extension
            name, _ = os.path.splitext(filename)
            # Load the image and add it to the dictionary
            image = pygame.image.load(
                os.path.join(folder_path, filename)).convert_alpha()
            images[name] = image
    return images


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


# Load all game assets
cover_art = (pygame.image.load
             (os.path.join("assets", "cover_art.jpg")).convert_alpha())
cover_art_stretched = (pygame.transform.scale
                       (cover_art, (SCREEN_WIDTH, SCREEN_HEIGHT)))
crash_art = (pygame.image.load
             (os.path.join("assets", "crash_art.jpg")).convert_alpha())
crash_art_stretched = (pygame.transform.scale
                       (crash_art, (SCREEN_WIDTH, SCREEN_HEIGHT)))
road_image1 = (pygame.image.load
               (os.path.join("assets", "road.png")).convert_alpha())
road_image2 = (pygame.image.load
               (os.path.join("assets", "road.png")).convert_alpha())
assets_path_cars = os.path.join("assets", "cars")
car_images = load_images(assets_path_cars)
road_stretched1 = (pygame.transform.scale
                   (road_image1, (SCREEN_WIDTH, SCREEN_HEIGHT)))
road_stretched2 = (pygame.transform.scale
                   (road_image2, (SCREEN_WIDTH, SCREEN_HEIGHT)))

# Initialize gameplay variables
background_pos1 = 0
background_pos2 = -SCREEN_HEIGHT
scroll_speed = 3
score = 0
high_score = load_high_score()
spawn_timer = 0
spawn_interval = 175
LANE_X_POSITIONS = [60, 98, 145, 180]


class Player(pygame.sprite.Sprite):  # Player car class
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.lane = 1  # Default lane is center lane

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_lane_position(self):
        if self.lane == 0:
            self.rect.centerx = 60
        elif self.lane == 1:
            self.rect.centerx = 98
        elif self.lane == 2:
            self.rect.centerx = 145
        elif self.lane == 3:
            self.rect.centerx = 180

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < 3:
            self.lane += 1


class Car(pygame.sprite.Sprite):  # obstacle car class
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        global score, scroll_speed, obstacle_cars
        # Move the car down by the scroll speed
        self.rect.y += scroll_speed
        # Check if the car has gone off the screen
        if self.rect.top > SCREEN_HEIGHT:
            # Remove the car from the obstacle_cars list
            obstacle_cars.remove(self)
            score += 1
            # Increase scroll speed every 10 points
            if 0 < scroll_speed < 25:
                if score % 10 == 0 and score != 0:
                    scroll_speed += 1
            elif 25 <= scroll_speed < 50:
                if score % 15 == 0 and score != 0:
                    scroll_speed += 1
            elif 50 <= scroll_speed < 100:
                if score % 100 == 0 and score != 0:
                    scroll_speed += 1


def check_collision(player, obstacles):
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            return True
    return False


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def start_menu():
    while True:
        SCREEN.fill(WHITE)
        SCREEN.blit(cover_art_stretched, (0, 0))
        draw_text("Crazy Crashers", font_title,
                  BLACK, SCREEN, 15, 0)
        draw_text("Press any key to start", font_subtitle,
                  WHITE, SCREEN, 15, 140)
        draw_text("Use 'A' and 'D' or", font_text,
                  WHITE, SCREEN, 60, 95)
        draw_text("the left and right arrows move", font_text,
                  WHITE, SCREEN, 30, 110)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                return True


def game_over_menu(score, high_score):
    while True:
        SCREEN.fill(WHITE)
        SCREEN.blit(crash_art_stretched, (0, 0))
        draw_text(f"Game Over!", font_title, WHITE, SCREEN, 40, 0)
        draw_text(f"Score: {score}", font_title, WHITE, SCREEN, 60, 80)
        draw_text(f"High Score: {high_score}", font_subtitle, WHITE, SCREEN, 45, 120)
        draw_text("Press R to restart", font_subtitle, WHITE, SCREEN, 40, 350)
        draw_text("or Q to quit", font_subtitle, WHITE, SCREEN, 70, 370)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False


def spawn_cars():
    global spawn_timer
    # Increment spawn timer
    spawn_timer += 1
    if (spawn_interval - (scroll_speed * 10)) <= spawn_timer >= 15:
        spawn_timer = 0
        random_lanes_spawn = random.randint(1, 100)
        print("spawn attempt")
        print(random_lanes_spawn)
        if random_lanes_spawn < 25:
            new_car = Car(car_images[random.choice(list(car_images.keys()))],
                          random.choice(LANE_X_POSITIONS),
                          -SCREEN_HEIGHT // 2)
            obstacle_cars.append(new_car)
        elif random_lanes_spawn < 90:
            lanes = [0, 1, 2, 3]
            random_lane = random.choice(lanes)
            lanes.remove(random_lane)
            new_car = Car(car_images[random.choice(list(car_images.keys()))],
                          LANE_X_POSITIONS[random_lane],
                          -SCREEN_HEIGHT // 2)
            obstacle_cars.append(new_car)
            random_lane_2 = random.choice(lanes)
            lanes.remove(random_lane_2)
            new_car = Car(car_images[random.choice(list(car_images.keys()))],
                          LANE_X_POSITIONS[random_lane_2],
                          -SCREEN_HEIGHT // 2)
            obstacle_cars.append(new_car)
        elif random_lanes_spawn < 100:
            lanes = [0, 1, 2, 3]
            random_lane = random.choice(lanes)
            lanes.remove(random_lane)
            new_car = Car(car_images[random.choice(list(car_images.keys()))],
                          LANE_X_POSITIONS[random_lane],
                          -SCREEN_HEIGHT // 2)
            obstacle_cars.append(new_car)
            random_lane_2 = random.choice(lanes)
            lanes.remove(random_lane_2)
            new_car = Car(car_images[random.choice(list(car_images.keys()))],
                          LANE_X_POSITIONS[random_lane_2],
                          -SCREEN_HEIGHT // 2)
            obstacle_cars.append(new_car)
            random_lane_3 = random.choice(lanes)
            lanes.remove(random_lane_3)
            new_car = Car(car_images[random.choice(list(car_images.keys()))],
                          LANE_X_POSITIONS[random_lane_3],
                          -SCREEN_HEIGHT // 2)
            obstacle_cars.append(new_car)


# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
obstacle_cars = []
player_car = Player(car_images["car_18"],
                    LANE_X_POSITIONS[1], SCREEN_HEIGHT - 50)

# Show start menu
if not start_menu():
    running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_car.move_left()
                player_car.set_lane_position()
                player_car.draw(SCREEN)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_car.move_right()
                player_car.set_lane_position()
                player_car.draw(SCREEN)

    if not game_over:
        # Update background positions
        background_pos1 += scroll_speed
        background_pos2 += scroll_speed
        if background_pos1 >= SCREEN_HEIGHT:
            background_pos1 = -SCREEN_HEIGHT
        if background_pos2 >= SCREEN_HEIGHT:
            background_pos2 = -SCREEN_HEIGHT
        # Do car spawning
        spawn_cars()

        # Draw all backgrounds and game sprites
        SCREEN.blit(road_stretched1, (0, background_pos1))
        SCREEN.blit(road_stretched2, (0, background_pos2))
        player_car.set_lane_position()
        player_car.draw(SCREEN)
        for car in obstacle_cars:
            car.update()
            car.draw(SCREEN)
        draw_text(f"Score: {score}", font_text,
                  BLACK, SCREEN, 10, 10)

        # Check for collisions
        if check_collision(player_car, obstacle_cars):
            game_over = True
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            print("Game Over! Your score is:", score)

    else:
        if not game_over_menu(score, high_score):
            running = False
            pygame.quit()
            quit()
        else:
            game_over = False
            scroll_speed = 2
            score = 0
            obstacle_cars.clear()
            player_car = Player(car_images["car_18"],
                                LANE_X_POSITIONS[1], SCREEN_HEIGHT - 50)
            spawn_timer = 0
    # tick and update the display
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
