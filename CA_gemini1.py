"""
Promt для Gemini:
Створи Python-програму для симуляції клітинних автоматів. Кожен автомат є об'єктом, що належить до класу CA. Цей клас повинен мати атрибути: x, y, live та функцію rule(), що описує правила автомата. Розроби функцію step(), яка щоразу повертає оновлену матрицю 10 на 10 з цими автоматами.
"""

import random


class CA:

    def __init__(self, x: int, y: int, live: bool = False):
        self.x = x
        self.y = y
        self.live = live

    def rule(self, live_neighbors_count: int) -> bool:
        """Визначає стан клітини на наступному кроці за правилами Конвея:

        - Жива клітина з 2 або 3 живими сусідами виживає.
        - Мертва клітина з точно 3 живими сусідами оживає.
        - В усіх інших випадках клітина помирає або залишається мертвою.
        """
        if self.live:
            return live_neighbors_count in (2, 3)
        else:
            return live_neighbors_count == 3


def count_live_neighbors(grid: list[list[CA]], x: int, y: int) -> int:
    """Підраховує кількість живих сусідів для клітини (x, y) з урахуванням замкнених кордонів (тор)."""
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue

            # Замкнені кордони (клітина за краєм поле зв'язана з протилежним боком)
            nx = (x + dx) % rows
            ny = (y + dy) % cols

            if grid[nx][ny].live:
                count += 1

    return count


def step(grid: list[list[CA]]) -> list[list[CA]]:
    """Приймає поточну матрицю клітинних автоматів і повертає оновлену матрицю 10х10."""
    rows = len(grid)
    cols = len(grid[0])

    # Спочатку вираховуємо нові стани для всіх клітин
    next_states = [[False for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = count_live_neighbors(grid, r, c)
            next_states[r][c] = grid[r][c].rule(neighbors)

    # Оновлюємо стани об'єктів у матриці
    for r in range(rows):
        for c in range(cols):
            grid[r][c].live = next_states[r][c]

    return grid


def display_grid(grid: list[list[CA]]) -> None:
    """Виводить матрицю у консоль (■ — жива, . — мертва)."""
    for row in grid:
        print(" ".join("■" if cell.live else "." for cell in row))
    print("-" * 20)


# === Приклад використання ===
if __name__ == "__main__":
    SIZE = 10

    # Створюємо початкову матрицю 10 на 10 із випадковим заповненням
    grid = [
        [CA(x=r, y=c, live=random.choice([True, False])) for c in range(SIZE)]
        for r in range(SIZE)
    ]

    print("Початковий стан:")
    display_grid(grid)

    # Запускаємо 3 кроки симуляції
    for i in range(1, 4):
        grid = step(grid)
        print(f"Крок {i}:")
        display_grid(grid)