/*
Запит для Gemini:
Створи програму мовою C++ для симуляції клітинних автоматів. Кожен автомат є об'єктом, що належить до класу CA. Цей клас повинен мати поля: x, y, live та функцію rule(), що описує правила автомата. Розроби функцію step(), яка щоразу повертає оновлену матрицю 10 на 10 з цими автоматами. Візуалізація повинна виконуватись в консолі Windows.
*/
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <windows.h> // Необхідно для Windows-консолі (Sleep, system("cls"))

const int GRID_SIZE = 28;

// Клас клітинного автомата
class CA {
public:
    int x;
    int y;
    bool live;
    bool nextState; // Тимчасовий стан для синхронного оновлення

    CA(int posX = 0, int posY = 0, bool isAlive = false)
        : x(posX), y(posY), live(isAlive), nextState(isAlive) {}

    // Метод для визначення майбутнього стану за правилами гри "Життя"
    void rule(const std::vector<std::vector<CA>>& grid) {
        int aliveNeighbors = 0;

        // Перевірка всіх 8 сусідніх клітин
        for (int dx = -1; dx <= 1; ++dx) {
            for (int dy = -1; dy <= 1; ++dy) {
                if (dx == 0 && dy == 0) continue; // Пропускаємо саму клітину

                int nx = x + dx;
                int ny = y + dy;

                // Перевірка меж матриці 10x10
                if (nx >= 0 && nx < GRID_SIZE && ny >= 0 && ny < GRID_SIZE) {
                    if (grid[nx][ny].live) {
                        aliveNeighbors++;
                    }
                }
            }
        }

        // Застосування правил клітинного автомата:
        if (live) {
            // Жива клітина виживає тільки якщо має 2 або 3 живих сусідів
            nextState = (aliveNeighbors == 2 || aliveNeighbors == 3);
        } else {
            // Мертва клітина оживає, якщо має точно 3 живих сусідів
            nextState = (aliveNeighbors == 3);
        }
    }

    // Застосування нового стану
    void update() {
        live = nextState;
    }
};

// Тип для зручності використання матриці 10x10
using Grid10x10 = std::vector<std::vector<CA>>;

// Функція step, яка обробляє та повертає оновлену матрицю
Grid10x10 step(Grid10x10 grid) {
    // 1. Обчислюємо наступний стан для кожного автомата
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            grid[i][j].rule(grid);
        }
    }

    // 2. Оновлюємо поточний стан усіх автоматів
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            grid[i][j].update();
        }
    }

    return grid;
}

// Функція для візуалізації матриці в консолі Windows
void printGrid(const Grid10x10& grid) {
    // Переміщуємо курсор у початок консолі для уникнення миготіння екрана
    COORD coord = {0, 0};
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);

    std::cout << "--- Клітинний автомат (10x10) ---\n\n";
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            // Виводимо '█' для живих клітин та '.' для мертвих
            std::cout << (grid[i][j].live ? "O " : ". ");
        }
        std::cout << "\n";
    }
    std::cout << "\nНатисніть Ctrl+C для виходу...\n";
}

int main() {
    // Налаштування кодування для коректного відображення символу '█'
    SetConsoleOutputCP(1251);

    // Очищення екрана перед початком
    system("cls");

    // Ініціалізація генератора випадкових чисел
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    // Створення початкової матриці 10х10 з випадковими станами
    Grid10x10 grid(GRID_SIZE, std::vector<CA>(GRID_SIZE));
    for (int i = 0; i < GRID_SIZE; ++i) {
        for (int j = 0; j < GRID_SIZE; ++j) {
            bool randomLife = (std::rand() % 3 == 0); // ~33% шанс бути живим
            grid[i][j] = CA(i, j, randomLife);
        }
    }

    // Головний цикл симуляції
    while (true) {
        printGrid(grid);       // Візуалізація
        grid = step(grid);     // Виклик функції step() для отримання оновленої матриці
        Sleep(300);            // Затримка 300 мс для Windows
    }

    return 0;
}
