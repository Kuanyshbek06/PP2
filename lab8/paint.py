import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint Application")
    clock = pygame.time.Clock()
    
    mode = 'blue'
    tool = 'pen'
    points = []
    start_pos = None
    drawing = False
    shapes = []
    
    running = True
    while running:
        screen.fill((0, 0, 0))  
        
        keys = pygame.key.get_pressed()  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
            
          
            if event.type == pygame.MOUSEMOTION:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    tool = 'rectangle'
                elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    tool = 'circle'
                elif pygame.mouse.get_pressed()[0]:
                    tool = 'pen'
                elif pygame.mouse.get_pressed()[2]:
                    tool = 'eraser'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos
                drawing = True
                
                if tool == 'pen':
                    points.append(event.pos)
            
            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'pen':
                    points.append(event.pos)
                elif tool == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0), event.pos, 10)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and tool in ['rectangle', 'circle']:
                    end_pos = event.pos
                    shapes.append((tool, start_pos, end_pos, mode))
                drawing = False
     
        for shape in shapes:
            tool, start, end, color = shape
            shape_color = pygame.Color(color)
            if tool == 'rectangle':
                rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
                pygame.draw.rect(screen, shape_color, rect, 2)
            elif tool == 'circle':
                radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
                pygame.draw.circle(screen, shape_color, start, radius, 2)

       
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], 5, mode)
            i += 1
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

if __name__ == "__main__":
    main()








