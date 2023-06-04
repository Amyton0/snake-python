import pygame
import random


class Snake:
    def __init__(self):
        self.length = 5
        self.direction = 0
        self.turns = []
        self.head = (width // 2, height // 2)
        self.segments = []
        self.fps = 70

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
            pygame.draw.circle(screen, snake_color, segment, snake_size)

    def eat_length_increasing_food(self):
        self.length += 1

    def eat_length_reducing_food(self):
        self.length -= 1

    def eat_speed_increasing_food(self):
        self.fps += 10

    def eat_speed_reducing_food(self):
        self.fps -= 10

    def is_collision(self):
        if self.head[0] < snake_size or self.head[0] > width - snake_size or \
                self.head[1] < snake_size or self.head[1] > height - snake_size:
            return True

        for segment in self.segments[2:]:
            if count_distance(segment, self.head) < 2 * snake_size:
                return True

        return False


class Food:
    def __init__(self, effect):
        self.coordinates = (random.randint(food_size, width - food_size), random.randint(food_size, height - food_size))
        self.effect = effect

    def draw(self):
        if self.effect == "increase length":
            pygame.draw.circle(screen, length_increasing_food_color, self.coordinates, food_size)
        if self.effect == "reduce length":
            pygame.draw.circle(screen, length_reducing_food_color, self.coordinates, food_size)
        if self.effect == "increase speed":
            pygame.draw.circle(screen, speed_increasing_food_color, self.coordinates, food_size)
        if self.effect == "reduce speed":
            pygame.draw.circle(screen, speed_reducing_food_color, self.coordinates, food_size)


class Obstruction:
    color = (127, 127, 127,)

    def __init__(self, x0, y0, x1, y1):
        self.obstruction_coordinates = (x0, y0, x1, y1)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.obstruction_coordinates)


def count_distance(coordinates1, coordinates2):
    return int(((coordinates1[0] - coordinates2[0]) ** 2 + (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5)


def count_distance_from_turn(turn_coordinates, coordinates):
    return int(((2 * snake_size) ** 2 - count_distance(turn_coordinates, coordinates) ** 2) ** 0.5)


def is_collision_obstruction(obstruction_coordinates, snake_coordinates):
    if obstruction_coordinates[0] < snake_coordinates[0] + snake_size < obstruction_coordinates[3]:
        if obstruction_coordinates[4] > snake_coordinates[1] + snake_size > obstruction_coordinates[2]:
            return True


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
running = True
is_alive = True
is_paused = False

length_increasing_food_color = (135, 234, 0)
length_reducing_food_color = (240, 128, 128)
speed_increasing_food_color = (255, 165, 0)
speed_reducing_food_color = (240, 230, 140)

food_size = 6

snake_color = (53, 194, 102)
snake_size = 7

lives = 3
last_length = 0

play_button_size = 70
play_button_coordinates = (width // 2, height // 2 + 50)

pause_button_size = 10
pause_button_color = (200, 200, 200)
pause_button_coordinates = (width - 15, 15)

length_increasing_food = Food("increase length")
length_reducing_food = Food("reduce length")
speed_increasing_food = Food("increase speed")
speed_reducing_food = Food("reduce speed")

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
                snake.turns.append((snake.head, snake.direction))
                snake.direction = 0
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 1 and \
                    snake.direction != 3:
                snake.turns.append((snake.head, snake.direction))
                snake.direction = 1
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 0 and \
                    snake.direction != 2:
                snake.turns.append((snake.head, snake.direction))
                snake.direction = 2
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 1 and \
                    snake.direction != 3:
                snake.turns.append((snake.head, snake.direction))
                snake.direction = 3
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (count_distance(event.pos, play_button_coordinates)) <= play_button_size and not is_alive:
                lives = 3
                is_alive = True

                length_increasing_food = Food("increase length")
                length_reducing_food = Food("reduce length")
                speed_increasing_food = Food("increase speed")
                speed_reducing_food = Food("reduce speed")

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
        snake.draw()

        score = font.render("Score " + str(snake.length - 5), True, (0, 0, 0))
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
                length_increasing_food = Food("increase length")
                length_increasing_food.draw()

            if count_distance(length_reducing_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_length_reducing_food()
                length_reducing_food = Food("reduce length")
                length_reducing_food.draw()

            if count_distance(speed_increasing_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_speed_increasing_food()
                speed_increasing_food = Food("increase speed")
                speed_increasing_food.draw()

            if count_distance(speed_reducing_food.coordinates, snake.head) <= snake_size + food_size:
                snake.eat_speed_reducing_food()
                speed_reducing_food = Food("reduce speed")
                speed_reducing_food.draw()

            if snake.is_collision():
                lives = lives - 1
                last_length = snake.length
                snake = Snake()
                snake.length = last_length
                print(lives)
                if lives <= 0:
                    is_alive = False

            clock.tick(snake.fps)
        else:
            pygame.draw.polygon(screen, pause_button_color, ((width - 18, 10), (width - 11, 14), (width - 18, 19)))
    else:
        screen.fill((255, 255, 255))
        text = font.render("Игра окончена", True, (0, 0, 0))
        screen.blit(text, (width // 2 - 130, height // 2 - 150))
        score = font.render(str(snake.length - 5), True, (0, 0, 0))
        screen.blit(score, (width // 2 - 10, height // 2 - 90))

        playText = font2.render("Играть", True, (0, 0, 0))

        pygame.draw.circle(screen, 'red', play_button_coordinates, play_button_size)
        screen.blit(playText, (width // 2 - 43, height // 2 + 40))
    pygame.display.flip()

pygame.quit()
