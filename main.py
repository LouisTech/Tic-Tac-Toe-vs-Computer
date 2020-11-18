import pygame as pg
from pygame.locals import *
import sys

# initialise pygame
pg.init()

# stores if it's x's or o's turn
# XO = "x"

Winner = None
draw = None

# paremeters for the game setup
header_height = 100
dis_height = 500 + header_height
dis_width = int((dis_height - header_height) * (4/3))
dis_center = int(dis_width/2)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (250, 0, 0)
line_color = black
fps = 30
mainClock = pg.time.Clock()
font = pg.font.SysFont(None, 25)

# sprites
x_img = pg.image.load("images/Xsprite.png")
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.image.load("images/Osprite.png")
o_img = pg.transform.scale(o_img, (80, 80))
# initialise the board
# board = [[None]*3, [None]*3, [None]*3]


# initialise the screen and window
screen = pg.display.set_mode((dis_width, dis_height), 0, 32)
pg.display.set_caption("Naughts and Crosses")

click = False


class Button():
    def __init__(self, color, x, y, width, height, text='', text_color=black):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color

    def draw(self, surface, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pg.draw.rect(surface, outline, (self.x-2, self.y -
                                            2, self.width+4, self.height+4), 0)

        pg.draw.rect(surface, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            text = font.render(self.text, 1, self.text_color)
            surface.blit(text, (self.x + int((self.width/2 - text.get_width()/2)),
                                self.y + int((self.height/2 - text.get_height()/2))))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Board():
    def __init__(self):
        self.board = [[None]*3, [None]*3, [None]*3]
        self.xo = "x"
        # height of a square
        self.y_third = ((dis_height-header_height)/3)
        # y co-ord of first horizontal line
        self.hoz_third = self.y_third+header_height
        self.hoz_third2 = self.y_third*2+header_height
        # x co-ord of first vertical line
        self.x_third = dis_width / 3
        self.win = False

    def draw_board(self):
        # draw vertical lines
        pg.draw.line(screen, line_color, (self.x_third, header_height),
                     (self.x_third, dis_height), 7)
        pg.draw.line(screen, line_color, (self.x_third * 2, header_height),
                     (self.x_third * 2, dis_height), 7)

        # draw horizontal lines
        pg.draw.line(screen, line_color, (0, header_height),
                     (dis_width, header_height), 3)
        pg.draw.line(screen, line_color, (0, self.hoz_third),
                     (dis_width, self.hoz_third), 7)
        pg.draw.line(screen, line_color, (0, self.hoz_third2),
                     (dis_width, self.hoz_third2), 7)

    def check_win(self):
        sixth_height = self.y_third / 2
        sixth_width = self.x_third / 2
        for i in range(0, 3):
            # check horizontal for win
            if ((self.board[i][0] is not None) and self.board[i][0] == self.board[i][1] == self.board[i][2]):
                winner = self.board[i][0]
                pg.draw.line(screen, (250, 0, 0),
                             (0, sixth_height+header_height +
                              (i*self.y_third)),
                             (dis_width, sixth_height+header_height +
                              (i*self.y_third)),
                             4)
                self.win = True
            # check vertical for win
            if ((self.board[0][i] is not None) and self.board[0][i] == self.board[1][i] == self.board[2][i]):
                winner = self.board[0][i]
                pg.draw.line(screen, (250, 0, 0), (sixth_width + (i*self.x_third),
                                                   header_height), (sixth_width + (i*self.x_third), dis_height), 4)
                self.win = True

            # check diagonal wins
            if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] is not None):
                # game won diagonally left to right
                winner = self.board[0][0]
                pg.draw.line(screen, (250, 70, 70),
                             (0, header_height), (dis_width, dis_height), 4)
                self.win = True

            if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] is not None):
                # game won diagonally right to left
                winner = self.board[0][2]
                pg.draw.line(screen, (250, 70, 70), (0, dis_height),
                             (dis_width, header_height), 4)
                self.win = True

    def user_click(self):
        x, y = pg.mouse.get_pos()
        if self.win == False:
            if y > header_height:
                # get column of mouse click (1-3)
                if(x < self.x_third):
                    col = 1
                elif (x < self.x_third * 2):
                    col = 2
                elif(x < dis_width):
                    col = 3
                else:
                    col = None

                # get row of mouse click (1-3)
                if(y < self.hoz_third):
                    row = 1
                elif (y < self.hoz_third2):
                    row = 2
                elif(y < dis_height):
                    row = 3
                else:
                    row = None

                if(row and col and self.board[row-1][col-1] is None):
                    self.draw_XO(row, col)

    def draw_XO(self, row, col):
        if row == 1:
            posy = header_height + 40
        if row == 2:
            posy = self.hoz_third + 40
        if row == 3:
            posy = self.hoz_third2 + 40
        if col == 1:
            posx = 40
        if col == 2:
            posx = self.x_third + 40
        if col == 3:
            posx = (2*self.x_third) + 40

        self.board[row-1][col-1] = self.xo

        if(self.xo == 'x'):
            screen.blit(x_img, (posx, posy))
            self.xo = 'o'
        else:
            screen.blit(o_img, (posx, posy))
            self.xo = 'x'
        pg.display.update()
        self.check_win()

    def reset(self, mode):
        self.win = False
        if mode == "pvp":
            pvp()
        else:
            pve()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


