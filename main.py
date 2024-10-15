import pygame
import random
import time


pygame.init()
pygame.mixer.init()


screen_width = 640
screen_height = 520
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Лабиринт')

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Параметры стен и дверей
line_width = 10
line_gap = 40
line_offset = 20
door_width = 40
max_openings_per_line = 5

# Параметры и стартовая позиция игрока
player_radius = 10
player_speed = 2
player_x = screen_width - 12
player_y = screen_height - 60

# Загрузка и масштабирование фонового изображения
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height - 40))

# Загрузка и настройка музыки
pygame.mixer.music.load('game_music.mp3')  # Основная музыка
victory_sound = pygame.mixer.Sound('victory_sound.mp3')  # Звук победы
defeat_sound = pygame.mixer.Sound('defeat_sound.mp3')  # Звук поражения

# Начало воспроизведения фоновой музыки
pygame.mixer.music.play(-1)  # (-1) для бесконечного повторения

# Переменные для управления звуком и паузой
is_muted = False
is_paused = False

# Рисуем стены и двери
lines = []
for i in range(0, screen_width, line_gap):
    # Генерируем количество открытий в стене
    num_openings = random.randint(1, max_openings_per_line)
    # Определяем границы открытий
    openings = sorted(
        random.sample(range(line_offset + door_width, screen_height - line_offset - door_width - 40), num_openings))

    # Создаем стены с дверями
    last_opening_bottom = 0
    for opening_top in openings:
        # Верхняя часть стены
        lines.append(pygame.Rect(i, last_opening_bottom, line_width, opening_top - last_opening_bottom))
        last_opening_bottom = opening_top + door_width
    # Нижняя часть стены
    lines.append(pygame.Rect(i, last_opening_bottom, line_width, screen_height - last_opening_bottom - 40))  # Уменьшаем высоту нижней части стены

# Функция для отображения текста
def show_message(message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.fill(black)
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(5000)


# Функция для отображения сообщения с временем и кнопками
def show_time_message(elapsed_time):
    font = pygame.font.Font(None, 36)
    message = f"Время: {elapsed_time:.2f} секунд"
    text = font.render(message, True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))


    screen.fill(black)
    screen.blit(text, text_rect)

    # Размеры кнопок
    button_width = 200
    button_height = 50

    # Создаем прямоугольники для кнопок с заданными размерами
    retry_button_rect = pygame.Rect((screen_width - button_width) // 2, screen_height // 2 + 10, button_width,
                                    button_height)  # Кнопка "Попробовать еще раз"
    exit_button_rect = pygame.Rect((screen_width - button_width) // 2, screen_height // 2 + 70, button_width,
                                   button_height)  # Кнопка "Выйти"

    # Рисуем кнопки
    pygame.draw.rect(screen, blue, retry_button_rect)  # Кнопка "Попробовать еще раз"
    pygame.draw.rect(screen, blue, exit_button_rect)  # Кнопка "Выйти"

    # Рисуем текст на кнопках с учетом центрирования
    retry_text = font.render("Еще раз", True, white)
    exit_text = font.render("Выйти", True, white)
    retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)  # Центрируем текст для кнопки "Еще раз"
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)  # Центрируем текст для кнопки "Выйти"
    screen.blit(retry_text, retry_text_rect)  # Рисуем текст на кнопке "Еще раз"
    screen.blit(exit_text, exit_text_rect)  # Рисуем текст на кнопке "Выйти"

    pygame.display.update()  # Обновляем экран

    # Ожидание нажатия кнопки
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button_rect.collidepoint(mouse_pos):
                    return True  # Вернуться в игру
                elif exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()  # Выйти из игры

# Координаты для кнопок паузы и звука
pause_button_rect = pygame.Rect(screen_width - 210, screen_height - 35, 80, 30)
mute_button_rect = pygame.Rect(screen_width - 120, screen_height - 35, 80, 30)

font = pygame.font.Font(None, 36)  # Шрифт для кнопок
clock = pygame.time.Clock()

