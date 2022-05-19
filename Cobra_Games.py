# importare pygame pentru instrumente GUI
import pygame
# importare sys pentru accesarea variabilelor si a functiilor ce interactioneaza puternic cu interpretorul
import sys
# preluarea clasei Button din fisierul button.py
from button import Button
# importare subprocess pentru posibilitatea rularii altor fisiere
import subprocess

pygame.init()

# initializare fereastra
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cobra Games")
BG = pygame.image.load("Background.png")


def get_font(size):
    return pygame.font.Font("font.ttf", size)


# apelarea fisierului cu X si 0
def xSI0():
    subprocess.call("Xsi0.py", shell=True)


# apelarea fisierului cu Sudoku
def sudoku():
    subprocess.call("Sudoku.py", shell=True)


# meniul principal al jocului
def main_menu():
    # ruleaza pana cand utilizatorul apasa quit
    while True:
        # formarea meniului principal
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("COBRA GAMES", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 130))

        xSI0_BUTTON = Button(image=pygame.image.load("Xsi0_Rect.png"), pos=(640, 290),
                             text_input="Xsi0", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SUDOKU_BUTTON = Button(image=pygame.image.load("Sudoku_Rect.png"), pos=(640, 440),
                               text_input="Sudoku", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit_Rect.png"), pos=(640, 590),
                             text_input="Quit", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # evidentierea butonului asupra caruia se afla utilizatorul cu mouse-ul
        for button in [xSI0_BUTTON, SUDOKU_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # activarea suprogramelor/exit-ului in urma optiunii selectate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if xSI0_BUTTON.checkForInput(MENU_MOUSE_POS):
                    xSI0()
                if SUDOKU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sudoku()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        # actualizarea ferestrei
        pygame.display.update()

# rularea programului
main_menu()
