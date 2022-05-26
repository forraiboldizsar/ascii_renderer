import math

calc_distance = lambda p1,p2: math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)



def calc_color(distance,view_distance):
    
    if not distance:
        return (155,) * 3
    
    ratio = view_distance**1.7 * 1.009 / distance
    
    if (c := round(155 - (155/ratio * 10))) < 0:
        return (0,) * 3
    return (c,) * 3
    

def convert_to_3d_from_points(center,endpoints,WIDHT,HEIGHT,side_len,angle,view_distance):
    


    src_buffer_h = HEIGHT//10
    scr_buffer_w = WIDHT//10
    degree_pixel_ratio = scr_buffer_w // len(endpoints)

    scr_buffer = [
        [[" ",[0,0,0]] for y in range(scr_buffer_w)] for x in range(src_buffer_h)
    ]
    
    for i,x in enumerate(endpoints):
        
        distance = calc_distance(center,x)
        
        if distance:
            line_height = int(side_len*src_buffer_h//distance)
            
            if line_height > src_buffer_h:
                line_height = src_buffer_h
            
        else:
            line_height = src_buffer_h
        


        color = calc_color(distance,view_distance)

        for y in range(src_buffer_h//2-line_height//2,src_buffer_h//2+line_height//2):
            for z in range(i*degree_pixel_ratio,(i+1)*degree_pixel_ratio):
                    
            
                scr_buffer[y][z][0] = "#"
                scr_buffer[y][z][1][:] = color
    

         
    return scr_buffer
                




