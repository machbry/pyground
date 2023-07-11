def fibonacci_generator(n_max: int = 10):
    u, v = 0, 1
    for n in range(n_max + 1):
        yield u
        u, v = v, u + v


def square_generator(numbers):
    for n in numbers:
        yield n, n**2


for i, j in square_generator(fibonacci_generator()):
    print(i, j)
