import pgzrun  # chama biblioteca pgZero
import sys  # chama a biblioteca pra "saída" do jogo
import random  # chama biblioteca "random"
import math  # chama biblioteca matemática do python

from pgzero.actor import Actor

# --- DEFININDO TAMANHO DA JANELA DO JOGO (DIMENSÃO) ---
WIDTH = 800  # largura
HEIGHT = 450  # altura

TITLE = "CirBot"  # título da janela

# --- ESTADO DO JOGO ---
game_state = "menu"  # estado do jogo: menu, playing, math_challenge, game_over, win
player_game = "playing"  # estado do jogador: playing, hit

# --- PONTUAÇÃO E VIDA ---
score = 0
score = 0
max_player_health = 100
player_health = max_player_health
low_health_challenge_offered = False

# --- LISTAS DE ATORES ---
enemy_actors = []  # Lista para armazenar os atores inimigos
attacks = []  # Lista para armazenar os ataques

# --- DESAFIO MATEMÁTICO ---
math_question = ""
math_answer = ""
user_answer = ""

# --- TEMA E CORES DO JOGO ---
dark_green = '#0e8c38'
light_green = '#065328'

# --- BOTÕES DO MENU E GAME OVER ---
btn_start = Actor('start', (WIDTH / 2, HEIGHT / 2 + 80))
btn_exit = Actor('exitgame', (WIDTH - 50, 50))
btn_restart = Actor('start', (WIDTH / 2, HEIGHT / 2 + 80))  # Reutiliza a imagem 'start'

sound_button_pos = (WIDTH - 120, 50)
btn_mute = Actor('mute', sound_button_pos)
btn_sound_on = Actor('onsound', sound_button_pos)
sound_is_on = True

# --- PERSONAGENS E SEUS "FRAMES"(SPRITES) ---

# Robô (jogador principal):
frame_Happy = ["happy1", "happy2", "happy3", "happy4"]
frame_Sad = ["sad1", "sad2", "sad3", "sad4"]
frame_Fearful = ["fearful1", "fearful2", "fearful3", "fearful4"]
frame_Angry = ["angry1", "angry2", "angry3", "angry4"]

# Robô (inimigos):
frame_Enemy1 = ["enemy1walk1", "enemy1walk2", "enemy1walk3", "enemy1walk4"]
frame_Enemy2 = ["enemy2walk1", "enemy2walk2", "enemy2walk3", "enemy2walk4"]
frame_Enemy3 = ["enemy3walk1", "enemy3walk2", "enemy3walk3", "enemy3walk4"]

# Ator do robô
robot = Actor(frame_Happy[0])
robot.frames = frame_Happy
robot.frame_index = 0

# --- VARIÁVEIS DA TELA ---
limite_esquerdo = -44
limite_direito = 840
limite_superior = -38
limite_inferior = 486

# Variáveis de Animação
anim_speed = 0.2
counter = 0.0

# música no começo do jogo
music.play('music_game')
music.set_volume(0.4)


# --- FUNÇÕES ---

def spawn_enemies():
    if game_state != "playing":
        return

    num_to_spawn = random.randint(1, 15)
    for _ in range(num_to_spawn):
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        x, y = 0, 0
        if edge == 'top':
            x = random.randint(limite_esquerdo, limite_direito)
            y = limite_superior - 50
        elif edge == 'bottom':
            x = random.randint(limite_esquerdo, limite_direito)
            y = limite_inferior + 50
        elif edge == 'left':
            x = limite_esquerdo - 50
            y = random.randint(limite_superior, limite_inferior)
        elif edge == 'right':
            x = limite_direito + 50
            y = random.randint(limite_superior, limite_inferior)

        frames = enemy()
        new_enemy = Actor(frames[0], (x, y))
        new_enemy.frames = frames
        new_enemy.frame_index = 0
        new_enemy.counter = 0.0
        new_enemy.speed = random.uniform(0.5, 1.5)
        enemy_actors.append(new_enemy)


def start_game():
    global counter, player_game, enemy_actors, attacks, game_state, score, player_health, low_health_challenge_offered

    # para a música do menu ao iniciar o jogo
    if sound_is_on and music.is_playing('music_game'):
        music.stop()

    robot.pos = (WIDTH / 2, HEIGHT / 2)
    robot.frames = frame_Happy
    robot.frame_index = 0
    robot.image = robot.frames[robot.frame_index]
    counter = 0.0
    player_game = "playing"
    game_state = "playing"
    score = 0
    player_health = max_player_health
    low_health_challenge_offered = False

    enemy_actors.clear()
    attacks.clear()
    clock.unschedule(spawn_enemies)
    clock.schedule_interval(spawn_enemies, 15.0)

