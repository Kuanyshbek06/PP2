import pygame
import datetime

pygame.init()
pygame.display.set_caption("AIUclock")

def rot_center(image, angle, center):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    return rotated_image, new_rect.topleft  


H, W = 700, 700
screen = pygame.display.set_mode((H, W))


mickey = pygame.image.load("/Users\kuany\OneDrive\Рабочий стол\PP2\lab7\clock.png") 
hand = pygame.image.load("/Users\kuany\OneDrive\Рабочий стол\PP2\lab7\min_hand.png") 
hand1 = pygame.image.load("/Users\kuany\OneDrive\Рабочий стол\PP2\lab7\sec_hand.png")

mickey = pygame.transform.scale(mickey, (H, W))  
clock_center = (H // 2, W // 2)
font = pygame.font.Font(None, 50)  

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получаем текущее время
    now = datetime.datetime.now()
    second = now.second
    minute = now.minute
    hour = now.hour

    time_text = f"{hour:02}:{minute:02}:{second:02}"

    time_surface = font.render(time_text, True, (0, 0, 0))  
    time_rect = time_surface.get_rect(topleft=(20, 20))  

    min_angle = -6 * minute  
    sec_angle = -6 * second 

   
    rotated_min_hand, min_pos = rot_center(hand, min_angle, clock_center)
    rotated_sec_hand, sec_pos = rot_center(hand1, sec_angle, clock_center)

  
    screen.fill((255, 255, 255)) 
    screen.blit(mickey, (0, 0)) 
    screen.blit(rotated_min_hand, min_pos)  
    screen.blit(rotated_sec_hand, sec_pos) 
    screen.blit(time_surface, time_rect)  

    pygame.display.update()
    clock.tick(60) 

pygame.quit()