cpu_btn = Button(blue, dis_center-100,
                 int(dis_height/2), 200, 50, '1 Player', white)
pvp_btn = Button(blue, dis_center-100,
                 int(2*dis_height/3), 200, 50, '2 Players', white)


def main_menu():
    running = True
    while running:

        pg.display.update()
        # draw the main menu screen
        screen.fill(white)
        cpu_btn.draw(screen)
        pvp_btn.draw(screen)

        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if pvp_btn.isOver(pos):
                    pvp()
                if cpu_btn.isOver(pos):
                    pve()

            if event.type == pg.MOUSEMOTION:
                if pvp_btn.isOver(pos):
                    pvp_btn.color = (52, 198, 235)
                else:
                    pvp_btn.color = (52, 183, 235)
                if cpu_btn.isOver(pos):
                    cpu_btn.color = (52, 198, 235)
                else:
                    cpu_btn.color = (52, 183, 235)

        mainClock.tick(60)


home_btn = Button((52, 183, 235), 0, 0, 50, 50, 'H', white)
reset_btn = Button((52, 183, 235), 0, 50, 50, 50, 'R', white)


def pvp():
    running = True
    screen.fill(white)
    board = Board()
    board.draw_board()
    while running:
        home_btn.draw(screen)
        reset_btn.draw(screen)
        pg.display.update()
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if home_btn.isOver(pos):
                    main_menu()
                elif reset_btn.isOver(pos):
                    board.reset("pvp")
                else:
                    board.user_click()
            if event.type == pg.MOUSEMOTION:
                if home_btn.isOver(pos):
                    home_btn.color = (52, 198, 235)
                else:
                    home_btn.color = (52, 183, 235)
                if reset_btn.isOver(pos):
                    reset_btn.color = (52, 198, 235)
                else:
                    reset_btn.color = (52, 183, 235)
        pg.display.update()
        mainClock.tick(60)


def pve():
    running = True
    screen.fill(white)
    home_btn.draw(screen)
    reset_btn.draw(screen)
    board = Board()
    board.draw_board()
    while running:
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if home_btn.isOver(pos):
                    main_menu()
            if event.type == pg.MOUSEMOTION:
                if home_btn.isOver(pos):
                    home_btn.color = (52, 198, 235)
                else:
                    home_btn.color = (52, 183, 235)
        pg.display.update()
        mainClock.tick(60)


main_menu()
