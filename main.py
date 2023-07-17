import random
import copy
import pygame
import time
# creating assets
tetromino = []
object1 = "..X." \
           "..X." \
           "..X." \
           "..X."
object2 =  "..X." \
           ".XX." \
           ".X.." \
           "...."
object3 =  ".X.." \
           ".XX." \
           "..X." \
           "...."
object4 = "...." \
           ".XX." \
           ".XX." \
           "...."
object5 =  "..X." \
           ".XX." \
           "..X." \
           "...."
object6 = "...." \
           ".XX." \
           "..X." \
           "..X."
object7 = "...." \
           ".XX." \
           ".X.." \
           ".X.."

tetromino.append(object1)
tetromino.append(object2)
tetromino.append(object3)
tetromino.append(object4)
tetromino.append(object5)
tetromino.append(object6)
tetromino.append(object7)
# print(tetromino[1])
#
# exit(0)
# rotate
def rotate(px, py, r):
    if r == 0:
        return py*4+px
    elif r == 1:
        return 12+py-4*px
    elif r == 2:
        return 15-4*py-px
    elif r == 3:
        return 3-py+4*px


# Field
fieldwidth = 12
fieldheight = 18

pField = [0 for i in range(fieldwidth*fieldheight)]
# print(len(pField))
for x in range(fieldwidth):
    for y in range(fieldheight):
        # print(y*fieldwidth+x)
        pField[y*fieldwidth+x] = 9 if (x == 0 or x == fieldwidth-1 or y == fieldheight-1) else 0

# print(pField)
# game window
pygame.init()
window_width = 480
window_height = 720
window_title = "Tetris"

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)

# judge if the position of the piece fit the rule
def doesPieceFit(nTetromino, nrotation, positionX, positionY):
    for px in range(4):
        for py in range(4):
            # get the index
            pi = rotate(px, py, nrotation)
            # print(pi)
            # exit(0)
            #get index into field
            fi = int((positionY+py)*12+positionX+px)
            # print(fi)
            # exit(0)
            if (positionX+px >= 0) and (positionX+px <= 11):
                if (positionY+py >= 0) and (positionY+py <= 18):
                    if tetromino[nTetromino][pi] == 'X' and ((pField[fi] == 1) or (pField[fi] == 9)):
                        return False

    return True

# Game logic stuff======================================================
gameover = False
# which piece is falling
nCurrentPiece = random.randint(0, 6)
# is it rotate
nCurrentRotation = 0
nCurrentX = fieldwidth/2
nCurrentY = 0

bKey = []
clock = pygame.time.Clock()
fps = 60
wait_time = 100

fall_time = 0.5
last_fall_time = time.time()  # 初始化最后一次下降时间点
vline = []

nPieceCount = 1
nscore = 0
# Render output ===================================================

