import pygame
import sys
import os
from mutagen.mp3 import MP3  

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 500, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")


font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)


songs = [
    {
        "name": "Let it happen",
        "path": r"C:\Users\kuany\Downloads\Tame_Impala_-_Let_It_Happen_62939593.mp3"
    },
    {
        "name": "Alone",
        "path": r"C:\Users\kuany\OneDrive\Документы\alan-walker-alone.mp3"
    }
]

curr_index = 0
playing = False
current_time = 0 

def play(index, start_time=0):
    
    global playing, current_time
    pygame.mixer.music.load(songs[index]["path"])
    pygame.mixer.music.play(start=start_time)
    playing = True
    current_time = start_time

def stop():
   
    global playing
    pygame.mixer.music.stop()
    playing = False

def next_track():
    
    global curr_index, current_time
    curr_index = (curr_index + 1) % len(songs)
    current_time = 0
    play(curr_index)

def prev_track():
    
    global curr_index, current_time
    curr_index = (curr_index - 1) % len(songs)
    current_time = 0
    play(curr_index)


def get_song_length(path):
    return int(MP3(path).info.length)


def rewind(seconds):
   
    global current_time
    if playing:
        current_time = max(0, min(current_time + seconds, get_song_length(songs[curr_index]["path"])))
        play(curr_index, current_time)


def draw_slider():

    if playing:
        current_time = pygame.mixer.music.get_pos() // 1000
        total_time = get_song_length(songs[curr_index]["path"])
        pygame.draw.rect(screen, (200, 200, 200), (50, 150, 400, 10)) 
        pygame.draw.rect(screen, (255, 100, 100), (50, 150, (current_time / total_time) * 400, 10)) 
        time_text = small_font.render(f"{current_time:02}:{total_time:02}", True, (0, 0, 0))
        screen.blit(time_text, (220, 120))

print("UP: Play | DOWN: Stop | RIGHT: Next | LEFT: Prev | A: -10 sec | D: +10 sec")

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                play(curr_index, current_time)
            elif event.key == pygame.K_DOWN:
                stop()
            elif event.key == pygame.K_RIGHT:
                next_track()
            elif event.key == pygame.K_LEFT:
                prev_track()
            elif event.key == pygame.K_a:  
                rewind(-10)
            elif event.key == pygame.K_d:  
                rewind(10)

   
    current_text = font.render(songs[curr_index]["name"], True, (0, 0, 0))
    screen.blit(current_text, (20, 50))

    draw_slider()

    pygame.display.flip()

pygame.quit()
sys.exit()





