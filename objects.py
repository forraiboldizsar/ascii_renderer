import pygame
import math
import random

pygame.init()

WIDHT,HEIGHT = 700,500
WIN = pygame.display.set_mode((WIDHT,HEIGHT))
FONT = pygame.font.Font("freesansbold.ttf",10)

distance_between2_points = lambda p1,p2: math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
point_in_rect = lambda rect,p : rect.x < p[0] and rect.x + rect.w > p[0] and rect.y < p[1] and rect.y + rect.h > p[1]

class rect(pygame.Rect):

    def __init__(self,x,y,w,h,color,draw_only_bounds = 0) -> None:
        super().__init__(x,y,w,h)
        self.color = color
        self.draw_only_bounds = draw_only_bounds

    def draw(self):
        pygame.draw.rect(WIN,self.color,self,self.draw_only_bounds)


class circle:

    def __init__(self,center,r,color) -> None:
        self.center = pygame.math.Vector2(center)
        self.color = color
        self.r = r

    def draw(self):
        pygame.draw.circle(WIN,self.color,self.center,self.r)
    
    def point_from_angle(self,angle):

        in_radians = math.radians(angle)

        return [
            self.center[0] + math.cos(in_radians) * self.r,
            self.center[1] - math.sin(in_radians) * self.r
        ]
    
    def angle_from_point(self,point):

        r = distance_between2_points(self.center,point)
        

        if r:
            degrees = math.degrees(math.acos((point[0] - self.center[0]) / r))
            
            if self.center[1] - point[1] < 0:
                degrees = 360 - degrees

            return degrees

            
            
        else:
            return 0

class chars:

    def __init__(self,cord,text,FONT,color = (155,155,155)) -> None:

        self.text = text
        self.font = FONT
        self.cord = cord
        self.color = color


    def draw(self):
        
        text = self.font.render(self.text,True,self.color)
        WIN.blit(text,self.cord)




class line:

    def __init__(self,p1,p2,color) -> None:
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.lenght = distance_between2_points(p1,p2)    

    def draw(self):
        pygame.draw.line(WIN,self.color,self.p1,self.p2)

    


class player(circle):

    def __init__(self, center, r, color,view_angle,view_distance,velocity,main_rect,cell_w,cell_h,grid,numgrid) -> None:
        super().__init__(center, r, color)
        self.view_distance = view_distance
        self.view_angle = view_angle
        self.velocity = velocity
        self.main_rect = main_rect
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.grid = grid
        self.numgrid = numgrid


        self.x_ch = [self.velocity,0]
        self.y_ch = [0,self.velocity]
        
            
    
    def handle_movement(self,pressed_keys,objects):
        
        change = pygame.math.Vector2([0,0])
        
        

        if pressed_keys[pygame.K_a]:
            change -= self.x_ch

        if pressed_keys[pygame.K_d]:
            change += self.x_ch

        if pressed_keys[pygame.K_s]:
            change += self.y_ch

        if pressed_keys[pygame.K_w]:
            change -= self.y_ch

        self.center += change

        for x in objects:
            
        
            if point_in_rect(x,self.center):
                self.center -= change
                
                break



    def cast_ray(self,angle):

        
        angle %= 360
        in_radians = math.radians(angle)
        


        endpoint = pygame.math.Vector2(self.center)

        current_cell = [
            int((endpoint[1] - self.main_rect.y) / self.cell_h),
            int((endpoint[0] - self.main_rect.x) / self.cell_w) 
        ]



        


        while not self.numgrid[current_cell[0]][current_cell[1]]:
             

            # vertical line check
            
            if 0 < angle < 90 or 360 > angle > 270:

                vdx = ((current_cell[1] + 1) * self.cell_w + self.main_rect.x) - endpoint[0]
                vdy = math.tan(in_radians) * vdx * -1
                                

            elif angle % 90:

                vdx = (self.main_rect.x + current_cell[1] * self.cell_w) - endpoint[0]
                vdy = math.tan(in_radians) * vdx

                
            else:
                
                if angle == 0:

                    vdx = (self.main_rect.x + (current_cell[1] + 1 ) * self.cell_w) - endpoint[0]
                    endpoint[0] += vdx    
                    current_cell[1] += 1 
                    continue

                elif angle == 180:
                    vdx = endpoint[0] - (current_cell[1]  * self.cell_w + self.main_rect.x)
                    endpoint[0] -= vdx
                    current_cell[1] -= 1
                    continue
            

            #check horizontal


            if  angle < 180 and angle != 90:

                hdy = endpoint[1] - (self.main_rect.y + current_cell[0] * self.cell_h)
                hdx = hdy / math.tan(in_radians)
            
            elif angle > 180 and angle != 270:
                
                hdy = (self.main_rect.y + (current_cell[0]+1) * self.cell_h) - endpoint[1]
                hdx = hdy / math.tan(in_radians)
            

            else:

                if angle == 90:
                    hdy = endpoint[1] - (self.main_rect.y + current_cell[0] * self.cell_h)
                    endpoint[1] -= hdy
                    current_cell[0] -= 1
                    continue

                else:
                    hdy = (self.main_rect.y + (current_cell[0]+1) * self.cell_h) - endpoint[1]
                    endpoint[1] += hdy
                    current_cell[0] += 1
                    continue

            
            if vdx ** 2 + vdy ** 2 < hdx ** 2 + hdy ** 2:
                
                if angle < 90 or angle > 270:
                    endpoint[0] += vdx
                    endpoint[1] += vdy
                    current_cell[1] += 1    

                else:
                    endpoint[0] += vdx
                    endpoint[1] -= vdy
                    current_cell[1] -= 1

            else:

                if angle < 180:
                    
                    if angle < 90:
                        endpoint[0] += hdx
                        endpoint[1] -= hdy

                    else:
                        endpoint[0] += hdx
                        endpoint[1] -= hdy

                    current_cell[0] -= 1
                
                else:
                    
                    if angle < 270:
                        endpoint[0] -= hdx
                        endpoint[1] += hdy

                    else:
                        endpoint[0] -= hdx
                        endpoint[1] += hdy

                    current_cell[0] += 1
            
        
        


        return endpoint
