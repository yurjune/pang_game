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

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    for w in weapons:
        screen.blit(weapon, [w[0], w[1]])
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()

pygame.quit()
