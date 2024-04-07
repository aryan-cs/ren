import pygame
import pygame.gfxdraw
import sys
import math

display_message_backlog = ["I am Ren, your emotionally capable AI companion.",
                           "I was designed to help you better your mental health.",
                           "How may I help you today?",
                           " "]

# Initialize Pygame
pygame.init()

# Set up screen dimensions
WIDTH, HEIGHT = 800, 600

# Heatmap for gradient
heatmap = [
    [0.0, (28, 244, 255)],      # Start color: blue
    [1.0, (204, 0, 255)]        # End color: purple
]

# Coordinates of starting point for gradient
start_x, start_y = 0, 0

# Precompute the gradient for each pixel in the screen
gradient_colors = []
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        dist = math.sqrt((start_x - x) ** 2 + (start_y - y) ** 2)
        total_dist = math.sqrt(WIDTH ** 2 + HEIGHT ** 2)
        ratio = dist / total_dist

        color1_pos = None
        color2_pos = None

        for i, (pos, _) in enumerate(heatmap):
            if ratio <= pos:
                color1_pos = heatmap[i - 1]
                color2_pos = heatmap[i]
                break

        if color1_pos is None:
            color1_pos = heatmap[-2]
            color2_pos = heatmap[-1]

        start_rgb = color1_pos[1]
        end_rgb = color2_pos[1]

        t = (ratio - color1_pos[0]) / (color2_pos[0] - color1_pos[0])
        r = start_rgb[0] * (1 - t) + end_rgb[0] * t
        g = start_rgb[1] * (1 - t) + end_rgb[1] * t
        b = start_rgb[2] * (1 - t) + end_rgb[2] * t

        row.append((int(r), int(g), int(b)))
    gradient_colors.append(row)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ren")
pygame.display.set_icon(pygame.image.load('ren.png'))

# Function to draw a filled circle with gradient
def draw_gradient_circle(surface, center, radius):
    pygame.gfxdraw.aacircle(surface, center[0], center[1], radius, (255, 255, 255))  # Anti-aliased circle
    pygame.gfxdraw.filled_circle(surface, center[0], center[1], radius, (255, 255, 255))  # Filled circle
    for x in range(center[0] - radius, center[0] + radius):
        for y in range(center[1] - radius, center[1] + radius):
            if (x - center[0])**2 + (y - center[1])**2 <= radius**2:
                color = gradient_colors[y][x]
                pygame.gfxdraw.pixel(surface, x, y, color)  # Draw pixel

# Function to draw a white circle at the center of the screen
def draw_white_circle(surface, center, radius):
    pygame.draw.circle(surface, (255, 255, 255), center, radius)

# Function to render and blit text on the screen
def render_text(text, font, color, center):
    font_obj = pygame.font.Font('Poppins-Medium.ttf', 20)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)


# Function to draw semi-transparent white rectangle with increasing opacity over time
def draw_semi_transparent_rect(surface, rect, current_time, start_time, duration):
    time_elapsed = current_time - start_time
    max_opacity = 255
    target_opacity = min(255, int(255 * (time_elapsed / duration)))  # Opacity increases gradually over the duration
    frames = 60  # Number of frames for the transition
    current_frame = min(frames, int(frames * (time_elapsed / duration)))  # Current frame

    # Interpolate between current opacity and target opacity
    current_opacity = (max_opacity * current_frame + target_opacity * (frames - current_frame)) // frames

    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, current_opacity))  # Set opacity based on interpolation
    surface.blit(overlay, rect)


# Main loop
def main():
    running = True
    space_pressed = False
    text = display_message_backlog.pop(0)
    next_text = None  # Variable to hold the next text message
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    if display_message_backlog and not next_text:
                        next_text = display_message_backlog.pop(0)  # Store the next text message

        screen.fill((255, 255, 255))  # Fill background with white
        draw_gradient_circle(screen, (WIDTH // 2, HEIGHT // 2 - 50), 150)
        draw_white_circle(screen, (WIDTH // 2, HEIGHT // 2 - 50), 130)  # Draw smaller white circle
        
        # Render and blit text
        text_color = (0, 0, 0)  # Black color for the text
        text_center = (WIDTH // 2, HEIGHT // 2 + 200)  # Place text 200 pixels below the circle's center
        render_text(text, pygame.font.Font('Poppins-Medium.ttf', 20), text_color, text_center)

        if space_pressed and next_text:  # If space is pressed and there's a next text message to display
            text = next_text
            next_text = None  # Reset the next text message
            space_pressed = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()