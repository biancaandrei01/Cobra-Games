# importarea librariei pygame pentru instrumentele GUI
import pygame

# initializarea fontului pygame
pygame.font.init()

# setarea ferestrei principale
screen = pygame.display.set_mode((600, 800))

# titlul ferestrei si iconita jocului
pygame.display.set_caption("Sudoku")
img = pygame.image.load('icon.png')
pygame.display.set_icon(img)

x = 0
y = 0
dif = 600 / 9
val = 0
poz = []
# tabla prestabilita de Sudoku
grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]
grid_s = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]  # copia tablei prestabilite pe care facem rezolvarea

# preluarea unor fonturi de test pentru uz ulterior
font1 = pygame.font.SysFont("courier", 28, bold=True)
font2 = pygame.font.SysFont("courier", 20)


def get_cord(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif


# evidentierea cu galben a celulei selectate
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 255, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 255, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


# evidentierea cu rosu a celulei selectate
def draw_red_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 26, 26), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 26, 26), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


# functie pentru desenarea liniilor si umplerea celulelor cu culoarea si valorile specifice
def draw():
    # desenarea numerelor si umplerea celulelor cu culoare
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != 0 and [i, j] not in poz:
                # umplerea celulei cu mov inchis
                pygame.draw.rect(screen, (170, 128, 255), (i * dif, j * dif, dif + 1, dif + 1))

                # umplerea celulei cu numerele presabilite
                text1 = font1.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text1, (i * dif + 25, j * dif + 15))

            elif grid[i][j] != 0 and [i, j] in poz:
                # umplerea celulei cu un mov deschis
                pygame.draw.rect(screen, (221, 204, 255), (i * dif, j * dif, dif + 1, dif + 1))

                # umplerea celulei cu numere rosii, introduse de utilizator
                text1 = font1.render(str(grid[i][j]), True, (255, 0, 0))
                screen.blit(text1, (i * dif + 25, j * dif + 15))

    # desenarea liniilor verticale si orizonatele ce formeaza tabla de Sudoku
    for i in range(len(grid) + 1):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (600, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 600), thick)


# afisare eroare cand o valoare introdusa de afla deja pe aceeasi linie/coloana/casuta
def raise_error1():
    text1 = font1.render("Wrong value, try again!", True, (153, 0, 0))
    screen.blit(text1, (10, 700))


# afisare eroare cand o valoare introdusa nu este cifra/r-resetare/enter-rezolvare
def raise_error2():
    text1 = font1.render("Invalid value, try again!", True, (153, 0, 0))
    screen.blit(text1, (10, 700))


# verificare daca valoarea introdusa pe tabla nu se afla deja pe aceeasi linie/coloana/casuta
def valid(m, i, j, val):
    for it in range(len(m)):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    it = i // 3
    jt = j // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False
    return True


# verificare daca valorile introduse sunt aceleasi cu cele din solutia finala
def check(sol, inp):
    for i in range(len(sol)):
        for j in range(len(sol)):
            if sol[i][j] != inp[i][j]:
                return False
    return True


# validarea solutiei introduse si afisarea in celule
def valid_solution(sol, inp):
    for i in range(len(sol)):
        for j in range(len(sol)):
            if sol[i][j] == inp[i][j] and [i, j] not in poz:  # valorile prestabilite pe care le avem in ambele matrici
                # umplerea celulei cu mov inchis
                pygame.draw.rect(screen, (179, 179, 255), (i * dif, j * dif, dif + 1, dif + 1))

                # umplerea celulei cu cifre negre (cifre prestabilite)
                text1 = font1.render(str(sol[i][j]), True, (0, 0, 0))
                screen.blit(text1, (i * dif + 25, j * dif + 15))
            elif sol[i][j] == inp[i][j] and [i, j] in poz:  # valorile introduse de noi la fel cu cele din solutia finala
                # umplerea celulei cu verde (raspuns corect)
                pygame.draw.rect(screen, (128, 255, 128), (i * dif, j * dif, dif + 1, dif + 1))

                # umplerea celulei cu cifre albe (cifre introduse de utilizator)
                text1 = font1.render(str(sol[i][j]), True, (255, 255, 255))
                screen.blit(text1, (i * dif + 25, j * dif + 15))
            elif sol[i][j] != inp[i][j] and inp[i][j] != 0:
                # umplerea celulei cu rosu (raspuns gresit)
                pygame.draw.rect(screen, (255, 102, 102), (i * dif, j * dif, dif + 1, dif + 1))

                # umplerea celulei cu cifre albe (cifre introduse de utilizator)
                text1 = font1.render(str(sol[i][j]), True, (255, 255, 255))
                screen.blit(text1, (i * dif + 25, j * dif + 15))
            else:
                # umplerea celulei cu rosu (raspuns gresit)
                pygame.draw.rect(screen, (255, 102, 102), (i * dif, j * dif, dif + 1, dif + 1))

                # umplerea celulei cu cifre negre (cifre neintroduse de utilizator)
                text1 = font1.render(str(sol[i][j]), True, (0, 0, 0))
                screen.blit(text1, (i * dif + 25, j * dif + 15))
    # desenarea liniilor verticale si orizontale ce formeaza tabla de Sudoku
    for i in range(len(grid) + 1):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (600, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 600), thick)
    return


