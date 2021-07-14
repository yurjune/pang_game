import pygame
import os
############################################################
# 기본 초기화 (반드시)
pygame.init()

# 화면 크기
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀
pygame.display.set_caption('Honey Pang Game')

# FPS
clock = pygame.time.Clock()

############################################################
# 1. 사용자 게임 초기화(배경, 캐릭터 정보(크기, 위치, 속도..), 폰트, 시간..)
# 경로 설정
current_path = os.path.dirname(__file__)    # 현재 파일의 위치 반환
image_path = os.path.join(current_path, 'images')   # images 폴더 위치 반환

# 배경화면, 640*480
background = pygame.image.load(os.path.join(image_path, 'background.png'))

# 스테이지, 640*50
stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]    # 나중에 계산을 위해 하는거

# 캐릭터, 60*33
character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - stage_height - character_height

# 이동할 좌표
# 키 충돌 방지위해 두개로 나눔
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

# 캐릭터 속도
character_speed = 5

# 무기, 20*430
weapon = pygame.image.load(os.path.join(image_path, 'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 여러개이므로 무기의 위치를 리스트로 만들기
weapons = []

# 무기 속도
weapon_speed = 10

# 공
ball_images = [
    pygame.image.load(os.path.join(image_path, 'balloon1.png')),
    pygame.image.load(os.path.join(image_path, 'balloon2.png')),
    pygame.image.load(os.path.join(image_path, 'balloon3.png')),
    pygame.image.load(os.path.join(image_path, 'balloon4.png'))
]

# 공 크기에 따른 최초 속도
ball_speed_y = [-18, -15, -12, -9]

# 공들
balls = []
balls.append({
    'pos_x': 50,    # 공의 시작 위치
    'pos_y': 50,
    'img_idx': 0,   # 공의 이미지 인덱스
    'to_x': 3,      # 공의 이동 방향
    'to_y': -6,
    'init_spd_y': ball_speed_y[0]    # y 최초 속도
})

running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 이동 키 입력
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE:
                # 무기의 위치를 캐릭터의 중앙으로 설정
                weapon_x_pos = character_x_pos + character_width / 2 - weapon_width / 2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        # 이동 키 떼기
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    # 3. 캐릭터 위치 정의

    # 캐릭터 위치 정의
    character_to_x = character_to_x_LEFT + character_to_x_RIGHT
    character_x_pos += character_to_x

    # 바깥으로 안가게
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 정의
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿으면 소멸: 화면 밖으로 벗어난 무기는 리스트로 저장안함
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']
        
        # 공 스펙
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 경계값 처리
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val['to_x'] = ball_val['to_x'] * -1
        
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val['to_y'] = ball_val['init_spd_y']
        # 그 외의 경우 속도 증가
        else: 
            ball_val['to_y'] += 0.5 

        # 공의 위치에 위 값 반영
        ball_val['pos_x'] += ball_val['to_x']
        ball_val['pos_y'] += ball_val['to_y']

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    for w in weapons:
        screen.blit(weapon, [w[0], w[1]])
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    for idx, val in enumerate(balls):
        # 실제 값은 pos_x
        ball_pos_x = val['pos_x']
        ball_pos_y = val['pos_y']
        ball_img_idx = val['img_idx']
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    pygame.display.update()

pygame.quit()