while not gameover:
    # game timing =====================================================
    clock.tick(fps)
    current_time = time.time()  # 当前时间
    # input ===========================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # 用户按下了左箭头键
                # print("左箭头键被按下")
                # bKey = 1
                bKey.append(1)
            elif event.key == pygame.K_RIGHT:
                # 用户按下了右箭头键
                # print("右箭头键被按下")
                # bKey = 2
                bKey.append(2)
            elif event.key == pygame.K_DOWN:
                # 用户按下了下箭头键
                # print("下箭头键被按下")
                # bKey = 3
                bKey.append(3)
            elif event.key == pygame.K_z:
                # 用户按下了上箭头键
                # print("上箭头键被按下")
                # bKey = 4
                bKey.append(4)
    # Game logic ======================================================
    if (1 in bKey) and doesPieceFit(nCurrentPiece, nCurrentRotation, nCurrentX-1, nCurrentY):
        nCurrentX = nCurrentX - 1
        bKey.remove(1)
        # bKey=0

    if (2 in bKey) and doesPieceFit(nCurrentPiece, nCurrentRotation, nCurrentX+1, nCurrentY):
        nCurrentX = nCurrentX + 1
        bKey.remove(2)
        # bKey=0

    if (3 in bKey) and doesPieceFit(nCurrentPiece, nCurrentRotation, nCurrentX, nCurrentY+1):
        nCurrentY = nCurrentY + 1
        bKey.remove(3)
        # bKey=0

    if (4 in bKey) and doesPieceFit(nCurrentPiece, (nCurrentRotation+1)%4, nCurrentX, nCurrentY):
        nCurrentRotation += 1
        nCurrentRotation %= 4
        bKey.remove(4)
        # bKey=0

    if current_time - last_fall_time >= fall_time:
        # 执行方块的下降操作
        if doesPieceFit(nCurrentPiece, nCurrentRotation, nCurrentX, nCurrentY + 1):
            nCurrentY += 1
            last_fall_time = current_time  # 更新最后一次下降时间点
        else:
            # lock the current piece into the field.
            for px in range(4):
                for py in range(4):
                    if tetromino[nCurrentPiece][rotate(px, py, nCurrentRotation)] == 'X':
                        # print(len(pField))
                        # print(int((nCurrentY+py)*fieldwidth+nCurrentX+px))
                        pField[int((nCurrentY+py)*fieldwidth+nCurrentX+px)] = 1
            # check if we get any lines.
            for py in range(4):
                if nCurrentY+py<fieldheight-1:
                    bline = True
                    for px in range(1, fieldwidth):
                        if pField[(nCurrentY+py)*fieldwidth+px] == 0:
                            bline = False
                    if bline:
                        # remove the line
                        for px in range(1, fieldwidth-1):
                            pField[(nCurrentY + py) * fieldwidth + px] = 8
                        vline.append(nCurrentY+py)
            # Finally, we choose next piece
            nCurrentX = fieldwidth//2
            nCurrentY = 0
            nCurrentRotation = 0
            nCurrentPiece = random.randint(0, 6)
            nPieceCount += 1
            nscore += 100
            # check if piece fits.
            gameover = not doesPieceFit(nCurrentPiece, nCurrentRotation, nCurrentX, nCurrentY)
    # Fill in black background
    screen.fill((0, 0, 0))
    # Draw field pygame.draw.rect(screen, (255, 0, 0), (block_x, block_y, block_size, block_size))
    # pygame.draw.rect(screen, (255, 0, 0), (0, 0, 10, 10))
    for x in range(fieldwidth):
        for y in range(fieldheight):
            # print(y*fieldwidth+x)
            if pField[y*fieldwidth+x] == 9:
                pygame.draw.rect(screen, (255, 255, 179), (x*40, y*40, 40, 40))
            if pField[y*fieldwidth+x] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (x*40, y*40, 40, 40))
            if pField[y*fieldwidth+x] == 8:
                pygame.draw.rect(screen, (255, 209, 224), (x*40, y*40, 40, 40))
    # draw current piece
    else:
        for px in range(4):
            for py in range(4):
                if tetromino[nCurrentPiece][rotate(px, py, nCurrentRotation)] == 'X':
                    pygame.draw.rect(screen, (255, 255, 255), ((nCurrentX+px) * 40, (nCurrentY+py) * 40, 40, 40))

    if len(vline) != 0:
        pField_copy = copy.deepcopy(pField)
        nscore += 114514*len(vline)
        for dy in vline:
            for dx in range(1, fieldwidth-1):
                pField[dy*fieldwidth+dx] = 0
        for dy in range(0, vline[0]):
            for dx in range(1, fieldwidth-1):
                pField[(dy + len(vline)) * fieldwidth + dx] = 0
        for dy in range(0, vline[0]):
            for dx in range(1, fieldwidth-1):
                if pField_copy[dy*fieldwidth+dx] == 1:
                    pField[(dy+len(vline))*fieldwidth+dx] = 1
        vline = []

    if (nPieceCount%10 == 0) and fall_time>0.2:
        fall_time -= 0.01


    font = pygame.font.Font(None, 36)  # 创建字体对象
    score_text = font.render("Score: " + str(nscore), True, (255, 135, 207))  # 渲染分数文本
    screen.blit(score_text, (10, 10))  # 在屏幕上绘制分数文本的位置

    # pygame.time.delay(wait_time)
    pygame.display.update()



pygame.quit()

# print(tetromino)






