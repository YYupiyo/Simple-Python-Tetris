# Подробная инструкция по установке

## Для Windows

### Способ 1: Установка Python с официального сайта
1. Скачайте Python с [официального сайта](https://www.python.org/downloads/)
2. Запустите установщик, обязательно отметьте "Add Python to PATH"
3. Откройте командную строку (Win + R, введите `cmd`)
4. Установите pygame: `pip install pygame`
5. Запустите игру: `python tetris.py`

### Способ 2: Использование пакетного менеджера Chocolatey
```cmd
choco install python
pip install pygame
python tetris.py

Для Linux (Ubuntu/Debian)
# Установка Python и pip
sudo apt update
sudo apt install python3 python3-pip

# Установка pygame
pip3 install pygame

# Запуск игры
python3 tetris.py

Для macOS
# Установка через Homebrew
brew install python3

# Установка pygame
pip3 install pygame

# Запуск игры
python3 tetris.py

Проверка установки
После установки проверьте, что все работает:
python --version
# Должно показать Python 3.8 или выше

python -c "import pygame; print(pygame.version.ver)"
# Должно показать версию pygame
Решение проблем
Ошибка "python not found"
Используйте python3 вместо python

Ошибка прав доступа при установке pygame
Используйте: pip install --user pygame

Игра запускается, но нет графического окна
Убедитесь, что у вас установлена графическая среда
