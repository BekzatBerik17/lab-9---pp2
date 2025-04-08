import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0)
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application")
screen.fill(WHITE)

font = pygame.font.SysFont(None, 24)

drawing = False
last_pos = None
start_pos = None
mode = "pen"
color = BLACK
radius = 5

# Define buttons
buttons = {
    "Rectangle": pygame.Rect(10, 10, 100, 30),
    "Circle": pygame.Rect(120, 10, 100, 30),
    "Brush": pygame.Rect(230, 10, 100, 30),
    "Eraser": pygame.Rect(340, 10, 100, 30),
    "Clear": pygame.Rect(450, 10, 100, 30),
    "Exit": pygame.Rect(560, 10, 100, 30),
    "Red": pygame.Rect(670, 10, 30, 30),
    "Green": pygame.Rect(705, 10, 30, 30),
    "Blue": pygame.Rect(740, 10, 30, 30),
    "Yellow": pygame.Rect(775, 10, 30, 30),

    "Square": pygame.Rect(10, 50, 100, 30),
    "Right Triangle": pygame.Rect(120, 50, 100, 30),
    "Equilateral Triangle": pygame.Rect(230, 50, 140, 30),
    "Rhombus": pygame.Rect(380, 50, 100, 30),
}


def draw_buttons():
    for name, rect in buttons.items():
        if name in COLORS:
            pygame.draw.rect(screen, COLORS[name], rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text = font.render(name, True, BLACK)
            screen.blit(text, (rect.x + 5, rect.y + 5))


running = True
while running:
    draw_buttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            
            clicked_button = False
            for name, rect in buttons.items():
                if rect.collidepoint(pos):
                    clicked_button = True
                    if name in ["Rectangle", "Circle", "Brush", "Eraser",
                                "Square", "Right Triangle", "Equilateral Triangle", "Rhombus"]:  # NEW
                        mode = name.lower().replace(" ", "_")
                    elif name == "Clear":
                        screen.fill(WHITE)
                    elif name == "Exit":
                        pygame.quit()
                        sys.exit()
                    elif name in COLORS:
                        color = COLORS[name]
                    break

            if not clicked_button:
                drawing = True
                last_pos = pos
                if "triangle" in mode or mode in ["rectangle", "circle", "square", "rhombus"]:
                    start_pos = pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                end_pos = event.pos
                if mode == "rectangle":
                    rect = pygame.Rect(min(start_pos[0], end_pos[0]),
                                       min(start_pos[1], end_pos[1]),
                                       abs(end_pos[0] - start_pos[0]),
                                       abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, color, rect, 2)

                elif mode == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)

                elif mode == "square":
                    side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    top_left = (start_pos[0], start_pos[1])
                    pygame.draw.rect(screen, color, (top_left[0], top_left[1], side, side), 2)

                elif mode == "right_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    points = [(x1, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(screen, color, points, 2)

                elif mode == "equilateral_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    side = abs(x2 - x1)
                    height = (3 ** 0.5 / 2) * side
                    top = (x1, y1)
                    left = (x1 - side // 2, y1 + height)
                    right = (x1 + side // 2, y1 + height)
                    pygame.draw.polygon(screen, color, [top, left, right], 2)

                elif mode == "rhombus":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    mid_x = (x1 + x2) // 2
                    mid_y = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    points = [
                        (mid_x, y1),  # top
                        (x2, mid_y),  # right
                        (mid_x, y2),  # bottom
                        (x1, mid_y)   # left
                    ]
                    pygame.draw.polygon(screen, color, points, 2)

        elif event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.line(screen, color, last_pos, event.pos, 5)
                last_pos = event.pos
            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 20)

    pygame.display.flip()

pygame.quit()