# Переменная для отслеживания времени
start_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Проверка нажатия кнопки паузы
            if pause_button_rect.collidepoint(mouse_pos):
                is_paused = not is_paused  # Переключаем состояние паузы
                if is_paused:
                    pygame.mixer.music.pause()  # Останавливаем музыку
                else:
                    if not is_muted:  # Если звук не выключен, возобновляем музыку
                        pygame.mixer.music.unpause()  # Возобновляем музыку
            # Проверка нажатия кнопки звука
            elif mute_button_rect.collidepoint(mouse_pos):
                is_muted = not is_muted  # Переключаем состояние звука
                if is_muted:
                    pygame.mixer.music.pause()  # Останавливаем музыку
                    victory_sound.stop()  # Останавливаем звук победы
                    defeat_sound.stop()  # Останавливаем звук поражения
                else:
                    pygame.mixer.music.unpause()  # Возобновляем музыку

    if is_paused:
        continue  # Если игра на паузе, пропускаем остальную логику

    # Передвижение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_radius:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < screen_width - player_radius:
        player_x += player_speed
    elif keys[pygame.K_UP] and player_y > player_radius:
        player_y -= player_speed
    elif keys[pygame.K_DOWN] and player_y < screen_height - player_radius - 40:  # Учитываем место для кнопок
        player_y += player_speed

    # Проверка столкновений игрока со стенами
    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
    collided = False

    for line in lines:
        if line.colliderect(player_rect):
            # Проверяем, если столкновение произошло со стеной
            if line.height > door_width:  # Если это не дверь
                collided = True
                # Обрабатываем столкновение
                if player_x < line.left:
                    player_x = line.left - player_radius  # Уходим влево
                elif player_x > line.right:
                    player_x = line.right + player_radius  # Уходим вправо
                elif player_y < line.top:
                    player_y = line.top - player_radius  # Уходим вверх
                elif player_y > line.bottom:
                    player_y = line.bottom + player_radius  # Уходим вниз
            else:
                # Если столкновение с дверью, игрок может пройти
                collided = False

    # Проверка столкновения с нижней стеной (поражение)
    if collided:
        pygame.mixer.music.pause()  # Останавливаем текущую музыку
        if not is_muted:  # Проверяем, не отключен ли звук
            defeat_sound.play()  # Проигрываем звук поражения
        elapsed_time = time.time() - start_time  # Вычисляем прошедшее время
        if show_time_message(elapsed_time):  # Показать сообщение с временем
            # Сбрасываем начальные параметры для новой игры
            player_x = screen_width - 12
            player_y = screen_height - 60
            start_time = time.time()  # Сбрасываем таймер

            # Проверяем состояние звука при перезапуске игры
            if not is_muted:  # Если звук не отключен
                pygame.mixer.music.play(-1)  # Включаем музыку заново

            continue

    # Проверка столкновения с левой стеной (победа)
    if player_rect.colliderect(pygame.Rect(0, 0, line_width, screen_height)):
        pygame.mixer.music.stop()  # Останавливаем текущую музыку
        if not is_muted:  # Проверяем, не отключен ли звук
            victory_sound.play()  # Проигрываем звук победы
        elapsed_time = time.time() - start_time  # Вычисляем прошедшее время
        if show_time_message(elapsed_time):  # Показать сообщение с временем
            # Сбрасываем начальные параметры для новой игры
            player_x = screen_width - 12
            player_y = screen_height - 60
            start_time = time.time()  # Сбрасываем таймер

            # Проверяем состояние звука при перезапуске игры
            if not is_muted:  # Если звук не отключен
                pygame.mixer.music.play(-1)  # Включаем музыку заново

            continue

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка стен и игрока
    for line in lines:
        pygame.draw.rect(screen, green, line)
    pygame.draw.circle(screen, red, (player_x, player_y), player_radius)

    # Отрисовка кнопок
    pygame.draw.rect(screen, blue, pause_button_rect)  # Кнопка паузы
    pygame.draw.rect(screen, blue, mute_button_rect)  # Кнопка звука

    # Создаем текст для кнопок
    pause_text = font.render("Пауза", True, white)
    mute_text = font.render("Звук", True, white)

    # Центрируем текст на кнопках
    pause_text_rect = pause_text.get_rect(center=pause_button_rect.center)
    mute_text_rect = mute_text.get_rect(center=mute_button_rect.center)


    screen.blit(pause_text, pause_text_rect)
    screen.blit(mute_text, mute_text_rect)

    # Очистка области для таймера
    pygame.draw.rect(screen, black, (10, screen_height - 35, 200, 30))

    # Отображение времени на экране
    elapsed_time = time.time() - start_time
    time_text = font.render(f"Время: {elapsed_time:.2f} сек", True, white)
    screen.blit(time_text, (10, screen_height - 35))  # Рисуем время в нижнем левом углу

    pygame.display.update()  # Обновляем экран
    clock.tick(60)  # Устанавливаем 60 кадров в секунду