def enemy():
    return frame_Enemy2


def expression_robot_main():
    global robot, player_game

    enemies_count = len(enemy_actors)
    previous_frames = robot.frames

    if player_game == "hit":
        robot.frames = frame_Sad
    elif enemies_count >= 5:
        robot.frames = frame_Angry
    elif enemies_count > 0 and enemies_count < 5:
        robot.frames = frame_Fearful
    elif enemies_count <= 0:
        robot.frames = frame_Happy

    if robot.frames != previous_frames:
        robot.frame_index = 0
        robot.image = robot.frames[robot.frame_index]


def update():
    if game_state == "playing":
        update_game()


def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "math_challenge":
        draw_math_challenge()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "win":
        draw_win()


def draw_menu():
    screen.fill(light_green)
    screen.draw.text(
        "CirBot",
        center=(WIDTH / 2, HEIGHT / 2 - 50),
        fontname="gameofsquids",
        fontsize=100,
        color="white"
    )
    btn_start.draw()
    btn_exit.draw()

    if sound_is_on:
        btn_mute.draw()
    else:
        btn_sound_on.draw()


def draw_game():
    screen.fill(dark_green)
    robot.draw()

    for e in enemy_actors:
        e.draw()

    for attack in attacks:
        screen.draw.filled_rect(attack['rect'], "yellow")

    health_bar_width = 150
    health_bar_height = 20
    health_percentage = player_health / max_player_health
    current_health_width = health_bar_width * health_percentage

    screen.draw.filled_rect(Rect(10, 10, health_bar_width, health_bar_height), "red")
    if current_health_width > 0:
        screen.draw.filled_rect(Rect(10, 10, current_health_width, health_bar_height), "yellow")

    screen.draw.text(f"Score: {score}", topleft=(10, 35), fontsize=30, color="white")


def draw_math_challenge():
    draw_game()
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 150))
    box = Rect(WIDTH / 4, HEIGHT / 4, WIDTH / 2, HEIGHT / 2)
    screen.draw.filled_rect(box, "white")
    screen.draw.text(math_question, center=box.center, fontsize=60, color="black")
    screen.draw.text(user_answer, midbottom=box.midbottom, fontsize=50, color="blue")


def draw_game_over():
    screen.fill(light_green)
    screen.draw.text(
        "Game Over",
        center=(WIDTH / 2, HEIGHT / 2 - 50),
        fontname="gameofsquids",
        fontsize=100,
        color="white"
    )
    screen.draw.text(
        f"score: {score}",
        center=(WIDTH / 2, HEIGHT / 2 + 20),
        fontname="gameofsquids",
        fontsize=40,
        color="white"
    )
    btn_restart.draw()
    btn_exit.draw()


def draw_win():
    screen.fill(light_green)
    screen.draw.text(
        "Você Venceu!",
        center=(WIDTH / 2, HEIGHT / 2 - 50),
        fontname="gameofsquids",
        fontsize=100,
        color="white"
    )
    screen.draw.text(
        f"score: {score}",
        center=(WIDTH / 2, HEIGHT / 2 + 20),
        fontname="gameofsquids",
        fontsize=40,
        color="white"
    )
    btn_restart.draw()
    btn_exit.draw()


