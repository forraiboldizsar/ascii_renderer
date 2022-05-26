
from objects import *




class scene_2d:

    def __init__(self,main_rect,num_grid) -> None:
        self.main_rect = main_rect
        self.arrlen_x = len(num_grid[0])
        self.arrlen_y = len(num_grid)
        self.num_grid = num_grid    
        self.grid = self.create_grid()    
        self.angle = 0

        self.initialize_player()
        self.set_backround_functions()
        self.set_screen_data()
    


    def create_grid(self):
        
        cells = []
        
        self.cell_w = self.main_rect.w / self.arrlen_x
        self.cell_h = self.main_rect.h / self.arrlen_y

        for x in range(self.arrlen_y):
            row = []
            for y in range(self.arrlen_x):
                
                if self.num_grid[x][y]:

                    row.append(
                        rect(
                            self.main_rect.x + self.cell_w * y,
                            self.main_rect.y + self.cell_h * x,
                            self.cell_w,self.cell_h,(0,0,0),
                        )
                    )


            cells.append(row)

        
        return cells
    
    def initialize_player(self):
        
        
        for x,y in enumerate(self.num_grid):
            for z,w in enumerate(y):
                
                if not w:
                    xpos = self.main_rect.x + self.cell_w * (z+0.5)
                    ypos = self.main_rect.y + self.cell_h * (x+0.5)
                    break        

            if not w:
                break

        
        if w == 1:
            raise Exception
        
        self.player1 = player([xpos,ypos],3,(255,0,0),25,50,2,self.main_rect,self.cell_w,self.cell_h,self.grid,self.num_grid)


        


    def set_backround_functions(self):
        
        pressed_keys = pygame.key.get_pressed()
        self.endpoints = self.cast_rays()
        
        self.backround_functions = (
            (self.draw_screen,()),
            (self.player1.handle_movement,(pressed_keys,(y for x in self.grid for y in x))),
            (self.set_backround_functions,())
        )

         
    
    def set_screen_data(self):
        

        self.screen_data = [
            self.main_rect,
            *[y for x in self.grid for y in x],
            self.player1

        ]
    
    def cast_rays(self,degree_to_mouse=None):
        
        endpoints = []
        
        if degree_to_mouse is None:
            degree_to_mouse = self.player1.angle_from_point(
                pygame.mouse.get_pos()
            )
        
        self.angle = degree_to_mouse


        for x in range(int(degree_to_mouse - self.player1.view_angle / 2),int(degree_to_mouse + self.player1.view_angle / 2)):
            endpoints.append(
                self.player1.cast_ray(x)
            )

        return endpoints

    def draw_screen(self):
        #WIN.fill((255,255,255))

        for x in self.screen_data:
            x.draw()

        for p in self.endpoints:

            pygame.draw.line(
                WIN,
                (255,0,0),
                self.player1.center,
                p
            )

        pygame.display.update()


    def update(self):

        for func,params in self.backround_functions:
            func(*params)
            
            
    def test(self):

        running = True
        
        clock = pygame.time.Clock()

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False

            self.update()

if __name__ == "__main__":
    m = scene_2d(
        rect(0,0,WIDHT,HEIGHT,(255,255,255),False),
        [
            [1,1,1,1,1,1,1],
            [1,0,1,1,0,0,1],
            [1,0,1,1,0,0,1],
            [1,0,1,0,0,0,1],
            [1,0,0,0,1,1,1],
            [1,1,1,1,1,1,1]
        ]
    )
    m.test()





