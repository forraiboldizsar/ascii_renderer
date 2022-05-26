from scene_2d import *
from create_3d_scene import *




class main:
    
    def __init__(self,labirinth_map,view_distance) -> None:
        
        self.labirinth_map = labirinth_map
        self.view_distance = view_distance
        
        self.raycaster = scene_2d(
            rect(0,0,100,100,(255,255,255)),
            labirinth_map
        )
        
        self.scr_buffer = [
            [chars((y*15,x*10)," ",FONT) for y in range(WIDHT//10)] for x in range(HEIGHT//10)
        ]
        
        self.angle = 0

        self.set_screen_data()
        self.set_backround_functions()
        self.main()
    

    def chars_from_screen_buffer(self,endpoints):
        

        data3d = convert_to_3d_from_points(
            self.raycaster.player1.center,
            endpoints,
            WIDHT,HEIGHT,
            self.raycaster.player1.cell_h,
            self.raycaster.angle,
            self.view_distance
        )    
        
        
        for x,y in enumerate(self.scr_buffer):
            for w,z in enumerate(y):
                z.text = data3d[x][w][0]
                z.color = data3d[x][w][1]

    def set_backround_functions(self):
        
        self.endpoints = self.raycaster.cast_rays()

        self.backround_functions = [
            (self.chars_from_screen_buffer,[self.endpoints]),
            (self.draw_screen,()),
            (self.set_backround_functions,()),
            (self.raycaster.update,())
        ]
    
    def set_screen_data(self):

        self.screen_data = [
            *(y for x in self.scr_buffer for y in x),
        ]
    
    def draw_screen(self):
        
        WIN.fill((0,0,0))

        for x in self.screen_data:
            x.draw()

    def main(self):
        
        running = True

        while running:
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

            for func,param in self.backround_functions:
                func(*param)


if __name__ == "__main__":
    
    m = main([
        [1,1,1,1,1,1,1],
        [1,0,1,1,0,0,1],
        [1,0,1,1,0,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1],
        ],
        50 
    )
    