def update_game():
    global counter, player_game, game_state, score, player_health, low_health_challenge_offered, math_question, math_answer, user_answer

    if score >= 1000:
        game_state = "win"
        music.stop()
        return

    expression_robot_main()

    if player_health <= 0:
        game_state = "game_over"
        music.stop()
        return

    moving = False
    if player_game == "playing":
        if keyboard.left:
            robot.x -= 2
            moving = True
        if keyboard.right:
            robot.x += 2
            moving = True
        if keyboard.up:
            robot.y -= 2
            moving = True
        if keyboard.down:
            robot.y += 2
            moving = True
        if keyboard.ESCAPE:
            sys.exit()

    if robot.left < limite_esquerdo:  robot.left = limite_esquerdo
    if robot.right > limite_direito:  robot.right = limite_direito
    if robot.top < limite_superior:   robot.top = limite_superior
    if robot.bottom > limite_inferior: robot.bottom = limite_inferior

    if moving:
        counter += anim_speed
        robot.frame_index = int(counter) % len(robot.frames)
        robot.image = robot.frames[robot.frame_index]
    else:
        robot.frame_index = 0
        robot.image = robot.frames[robot.frame_index]
        counter = 0.0

    attacks_in_screen = []
    for attack in attacks:
        attack['rect'].x += attack['vx']
        attack['rect'].y += attack['vy']
        if attack['rect'].right > limite_esquerdo and \
                attack['rect'].left < limite_direito and \
                attack['rect'].bottom > limite_superior and \
                attack['rect'].top < limite_inferior:
            attacks_in_screen.append(attack)
    attacks[:] = attacks_in_screen

    enemies_to_remove = []
    attacks_to_remove = []

    for e in enemy_actors:
        if player_game == "playing":
            dx = robot.x - e.x
            dy = robot.y - e.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx = dx / dist
                dy = dy / dist
                e.x += dx * e.speed
                e.y += dy * e.speed

        e.counter += anim_speed
        e.frame_index = int(e.counter) % len(e.frames)
        e.image = e.frames[e.frame_index]

        for attack in attacks:
            if e.colliderect(attack['rect']):
                enemies_to_remove.append(e)
                attacks_to_remove.append(attack)

    colliding_enemy_index = robot.collidelist(enemy_actors)
    if colliding_enemy_index != -1 and player_game == "playing":
        enemy_hit = enemy_actors[colliding_enemy_index]
        enemies_to_remove.append(enemy_hit)
        player_health -= 25

        if player_health <= 0:
            player_game = "hit"
            expression_robot_main()
        elif player_health <= 50 and not low_health_challenge_offered:
            low_health_challenge_offered = True
            game_state = "math_challenge"
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            math_question = f"{num1} + {num2} = ?"
            math_answer = str(num1 + num2)
            user_answer = ""

    for e in set(enemies_to_remove):
        if e in enemy_actors:
            enemy_actors.remove(e)
            score += 10

    unique_attacks_to_remove = []
    for attack in attacks_to_remove:
        if attack not in unique_attacks_to_remove:
            unique_attacks_to_remove.append(attack)

    for a in unique_attacks_to_remove:
        if a in attacks:
            attacks.remove(a)


def on_key_down(key):
    global game_state, player_game, user_answer, player_health, low_health_challenge_offered

    if game_state == "playing" and player_game == "playing":
        attack_speed = 5
        attack_played = False
        if key == keys.W:
            rect = Rect(robot.centerx - 2, robot.top - 20, 4, 20)
            attack = {'rect': rect, 'vx': 0, 'vy': -attack_speed}
            attacks.append(attack)
            attack_played = True
        elif key == keys.A:
            rect = Rect(robot.left - 20, robot.centery - 2, 20, 4)
            attack = {'rect': rect, 'vx': -attack_speed, 'vy': 0}
            attacks.append(attack)
            attack_played = True
        elif key == keys.S:
            rect = Rect(robot.centerx - 2, robot.bottom, 4, 20)
            attack = {'rect': rect, 'vx': 0, 'vy': attack_speed}
            attacks.append(attack)
            attack_played = True
        elif key == keys.D:
            rect = Rect(robot.right, robot.centery - 2, 20, 4)
            attack = {'rect': rect, 'vx': attack_speed, 'vy': 0}
            attacks.append(attack)
            attack_played = True

        if attack_played:
            sounds.attack_robot.play()

    elif game_state == "math_challenge":
        if key in range(keys.K_0, keys.K_9 + 1):
            user_answer += str(key - keys.K_0)
        if key == keys.BACKSPACE:
            user_answer = user_answer[:-1]
        if key == keys.RETURN:
            if user_answer == math_answer:
                print("Resposta correta! Vida recuperada.")
                player_health = max_player_health
                low_health_challenge_offered = False
            else:
                print("Resposta incorreta!")
                player_health -= 25
            game_state = "playing"


def on_mouse_down(pos):
    global sound_is_on, game_state

    if game_state == "menu":
        if btn_start.collidepoint(pos):
            if sound_is_on: sounds.click_mouse.play()
            print("Botão INICIAR clicado! Começando o jogo...")
            start_game()

    if game_state in ["menu", "game_over", "win"]:
        if btn_exit.collidepoint(pos):
            if sound_is_on: sounds.click_mouse.play()
            print("Saindo do jogo...")
            sys.exit()

    if game_state == "menu":
        if sound_is_on and btn_mute.collidepoint(pos):
            sounds.click_mouse.play()
            print("Som desativado!")
            sound_is_on = False
            music.pause()
        elif not sound_is_on and btn_sound_on.collidepoint(pos):
            print("Som ativado!")
            sound_is_on = True
            music.unpause()

    if game_state in ["game_over", "win"]:
        if btn_restart.collidepoint(pos):
            if sound_is_on: sounds.click_mouse.play()
            print("Botão REINICIAR clicado! Começando o jogo...")
            start_game()
            if sound_is_on:
                music.play('music_game', -1)
                music.set_volume(0.4)


pgzrun.go()