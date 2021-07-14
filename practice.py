import pygame
import os
pygame.init()

# 화면
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode(size=(screen_width, screen_height))

# 타이틀
pygame.display.set_caption('Honey Pang Game')

# FPS
clock = pygame.time.Clock()

# 배경설정
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

background = pygame.image.load(os.path.join(image_path, 'background.png'))

# 스테이지
stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터
character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - stage_height - character_height

# 이동할 좌표
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

# 캐릭터 속도
character_speed = 5

# 무기
weapon = pygame.image.load(os.path.join(image_path, 'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 무기 리스트
weapons = []

# 무기 속도
weapon_speed = 10

# 공
ball_image = [
    pygame.image.load(os.path.join(image_path, 'balloon1.png')),
    pygame.image.load(os.path.join(image_path, 'balloon2.png')),
    pygame.image.load(os.path.join(image_path, 'balloon3.png')),
    pygame.image.load(os.path.join(image_path, 'balloon4.png'))
]

# 공 리스트
balls = []

# 공크기에 따른 최초속도
ball_speed_y = [-18, -15, -12, -9]

# 최초 발생하는 공
balls.append({
    'pos_x': 50,
    'pos_y': 50,
    'img_idx': 0,
    'to_x': 3,
    'to_y': -6,
    'init_spd_y': ball_speed_y[0] 
})

# 충돌 시 사라질 공, 무기
weapon_to_remove = -1
ball_to_remove = -1

# 폰트
game_font = pygame.font.Font(None, 40)
game_result = ''

# 총 시간
total_time = 30

# 시작 시간
start_ticks = pygame.time.get_ticks()

# 이벤트 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed
                character_to_x_RIGHT = 0

            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed
                character_to_x_LEFT = 0
            
            elif event.type == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width / 2 - weapon_width / 2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0

            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    # 캐릭터 위치 정의
    character_to_x = character_to_x_LEFT + character_to_x_RIGHT
    character_x_pos += character_to_x

    # 캐릭터 경계 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 재정의
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # 무기 경계 처리
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        # 공 스펙
        ball_size = ball_image.get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]


    # 화면 표시
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for w in weapons:
        screen.blit(weapon, (w[0], w[1]))

    screen.blit(stage, (0, screen_height - stage_height))
    pygame.display.update()

# 게임종료 메시지
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 종료
# pygame.time.delay(2000)
pygame.quit()