import pygame as pg

class Graphics():
    RED = (255,0,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    WINDOW_HEIGHT = 900
    WINDOW_WIDTH = 800
    GRID_HEIGHT = int(3*WINDOW_WIDTH/4)
    GRID_WIDTH = int(3*WINDOW_WIDTH/4)
    def __init__(self):
        self.window = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.window.fill(self.WHITE)
        self.grid = pg.Surface((self.GRID_HEIGHT, self.GRID_WIDTH))
        self.grid.fill(self.WHITE)
        self.x_surface = pg.Surface((int(Symbol.WIDTH), int(Symbol.HEIGHT)))
        self.x_surface.fill(self.WHITE)
        self.o_surface = pg.Surface((int(Symbol.WIDTH), int(Symbol.HEIGHT)))
        self.o_surface.fill(self.WHITE)
        pg.init()
        pg.display.set_caption("Tic-Tac-Toe")
        pg.font.init()
        self.myfont = pg.font.SysFont('Comic Sans MS', 30)
        self.x_win_text = self.myfont.render('X Wins!', False, self.RED)
        self.o_win_text = self.myfont.render('O Wins!', False, self.BLUE)
        self.cat_game_text = self.myfont.render('Cat Game.', False, self.BLACK)
    def draw_grid(self):
        pg.draw.line(self.grid, self.BLACK, (int(self.GRID_WIDTH/3),0)    ,  (int(self.GRID_WIDTH/3)   , self.GRID_HEIGHT)      ,  5)
        pg.draw.line(self.grid, self.BLACK, (int(self.GRID_WIDTH*2/3),0)  ,  (int(self.GRID_WIDTH*2/3) , self.GRID_HEIGHT)      ,  5)
        pg.draw.line(self.grid, self.BLACK, (0,int(self.GRID_HEIGHT*2/3))  ,  (self.GRID_WIDTH, int(self.GRID_HEIGHT*2/3))                          ,  5)
        pg.draw.line(self.grid, self.BLACK, (0,int(self.GRID_HEIGHT/3))    ,  (self.GRID_WIDTH, int(self.GRID_HEIGHT/3))                          ,  5)
    def blit_grid(self):
        self.window.blit(self.grid, (int((self.WINDOW_WIDTH - self.GRID_HEIGHT)/2), int((self.WINDOW_WIDTH - self.GRID_WIDTH)/2)))
        if game.turn == 'x':
            self.window.blit(self.x_surface, (0,0))
        elif game.turn == 'o':
            self.window.blit(self.o_surface, (0,0))
    def draw_x_symbol(self):
        pg.draw.line(self.x_surface, self.RED, (0,0) , (Symbol.WIDTH, Symbol.HEIGHT), 10)
        pg.draw.line(self.x_surface, self.RED, (Symbol.WIDTH,0) , (0, Symbol.HEIGHT,), 10)
    def draw_o_symbol(self):
        center = int(Symbol.WIDTH / 2)
        pg.draw.circle(self.o_surface, self.BLUE, (center,center), 50, 5)
    def blit_winner(self):
        if game.winner == 'x':
            self.window.blit(self.x_win_text, (300, 800))
        elif game.winner == 'o':
            self.window.blit(self.o_win_text, (300, 800))
        elif game.winner == 'cat':
            self.window.blit(self.cat_game_text, (300, 800))            
    @staticmethod
    def pixelate(tup):
        x, y = tup
        return (Space.WIDTH * x, Space.HEIGHT * y)

    def blit_symbols(self):
        for space in Space.spaces:
            if space.symbol:
                symbol = space.symbol
                if symbol.type == 'x':
                    self.grid.blit(self.x_surface, symbol.center_in_space(self.pixelate(space.coords)))
                if symbol.type == 'o':
                    self.grid.blit(self.o_surface, symbol.center_in_space(self.pixelate(space.coords)))
        
class Game():
    def __init__(self):
        self.running = False
        self.set_spaces()
        self.turn = 'x'
        self.winner = None
        self.turn_count = 0
    def run(self):
        self.running = True
        while self.running:
            graphics.draw_grid()
            graphics.blit_grid()
            graphics.draw_x_symbol()
            graphics.draw_o_symbol()
            graphics.blit_symbols()
            graphics.blit_winner()
            pg.display.update()
            # print(pg.mouse.get_pos())
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.place_symbol()

    def set_spaces(self):
        for x in range(3):
            for y in range(3):
                Space.spaces.add(Space((x, y)))
    def change_turn(self):
        if self.turn == 'x':
            self.turn = 'o'
        else:
            self.turn = 'x'
    def place_symbol(self):
        for space in Space.spaces:
            if space.is_clicked():
                if not space.symbol:
                    space.symbol = Symbol(self.turn)
                    winner = self.return_winner()
                    if winner:
                        self.winner = winner
                    self.turn_count += 1
                    if self.turn_count >= 9 and winner != 'x' and winner != 'o':
                        self.winner = 'cat'
                    self.change_turn()
                    
    def return_winner(self):
        list_of_x_symbol_coords = set()
        list_of_o_symbol_coords = set()
        for space in Space.spaces:
            if space.symbol:
                if space.symbol.type == 'x':
                    list_of_x_symbol_coords.add(space.coords)
                elif space.symbol.type == 'o':
                    list_of_o_symbol_coords.add(space.coords)
        def is_winner(list_of_symbols):
            sets = []
            sets.append(set([(0,0),(1,0),(2,0)])) # Top Win
            sets.append(set([(0,1),(1,1),(2,1)])) # Middle Horizonal Win
            sets.append(set([(0,2),(1,2),(2,2)])) # Bottom Win
            sets.append(set([(0,0),(0,1),(0,2)])) # Left Win
            sets.append(set([(1,0),(1,1),(1,2)])) # Middle Vertical Win
            sets.append(set([(2,0),(2,1),(2,2)])) # Right Win
            sets.append(set([(0,0),(1,1),(2,2)])) # Diagonal Win 1
            sets.append(set([(0,2),(1,1),(2,0)])) # Diagonal Win 2
            for current_set in sets:
                if current_set.issubset(list_of_symbols):
                    return True
        if is_winner(list_of_x_symbol_coords):
            return 'x'
        elif is_winner(list_of_o_symbol_coords):
            return 'o'
class Space():
    spaces = set()
    HEIGHT = int(Graphics.GRID_HEIGHT/3)
    WIDTH = HEIGHT
    def __init__(self, coords):
        self.coords = coords
        self.symbol = None
    def get_max_min(self):
        x_coord, y_coord = Graphics.pixelate(self.coords)
        buffer = (Graphics.WINDOW_WIDTH - Graphics.GRID_WIDTH) / 2
        x_max = x_coord + self.WIDTH + buffer
        y_max = y_coord + self.HEIGHT + buffer
        x_min, y_min = x_coord + buffer, y_coord + buffer
        return (x_max, y_max, x_min, y_min)
    def is_clicked(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x_max, y_max, x_min, y_min = self.get_max_min()
        if x_min <= mouse_x <= x_max and y_min <= mouse_y <= y_max:
            return True

class Symbol():
    WIDTH = Space.WIDTH/2
    HEIGHT = Space.HEIGHT/2
    def __init__(self, type):
        self.type = type
        self.location = None
    def set_location(self, location):
        self.location = location
    def center_in_space(self, origin_tuple):
        x_origin, y_origin = origin_tuple
        return ((Space.WIDTH - self.WIDTH) / 2 + x_origin, (Space.HEIGHT - self.HEIGHT) / 2 + y_origin)

def main():
    global graphics
    graphics = Graphics()
    global game
    game = Game()
    game.run()

if __name__ == "__main__":
    main()