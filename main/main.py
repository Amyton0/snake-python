import os.path

import pygame
import random
import time
import pickle


class Snake:
    def __init__(self):
        self.length = 5
        self.direction = 0
        self.turns = []
        self.head = (width // 2, height // 2)
        self.segments = []
        self.fps = 70
        self.score = 0
        self.color = (128, 80, 128)
        self.size = snake_size

    def move(self):
        current_turn = len(self.turns) - 1
        current_direction = self.direction

        if self.direction == 0:
            self.head = (self.head[0], self.head[1] - 1)
        elif self.direction == 1:
            self.head = (self.head[0] + 1, self.head[1])
        elif self.direction == 2:
            self.head = (self.head[0], self.head[1] + 1)
        else:
            self.head = (self.head[0] - 1, self.head[1])

        current_coordinates = self.head
        self.segments = [self.head]

        for i in range(self.length - 1):
            if len(self.turns) > current_turn >= 0 and \
                    count_distance(current_coordinates, self.turns[current_turn][0]) < 2 * snake_size:
                current_direction = self.turns[current_turn][1]
                if current_direction == 0:
                    current_coordinates = (self.turns[current_turn][0][0],
                                           current_coordinates[1] +
                                           count_distance_from_turn(self.turns[current_turn][0], current_coordinates))
                elif current_direction == 1:
                    current_coordinates = (current_coordinates[0] -
                                           count_distance_from_turn(self.turns[current_turn][0], current_coordinates),
                                           self.turns[current_turn][0][1])
                elif current_direction == 2:
                    current_coordinates = (self.turns[current_turn][0][0], current_coordinates[1] -
                                           count_distance_from_turn(self.turns[current_turn][0], current_coordinates))
                else:
                    current_coordinates = (current_coordinates[0] +
                                           count_distance_from_turn(self.turns[current_turn][0], current_coordinates),
                                           self.turns[current_turn][0][1])
                current_turn -= 1
            else:
                if current_direction == 0:
                    current_coordinates = (current_coordinates[0], current_coordinates[1] + snake_size * 2)
                elif current_direction == 1:
                    current_coordinates = (current_coordinates[0] - snake_size * 2, current_coordinates[1])
                elif current_direction == 2:
                    current_coordinates = (current_coordinates[0], current_coordinates[1] - snake_size * 2)
                else:
                    current_coordinates = (current_coordinates[0] + snake_size * 2, current_coordinates[1])
            self.segments.append(current_coordinates)

        if current_turn > 0:
            self.turns = self.turns[current_turn::]

    def draw(self):
        for segment in self.segments:
            pygame.draw.circle(screen, self.color, segment, self.size)

    def eat_length_increasing_food(self):
        self.length += 1
        self.score += 1

    def eat_length_reducing_food(self):
        self.length -= 1

    def eat_speed_increasing_food(self):
        self.fps += 10

    def eat_speed_reducing_food(self):
        self.fps -= 10

    def eat_bonus_food(self):
        self.score += 10

    def is_collision(self):
        if self.head[0] < self.size or self.head[0] > width - self.size or \
                self.head[1] < self.size or self.head[1] > height - self.size:
            return True

        for segment in self.segments[2:]:
            if count_distance(segment, self.head) < 2 * snake_size:
                return True

        for level in levels:
            if level.is_collision(game.snake.head):
                return True

        return False


class Food:
    def __init__(self):
        self.coordinates = (random.randint(food_size, width - food_size),
                            random.randint(food_size, height - food_size))

        while self.coordinates[0] < 130 and self.coordinates[1] < 70 or self.coordinates[0] > \
                pause_button_coordinates[0] - pause_button_size and self.coordinates[1] > \
                pause_button_coordinates[1] - pause_button_size and \
                not Level(level1_obstacles + level2_obstacles + level3_obstacles).is_collision(self.coordinates):
            self.coordinates = (random.randint(food_size, width - food_size),
                                random.randint(food_size, height - food_size))


class LengthIncreasingFood(Food):
    def draw(self):
        pygame.draw.circle(screen, length_increasing_food_color, self.coordinates, food_size)


class LengthReducingFood(Food):
    def draw(self):
        pygame.draw.circle(screen, length_reducing_food_color, self.coordinates, food_size)


class SpeedIncreasingFood(Food):
    def draw(self):
        pygame.draw.circle(screen, speed_increasing_food_color, self.coordinates, food_size)


class SpeedReducingFood(Food):
    def draw(self):
        pygame.draw.circle(screen, speed_reducing_food_color, self.coordinates, food_size)


class BonusFood(Food):
    def __init__(self):
        super().__init__()
        self.ticks = pygame.time.get_ticks()

    def set_timer(self):
        self.ticks = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.circle(screen, bonus_food_color, self.coordinates, bonus_food_size)


class Obstacle:
    color = (127, 127, 127)

    def __init__(self, x=None, y=None):
        if x is not None and y is not None:
            self.coordinates = (x, y, obstacle_size, obstacle_size)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.coordinates)


