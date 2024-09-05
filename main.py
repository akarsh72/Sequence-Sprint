# Sequence Sprint 
## pygame to web browser

import pygame
import random
import time
import asyncio              # Import asyncio for web compatibility

pygame.init()

# Box & Margin dimensions
BOX_SIZE = 80           
MARGIN = 10

# Screen dimensions based on grid siz and space for title, timer, button, and guidelines
GRID_SIZE = 5 * (BOX_SIZE + MARGIN) - MARGIN
TITLE_SPACE = 100                               # the space below title
TIMER_SPACE = 50                                # the space below timer
BUTTON_SPACE = 10                               # the space below button
GUIDELINES_WIDTH = 580                          # width for the guidelines
SCREEN_WIDTH = GRID_SIZE + 2 * MARGIN + GUIDELINES_WIDTH + 80  
SCREEN_HEIGHT = GRID_SIZE + TITLE_SPACE + TIMER_SPACE + BUTTON_SPACE +  90  

# Colors used
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
DARKBLUE = (0, 0, 139)
SKYBLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GOLDEN = (255, 236, 139)

# Creating game window.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Designer & Developer: AKARSH PRAKASH")

# Fonts
title_font = pygame.font.SysFont(['Impact', 'Arial', 'sans-serif'], 70)
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 40)
guidelines_heading_font = pygame.font.SysFont(['Trebuchet MS', 'Arial', 'sans-serif'], 50, bold=True)
guidelines_font = pygame.font.SysFont(['Verdana', 'Arial', 'sans-serif'], 20)


# Alarm sound
pygame.mixer.init()                
alarm_sound = pygame.mixer.Sound('Alarm_Sound.ogg')  



# Guidelines section on the right-hand side, aligned with the grid
def draw_guidelines():
    guidelines_x = SCREEN_WIDTH - GUIDELINES_WIDTH + 20
    guidelines_y = TITLE_SPACE + TIMER_SPACE                 # Align the guidelines with the grid's top

    guidelines_heading = guidelines_heading_font.render("Guidelines ", True, YELLOW)
    screen.blit(guidelines_heading, (guidelines_x, guidelines_y))
    guidelines_y += guidelines_heading_font.get_height() 
    

    guidelines_text = [
                "1. This game is designed to enhance your focus.",
                "2. A 5x5 grid will display numbers from ",
                "    1 to 25 in random order.",
                "3. These numbers will be visible for 10 seconds.",
                "4. Your goal is to find the numbers in their natural ",
                "    sequential order, starting from 1 up to 25.",
                "5. The highest number you successfully find will",
                "    determine your score.",
                "6. A 2-second alarm will signal the end of the game.",
                "7. Challenge yourself to achieve the highest",
                "   score possible.",
                "8. Click the 'Play' button to start."
                ]
    
    
    for line in guidelines_text:
        guidelines_surface = guidelines_font.render(line, True, GOLDEN)
        screen.blit(guidelines_surface, (guidelines_x, guidelines_y))
        guidelines_y += guidelines_font.get_height() + 7  


# Drawing the grid with Numbers
def draw_grid(numbers, visible):
    start_x = (SCREEN_WIDTH - GUIDELINES_WIDTH - GRID_SIZE) // 2
    start_y = TITLE_SPACE + TIMER_SPACE         # Placing the grid just below the title and timer

    for i in range(5):
        for j in range(5):
            number = numbers[i * 5 + j]
            x = start_x + j * (BOX_SIZE + MARGIN)
            y = start_y + i * (BOX_SIZE + MARGIN)
            pygame.draw.circle(screen, SKYBLUE, (x + BOX_SIZE // 2, y + BOX_SIZE // 2), BOX_SIZE // 2)

            # For numbers inside Grid
            if visible:
                text = font.render(str(number), True, DARKBLUE)
                screen.blit(text, (x + BOX_SIZE // 2 - 20, y + BOX_SIZE // 2 - 20))


# Generate a shuffled list of numbers
def generate_numbers():
    numbers = list(range(1, 26))                # numbers  --> it is a list 
    random.shuffle(numbers)
    return numbers



async def main():                     # def main(): ---> async def main():
    clock = pygame.time.Clock()                      
    numbers = generate_numbers()
    show_numbers = False
    start_time = None

    # Calculating the position for the Play button below the grid
    play_button_y = TITLE_SPACE + TIMER_SPACE + GRID_SIZE +  20
    play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - GUIDELINES_WIDTH // 2 - 75, play_button_y, 150, 50)

    running = True
    while running:
        screen.fill(ORANGE)           # Screen color    
        
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                running = False
            elif EVENT.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(EVENT.pos):
                    show_numbers = True
                    start_time = time.time()
                    numbers = generate_numbers()

        # Title in the center 
        title_text = title_font.render("Sequence Sprint", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))

        if show_numbers:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, int(10 - elapsed_time))
            if elapsed_time > 10:
                show_numbers = False
                alarm_sound.play()          # Play the alarm sound
            else:
                draw_grid(numbers, True)

            # Timer below the Title
            timer_text = small_font.render(f"Time Left: {remaining_time}s", True, RED)
            screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, TITLE_SPACE + 5))

        else:
            draw_grid(numbers, False)
        
        # Play button just below the grid
        pygame.draw.rect(screen, GREEN, play_button_rect, border_radius=200)
        play_text = small_font.render("PLAY", True, PURPLE)
        screen.blit(play_text, (play_button_rect.x + 40, play_button_rect.y + 10))

        # Guidelines
        draw_guidelines()
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)      # Yield control to the asyncio event loop

    # Exit Pygame
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())             # Use asyncio to run the main function
