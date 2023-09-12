import pygame
import random
import time


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
                print(self.head)
                print(segment)
                return True

        for obstruction in obstructions:
            if is_collision_obstruction(obstruction.coordinates, self.head):
                return True

        return False


class Food:
    def __init__(self):
        self.coordinates = (random.randint(food_size, width - food_size), random.randint(food_size, height - food_size))

        while self.coordinates[0] < 130 and self.coordinates[1] < 70 or self.coordinates[0] > \
                pause_button_coordinates[0] - pause_button_size and self.coordinates[1] > \
                pause_button_coordinates[1] - pause_button_size:
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


class Obstruction:
    color = (127, 127, 127)

    def __init__(self):
        coordinates = (random.randint(obstruction_size, width - obstruction_size),
                       random.randint(obstruction_size, height - obstruction_size))

        while is_collision_obstruction(coordinates, snake.head) or \
                is_collision_obstruction(coordinates, length_reducing_food.coordinates) or \
                is_collision_obstruction(coordinates, length_increasing_food.coordinates) or \
                is_collision_obstruction(coordinates, speed_reducing_food.coordinates) or \
                is_collision_obstruction(coordinates, speed_increasing_food.coordinates) or \
                is_collision_obstruction(coordinates, bonus_food.coordinates) or \
                coordinates[0] < 130 and coordinates[1] < 70:
            coordinates = (random.randint(obstruction_size, width - obstruction_size),
                           random.randint(obstruction_size, height - obstruction_size))

        self.coordinates = (coordinates[0], coordinates[1], obstruction_size,
                            obstruction_size)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.coordinates)