# rezolvarea tablei de Sudoku utilizand Algoritmul de Backtracking
def solve(sol, i, j):
    while sol[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    for it in range(1, 10):
        if valid(sol, i, j, it):
            sol[i][j] = it
            global x, y
            x = i
            y = j
            if solve(sol, i, j) == 1:
                return True
            else:
                sol[i][j] = 0
    return False


# afisarea instructiunilor jocului
def instruction():
    text1 = font2.render("PRESS R TO RESET TO DEFAULT", True, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO CORRECT", True, (0, 0, 0))
    screen.blit(text1, (10, 620))
    screen.blit(text2, (10, 650))


# afisarea mesajului de rezolvare corecta
def result():
    text1 = font1.render("Your answer is correct!", True, (0, 255, 0))
    screen.blit(text1, (10, 700))

# afisarea mesajului de rezolvare gresita
def wrong_result():
    text1 = font1.render("Wrong answer, try again!", True, (255, 0, 0))
    screen.blit(text1, (10, 700))


run = True
flag1 = 0  # = 1 evidentiaza casuta in care ne aflam
flag2 = 0  # = 1 verificarea jocului activata
flag3 = 0  # = 1 nu putem modifica celula evidentiata -> sa nu putem modifica valorile prestabilite
rs = 0  # = 1 resetare joc activata
error = 0  # = 1 rezolvare gresita

# mentine fereastra activa cat vrem sa jucam
while run:
    # umplerea fundalului ferestrei cu alb
    screen.fill((255, 255, 255))
    # verificarea evenimentelor din event.get()
    for event in pygame.event.get():
        # iesirea din joc
        if event.type == pygame.QUIT:
            run = False
            # preluarea pozitiei mouse-ului pentru inserarea valorilor
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 0  # pentru a verifica inainte de a colora celula ne aflam in tabla de Sudoku
            pos = pygame.mouse.get_pos()
            get_cord(pos)
            if 0 <= x <= 8 and 0 <= y <= 8:  # conditie sa ne aflam in tabla de Sudoku
                flag1 = 1
        # preluarea valorii daca o anumita tasta este apasata
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x > 0:  # conditie sa nu iasa din tabla
                    x -= 1
                    flag1 = 1
            elif event.key == pygame.K_RIGHT:
                if x < 8:  # conditie sa nu iasa din tabla
                    x += 1
                    flag1 = 1
            elif event.key == pygame.K_UP:
                if y > 0:  # conditie sa nu iasa din tabla
                    y -= 1
                    flag1 = 1
            elif event.key == pygame.K_DOWN:
                if y < 8:  # conditie sa nu iasa din tabla
                    y += 1
                    flag1 = 1
            elif event.key == pygame.K_1:
                val = 1
            elif event.key == pygame.K_2:
                val = 2
            elif event.key == pygame.K_3:
                val = 3
            elif event.key == pygame.K_4:
                val = 4
            elif event.key == pygame.K_5:
                val = 5
            elif event.key == pygame.K_6:
                val = 6
            elif event.key == pygame.K_7:
                val = 7
            elif event.key == pygame.K_8:
                val = 8
            elif event.key == pygame.K_9:
                val = 9
            elif event.key == pygame.K_RETURN:
                flag2 = 1
            # daca se apasa R, Sudoku revine la forma prestabilita
            elif event.key == pygame.K_r:
                fs = 0
                rs = 0
                error = 0
                flag2 = 0
                poz = []
                grid = [
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                ]
                grid_s = [
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                ]
            else:
                val = 'c'

    if flag2 == 1:
        solve(grid_s, 0, 0)
        if check(grid_s, grid):
            rs = 1
        else:
            error = 1
    else:
        # verificam daca avem o valoare prestabilita in celula in care ne aflam
        if grid_s[int(x)][int(y)] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            flag3 = 1
        else:
            flag3 = 0
        if val not in [0, 'c'] and flag3 == 0:
            poz.append([int(x), int(y)])
            if valid(grid, int(x), int(y), val):
                grid[int(x)][int(y)] = val
            else:
                grid[int(x)][int(y)] = val
                raise_error1()
                draw()
                draw_red_box()
                instruction()
                pygame.display.update()
                pygame.time.delay(100)
                grid[int(x)][int(y)] = 0
                # comentam daca vrem sa ne lase sa introducem o val care exista deja pe rand/coloana
        elif val == 'c' and flag3 == 0:
            raise_error2()
            draw()
            draw_red_box()
            instruction()
            pygame.display.update()
            pygame.time.delay(100)
        val = 0

    if error == 1:
        valid_solution(grid_s, grid)
        wrong_result()
    elif rs == 1:
        valid_solution(grid_s, grid)
        result()
    else:
        draw()
    if flag1 == 1:
        draw_box()
    instruction()

    # actualizare fereastra
    pygame.display.update()

# iesire din joc
pygame.quit()