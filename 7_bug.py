balls = [1, 2, 3, 4]
weapons = [11, 22, 3, 44]

for ball_idx, ball_value in enumerate(balls):
    print('balls: ', ball_value)

    for weapon_idx, weapon_value in enumerate(weapons):
        print('weapons: ', weapon_value)
        
        # 충돌 발생
        if ball_value == weapon_value:
            print('공과 무기가 충돌')
            break   # 안쪽 for문만 탈출한다.
    
    # 바깥쪽 for문도 탈출하도록 코드 수정
    else: # 계속 게임을 진행
        continue    # 안쪽 for문의 조건이 맞지 않으면 바깥쪽 for문 계속 수행
    print('바깥 for문 break 확인')
    break   # 안쪽 for문에서 break로 만나면 여기로 진입하여 2중 for문 한꺼번 에 탈출