def count_distance(coordinates1, coordinates2):
    return int(((coordinates1[0] - coordinates2[0]) ** 2 + (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5)


def count_distance_from_turn(turn_coordinates, coordinates):
    return int((abs((2 * snake_size) ** 2 - count_distance(turn_coordinates, coordinates) ** 2)) ** 0.5)


def create_obstructions(number):
    for i in range(number):
        obstructions.append(Obstruction())


def is_collision_obstruction(obstruction_coordinates, object_coordinates):
    if obstruction_coordinates[0] < object_coordinates[0] - snake_size < obstruction_coordinates[0] + obstruction_size:
        if obstruction_coordinates[1] < object_coordinates[1] - snake_size < \
                obstruction_coordinates[1] + obstruction_size:
            return True
        if obstruction_coordinates[1] < object_coordinates[1] + snake_size < \
                obstruction_coordinates[1] + obstruction_size:
            return True
    if obstruction_coordinates[0] < object_coordinates[0] + snake_size < obstruction_coordinates[0] + obstruction_size:
        if obstruction_coordinates[1] < object_coordinates[1] - snake_size < \
                obstruction_coordinates[1] + obstruction_size:
            return True
        if obstruction_coordinates[1] < object_coordinates[1] + snake_size < \
                obstruction_coordinates[1] + obstruction_size:
            return True

    return False


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
running = True
is_alive = True
is_paused = False

length_increasing_food_color = (135, 234, 0)
length_reducing_food_color = (240, 128, 128)
speed_increasing_food_color = (102, 205, 170)
speed_reducing_food_color = (240, 230, 140)
bonus_food_color = (255, 215, 0)

number_of_obstructions = 0
obstructions = []

food_size = 6
bonus_food_size = 8

obstruction_size = 40

snake_size = 7

lives = 3
last_length = 0

play_button_size = 70
play_button_coordinates = (width // 2, height // 2 + 50)

pause_button_size = 10
pause_button_color = (200, 200, 200)
pause_button_coordinates = (width - 15, 15)

length_increasing_food = LengthIncreasingFood()
length_reducing_food = LengthReducingFood()
speed_increasing_food = SpeedIncreasingFood()
speed_reducing_food = SpeedReducingFood()
bonus_food = BonusFood()

is_bonus = False

snake = Snake()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 40)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and is_alive and not is_paused:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != 0 and snake.direction != 2:
                if len(snake.turns) > 0:
                    if count_distance(snake.head, snake.turns[-1][0]) > 2 * snake_size:
                        snake.turns.append((snake.head, snake.direction))
                        snake.direction = 0
                else:
                    snake.turns.append((snake.head, snake.direction))
                    snake.direction = 0
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 1 and \
                    snake.direction != 3:
                if len(snake.turns) > 0:
                    if count_distance(snake.head, snake.turns[-1][0]) > 2 * snake_size:
                        snake.turns.append((snake.head, snake.direction))
                        snake.direction = 1
                else:
                    snake.turns.append((snake.head, snake.direction))
                    snake.direction = 1
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 0 and \
                    snake.direction != 2:
                if len(snake.turns) > 0:
                    if count_distance(snake.head, snake.turns[-1][0]) > 2 * snake_size:
                        snake.turns.append((snake.head, snake.direction))
                        snake.direction = 2
                else:
                    snake.turns.append((snake.head, snake.direction))
                    snake.direction = 2
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 1 and \
                    snake.direction != 3:
                if len(snake.turns) > 0:
                    if count_distance(snake.head, snake.turns[-1][0]) > 2 * snake_size:
                        snake.turns.append((snake.head, snake.direction))
                        snake.direction = 3
                else:
                    snake.turns.append((snake.head, snake.direction))
                    snake.direction = 3
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (count_distance(event.pos, play_button_coordinates)) <= play_button_size and not is_alive:
                lives = 3
                is_alive = True

                length_increasing_food = LengthIncreasingFood()
                length_reducing_food = LengthReducingFood()
                speed_increasing_food = SpeedIncreasingFood()
                speed_reducing_food = SpeedReducingFood()

                snake = Snake()
            if (count_distance(event.pos, pause_button_coordinates)) <= pause_button_size and is_alive:
                if is_paused:
                    is_paused = False
                else:
                    is_paused = True
    if is_alive:
        screen.fill((255, 255, 255))
        length_increasing_food.draw()
        length_reducing_food.draw()
        speed_increasing_food.draw()
        speed_reducing_food.draw()
        if is_bonus:
            bonus_food.draw()
        snake.draw()

        for obstruction in obstructions:
            obstruction.draw()

        score = font.render("Score " + str(snake.score), True, (0, 0, 0))
        lives_on_screen = font.render("Lives " + str(lives), True, (0, 0, 0))
        screen.blit(score, (10, 10))
        screen.blit(lives_on_screen, (10, 40))

        pygame.draw.circle(screen, pause_button_color, pause_button_coordinates, pause_button_size, 2)

        if not is_paused:
            snake.move()

            pygame.draw.rect(screen, pause_button_color, (width - 19, 10, 3, 10))
            pygame.draw.rect(screen, pause_button_color, (width - 14, 10, 3, 10))

            if count_distance(length_increasing_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_length_increasing_food()
                length_increasing_food = LengthIncreasingFood()
                length_increasing_food.draw()

                if snake.length % 2 != 0:
                    if number_of_obstructions < 20:
                        number_of_obstructions = (snake.length - 5) // 2
                    obstructions = []
                    create_obstructions(number_of_obstructions)

            if count_distance(length_reducing_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_length_reducing_food()
                length_reducing_food = LengthReducingFood()
                length_reducing_food.draw()

                if snake.length % 2 != 0:
                    if number_of_obstructions < 20:
                        number_of_obstructions = (snake.length - 5) // 2
                    obstructions = []
                    create_obstructions(number_of_obstructions)

            if count_distance(speed_increasing_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_speed_increasing_food()
                speed_increasing_food = SpeedIncreasingFood()
                speed_increasing_food.draw()

            if count_distance(speed_reducing_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_speed_reducing_food()
                speed_reducing_food = SpeedReducingFood()
                speed_reducing_food.draw()

            if is_bonus:
                if (pygame.time.get_ticks() - bonus_food.ticks) / 1000 >= 10:
                    is_bonus = False
                    bonus_food = BonusFood()
            else:
                if (pygame.time.get_ticks() - bonus_food.ticks) / 1000 >= 20:
                    is_bonus = True
                    bonus_food.set_timer()

            if is_bonus and count_distance(bonus_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_bonus_food()
                bonus_food = BonusFood()
                is_bonus = False

            if snake.is_collision() or snake.length == 0:
                lives = lives - 1
                last_length = snake.length
                snake = Snake()
                if last_length > 0:
                    snake.length = last_length
                else:
                    snake.length = 1
                if lives <= 0:
                    is_alive = False
                death_screen = pygame.Surface(size)
                death_screen.fill((255, 0, 0))
                death_screen.set_alpha(150)
                screen.blit(death_screen, (0, 0))
                pygame.display.flip()
                time.sleep(0.5)

            clock.tick(snake.fps)
        else:
            pygame.draw.polygon(screen, pause_button_color, ((width - 18, 10), (width - 11, 14), (width - 18, 19)))

    else:
        screen.fill((255, 255, 255))
        text = font.render("Игра окончена", True, (0, 0, 0))
        screen.blit(text, (width // 2 - 130, height // 2 - 150))
        score = font.render(str(snake.score), True, (0, 0, 0))
        screen.blit(score, (width // 2 - 10, height // 2 - 90))

        playText = font2.render("Играть", True, (0, 0, 0))

        pygame.draw.circle(screen, 'red', play_button_coordinates, play_button_size)
        screen.blit(playText, (width // 2 - 43, height // 2 + 40))

    print(snake.turns)
    pygame.display.flip()

pygame.quit()
