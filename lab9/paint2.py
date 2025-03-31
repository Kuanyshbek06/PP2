import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Paint Tool")
canvas = pygame.Surface((WIDTH, HEIGHT - 50))
canvas.fill(WHITE)
color = BLACK
mode = "pen"
drawing = False
start_pos = (0, 0)

colors = [(BLACK, (10, 10, 30, 30)), (RED, (50, 10, 30, 30)), (GREEN, (90, 10, 30, 30)), (BLUE, (130, 10, 30, 30))]
tools = {"pen": (170, 10, 50, 30),"eraser": (230, 10, 70, 30),"rect": (310, 10, 70, 30),"circle": (390, 10, 70, 30),
    "square": (470, 10, 70, 30),
    "r-triangle": (550, 10, 100, 30),
    "eq-triangle": (660, 10, 100, 30),
    "rhombus": (770, 10, 90, 30),
    "clear": (870, 10, 80, 30)
}

def draw_buttons():
    for col, rect in colors:
        pygame.draw.rect(screen, col, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
    
    for tool, rect in tools.items():
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = pygame.font.SysFont(None, 18).render(tool.capitalize(), True, BLACK)
        screen.blit(text, (rect[0] + 5, rect[1] + 5))

def get_color(pos):
    for col, rect in colors:
        if pygame.Rect(rect).collidepoint(pos):
            return col
    return None

def get_tool(pos):
    for tool, rect in tools.items():
        if pygame.Rect(rect).collidepoint(pos):
            return tool
    return None

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 50))
    draw_buttons()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected_color = get_color(event.pos)
                if selected_color:
                    color = selected_color
                else:
                    selected_tool = get_tool(event.pos)
                    if selected_tool:
                        if selected_tool == "clear":
                            canvas.fill(WHITE)
                        else:
                            mode = selected_tool
                    else:
                        drawing = True
                        start_pos = (event.pos[0], event.pos[1] - 50)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = (event.pos[0], event.pos[1] - 50)
                if mode == "rect":
                    pygame.draw.rect(canvas, color, pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])), 2)
                elif mode == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, radius, 2)
                elif mode == "square":
                    side = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(canvas, color, pygame.Rect(start_pos[0], start_pos[1], side, side), 2)
                elif mode == "r-triangle":
                    pygame.draw.polygon(canvas, color, [start_pos, (start_pos[0], end_pos[1]), (end_pos[0], end_pos[1])], 2)
                elif mode == "eq-triangle":
                    height = abs(end_pos[1] - start_pos[1])
                    half_base = height // math.sqrt(3)
                    pygame.draw.polygon(canvas, color, [start_pos, (start_pos[0] - half_base, end_pos[1]), (start_pos[0] + half_base, end_pos[1])], 2)
                elif mode == "rhombus":
                    dx = abs(end_pos[0] - start_pos[0]) // 2
                    dy = abs(end_pos[1] - start_pos[1]) // 2
                    pygame.draw.polygon(canvas, color, [(start_pos[0], start_pos[1] - dy), (start_pos[0] - dx, start_pos[1]), (start_pos[0], start_pos[1] + dy), (start_pos[0] + dx, start_pos[1])], 2)
                drawing = False
        
        elif event.type == pygame.MOUSEMOTION:
            if drawing and mode == "pen":
                pygame.draw.line(canvas, color, start_pos, (event.pos[0], event.pos[1] - 50), 2)
                start_pos = (event.pos[0], event.pos[1] - 50)
            elif drawing and mode == "eraser":
                pygame.draw.circle(canvas, WHITE, (event.pos[0], event.pos[1] - 50), 10)

pygame.quit()
sys.exit()