class Level:
    def __init__(self, obstacles):
        self.obstacles = obstacles

    def draw(self):
        for obstacle in self.obstacles:
            obstacle.draw()

    def is_collision(self, coordinates):
        for obstacle in self.obstacles:
            if is_collision_obstacle(obstacle.coordinates, coordinates):
                return True
        return False


def create_levels(score):
    levels = []

    level1 = Level(level1_obstacles)
    levels.append(level1)

    if score >= 5:
        level2 = Level(level1_obstacles + level2_obstacles)
        levels.append(level2)

        if score >= 10:
            level3 = Level(level1_obstacles + level2_obstacles + level3_obstacles)
            levels.append(level3)

    return levels


def count_distance(coordinates1, coordinates2):
    return int(((coordinates1[0] - coordinates2[0]) ** 2 + (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5)


def count_distance_from_turn(turn_coordinates, coordinates):
    return int((abs((2 * snake_size) ** 2 - count_distance(turn_coordinates, coordinates) ** 2)) ** 0.5)


def is_collision_obstacle(obstacle_coordinates, object_coordinates):
    if obstacle_coordinates[0] < object_coordinates[0] - snake_size < obstacle_coordinates[0] + obstacle_size:
        if obstacle_coordinates[1] < object_coordinates[1] - snake_size < \
                obstacle_coordinates[1] + obstacle_size:
            return True
        if obstacle_coordinates[1] < object_coordinates[1] + snake_size < \
                obstacle_coordinates[1] + obstacle_size:
            return True
    if obstacle_coordinates[0] < object_coordinates[0] + snake_size < obstacle_coordinates[0] + \
            obstacle_size:
        if obstacle_coordinates[1] < object_coordinates[1] - snake_size < \
                obstacle_coordinates[1] + obstacle_size:
            return True
        if obstacle_coordinates[1] < object_coordinates[1] + snake_size < \
                obstacle_coordinates[1] + obstacle_size:
            return True

    return False


class Game:
    def __init__(self):
        self.running = True
        self.is_alive = True
        self.is_paused = False

        self.lives = 3
        self.last_length = 0

        self.length_increasing_food = LengthIncreasingFood()
        self.length_reducing_food = LengthReducingFood()
        self.speed_increasing_food = SpeedIncreasingFood()
        self.speed_reducing_food = SpeedReducingFood()
        self.bonus_food = BonusFood()

        self.is_bonus = False

        self.snake = Snake()

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)


pygame.init()

size = width, height = 800, 600

screen = pygame.display.set_mode(size)

length_increasing_food_color = (135, 234, 0)
length_reducing_food_color = (240, 128, 128)
speed_increasing_food_color = (102, 205, 170)
speed_reducing_food_color = (240, 230, 140)
bonus_food_color = (255, 215, 0)

play_button_size = 70

pause_button_size = 10
pause_button_color = (200, 200, 200)

play_button_coordinates = (width // 2, height // 2 + 50)
pause_button_coordinates = (width - 15, 15)

food_size = 6
bonus_food_size = 8
snake_size = 7
obstacle_size = 30

font = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 40)
font3 = pygame.font.Font(None, 30)
font4 = pygame.font.Font(None, 28)

clock = pygame.time.Clock()

game = Game()

level1_obstacles = [Obstacle(100, 100), Obstacle(600, 400)]
level2_obstacles = [Obstacle(500, 40), Obstacle(200, 300)]
level3_obstacles = [Obstacle(400, 400), Obstacle(600, 200), Obstacle(100, 500)]

loaded = False

loading_button_coordinates = (width // 3 - 20, height // 2)
not_loading_button_coordinates = (2 * width // 3 + 20, height // 2)
loading_button_size = 120
loading_button_color = (176, 224, 230)

if os.path.isfile("saving.pickle"):
    while not loaded:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loaded = True
                game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if count_distance(loading_button_coordinates, event.pos) < loading_button_size:
                    game = Game.load("saving.pickle")
                    loaded = True
                elif count_distance(not_loading_button_coordinates, event.pos) < loading_button_size:
                    loaded = True
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, loading_button_color, loading_button_coordinates, loading_button_size)
        pygame.draw.circle(screen, loading_button_color, not_loading_button_coordinates, loading_button_size)
        loading_text = font3.render("Загрузить", True, (0, 0, 0))
        not_loading_text = font3.render("Не загружать", True, (0, 0, 0))
        saving_text = font4.render("последнее сохранение", True, (0, 0, 0))
        screen.blit(loading_text, (loading_button_coordinates[0] - 50, loading_button_coordinates[1] - 30))
        screen.blit(saving_text, (loading_button_coordinates[0] - 111, loading_button_coordinates[1] + 5))
        screen.blit(not_loading_text, (not_loading_button_coordinates[0] - 65, not_loading_button_coordinates[1] - 30))
        screen.blit(saving_text, (not_loading_button_coordinates[0] - 111, not_loading_button_coordinates[1] + 5))
        pygame.display.flip()
            

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save("saving.pickle")
            game.running = False
        if event.type == pygame.KEYDOWN and game.is_alive and not game.is_paused:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and game.snake.direction != 0 and \
                    game.snake.direction != 2:
                if len(game.snake.turns) > 0:
                    if count_distance(game.snake.head, game.snake.turns[-1][0]) > 2 * snake_size:
                        game.snake.turns.append((game.snake.head, game.snake.direction))
                        game.snake.direction = 0
                else:
                    game.snake.turns.append((game.snake.head, game.snake.direction))
                    game.snake.direction = 0
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game.snake.direction != 1 and \
                    game.snake.direction != 3:
                if len(game.snake.turns) > 0:
                    if count_distance(game.snake.head, game.snake.turns[-1][0]) > 2 * snake_size:
                        game.snake.turns.append((game.snake.head, game.snake.direction))
                        game.snake.direction = 1
                else:
                    game.snake.turns.append((game.snake.head, game.snake.direction))
                    game.snake.direction = 1
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game.snake.direction != 0 and \
                    game.snake.direction != 2:
                if len(game.snake.turns) > 0:
                    if count_distance(game.snake.head, game.snake.turns[-1][0]) > 2 * snake_size:
                        game.snake.turns.append((game.snake.head, game.snake.direction))
                        game.snake.direction = 2
                else:
                    game.snake.turns.append((game.snake.head, game.snake.direction))
                    game.snake.direction = 2
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game.snake.direction != 1 and \
                    game.snake.direction != 3:
                if len(game.snake.turns) > 0:
                    if count_distance(game.snake.head, game.snake.turns[-1][0]) > 2 * snake_size:
                        game.snake.turns.append((game.snake.head, game.snake.direction))
                        game.snake.direction = 3
                else:
                    game.snake.turns.append((game.snake.head, game.snake.direction))
                    game.snake.direction = 3
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (count_distance(event.pos, play_button_coordinates)) <= play_button_size and not game.is_alive:
                game.lives = 3
                game.is_alive = True

                game.length_increasing_food = LengthIncreasingFood()
                game.length_reducing_food = LengthReducingFood()
                game.speed_increasing_food = SpeedIncreasingFood()
                game.speed_reducing_food = SpeedReducingFood()

                game.snake = Snake()
            if (count_distance(event.pos, pause_button_coordinates)) <= pause_button_size and game.is_alive:
                if game.is_paused:
                    game.is_paused = False
                else:
                    game.is_paused = True
    if game.is_alive:
        screen.fill((255, 255, 255))
        game.length_increasing_food.draw()
        game.length_reducing_food.draw()
        game.speed_increasing_food.draw()
        game.speed_reducing_food.draw()
        if game.is_bonus:
            game.bonus_food.draw()
        game.snake.draw()

        if game.snake.score == 20:
            easter_egg = font3.render("Ого!", True, (0, 0, 0))
            screen.blit(easter_egg, (width // 2 - 10, 20))

        if game.snake.fps > 150:
            game.snake.color = (30, 144, 255)
        else:
            game.snake.color = (128, 80, 128)

        score = font.render("Score " + str(game.snake.score), True, (0, 0, 0))
        lives_on_screen = font.render("Lives " + str(game.lives), True, (0, 0, 0))
        screen.blit(score, (10, 10))
        screen.blit(lives_on_screen, (10, 40))
        levels = create_levels(game.snake.score)

        for level in levels:
            level.draw()

        pygame.draw.circle(screen, pause_button_color, pause_button_coordinates, pause_button_size, 2)

        if not game.is_paused:
            game.snake.move()

            pygame.draw.rect(screen, pause_button_color, (width - 19, 10, 3, 10))
            pygame.draw.rect(screen, pause_button_color, (width - 14, 10, 3, 10))

            if count_distance(game.length_increasing_food.coordinates, game.snake.head) <= snake_size + \
                    food_size:
                game.snake.eat_length_increasing_food()
                game.length_increasing_food = LengthIncreasingFood()
                game.length_increasing_food.draw()

            if count_distance(game.length_reducing_food.coordinates, game.snake.head) <= snake_size + food_size:
                game.snake.eat_length_reducing_food()
                game.length_reducing_food = LengthReducingFood()
                game.length_reducing_food.draw()

            if count_distance(game.speed_increasing_food.coordinates, game.snake.head) <= snake_size + food_size:
                game.snake.eat_speed_increasing_food()
                game.speed_increasing_food = SpeedIncreasingFood()
                game.speed_increasing_food.draw()

            if count_distance(game.speed_reducing_food.coordinates, game.snake.head) <= snake_size + food_size:
                game.snake.eat_speed_reducing_food()
                game.speed_reducing_food = SpeedReducingFood()
                game.speed_reducing_food.draw()

            if game.is_bonus:
                if (pygame.time.get_ticks() - game.bonus_food.ticks) / 1000 >= 10:
                    game.is_bonus = False
                    game.bonus_food = BonusFood()
            else:
                if (pygame.time.get_ticks() - game.bonus_food.ticks) / 1000 >= 20:
                    game.is_bonus = True
                    game.bonus_food.set_timer()

            if game.is_bonus and count_distance(game.bonus_food.coordinates, game.snake.head) <= snake_size + food_size:
                game.snake.eat_bonus_food()
                game.bonus_food = BonusFood()
                game.is_bonus = False

            if game.snake.is_collision() or game.snake.length == 0:
                game.lives = game.lives - 1
                last_length = game.snake.length
                game.snake = Snake()
                if last_length > 0:
                    game.snake.length = last_length
                else:
                    game.snake.length = 1
                if game.lives <= 0:
                    game.is_alive = False
                death_screen = pygame.Surface(size)
                death_screen.fill((255, 0, 0))
                death_screen.set_alpha(150)
                screen.blit(death_screen, (0, 0))
                pygame.display.flip()
                time.sleep(0.5)

            clock.tick(game.snake.fps)
        else:
            pygame.draw.polygon(screen, pause_button_color, ((width - 18, 10), (width - 11, 14), (width - 18, 19)))

    else:
        screen.fill((255, 255, 255))
        text = font.render("Игра окончена", True, (0, 0, 0))
        screen.blit(text, (width // 2 - 130, height // 2 - 150))
        score = font.render(str(game.snake.score), True, (0, 0, 0))
        screen.blit(score, (width // 2 - 10, height // 2 - 90))

        playText = font2.render("Играть", True, (0, 0, 0))

        pygame.draw.circle(screen, 'red', play_button_coordinates, play_button_size)
        screen.blit(playText, (width // 2 - 43, height // 2 + 40))

    pygame.display.flip()

pygame.quit()
