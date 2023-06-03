from main import count_distance
from main import Snake


def test_distance_between_dots():
    assert count_distance((0, 0), (0, 0)) == 0
    assert count_distance((0, 0), (0, 1)) == 1
    assert count_distance((0, 0), (1, 0)) == 1
    assert count_distance((0, 0), (0, -1)) == 1
    assert count_distance((0, 0), (-1, 0)) == 1
    assert count_distance((0, 0), (1, 1)) == 1
    assert count_distance((0, 0), (3, 4)) == 5
    assert count_distance((0, 0), (-1, 1)) == 1
    assert count_distance((0, 0), (1, -1)) == 1
    assert count_distance((2, 3), (5, 7)) == 5
    assert count_distance((2, 3), (-1, -1)) == 5


def test_moving_snake():
    snake = Snake()
    snake.head = (400, 299)
    snake.direction = 0
    snake.length = 5
    for i in range(100):
        snake.move()
    assert snake.segments == [(400, 199), (400, 213), (400, 227), (400, 241), (400, 255)]

    snake = Snake()
    snake.head = (547, 333)
    snake.turns = [((447, 295), 0), ((547, 295), 1)]
    snake.direction = 2
    snake.length = 5
    snake.move()
    snake.move()
    assert snake.segments == [(547, 335), (547, 321), (547, 307), (540, 295), (526, 295)]

    snake = Snake()
    snake.head = (251, 341)
    snake.turns = [((305, 403), 1), ((305, 286), 0), ((229, 286), 3), ((229, 341), 2)]
    snake.direction = 1
    snake.length = 14
    snake.move()
    assert snake.segments == [(252, 341), (238, 341), (229, 331), (229, 317), (229, 303), (229, 289), (242, 286),
                              (256, 286), (270, 286), (284, 286), (298, 286), (305, 298), (305, 312), (305, 326)]

