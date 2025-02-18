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

# Screen dimensions based on grid size and space for title, timer, button, and guidelines
GRID_SIZE = 5 * (BOX_SIZE + MARGIN) - MARGIN
TITLE_SPACE = 100                               # the space below title
TIMER_SPACE = 50                                # the space below timer
BUTTON_SPACE = 10                               # the space below button
GUIDELINES_WIDTH = 580                          # width for the guidelines
SCREEN_WIDTH = GRID_SIZE + 2 * MARGIN + GUIDELINES_WIDTH + 80  
SCREEN_HEIGHT = GRID_SIZE + TITLE_SPACE + TIMER_SPACE + BUTTON_SPACE +  90  

# Colors used
WHITE = (255, 255, 255)
LIGHT_BLACK = (50, 50, 50) 
DARK_OLIVE = (50, 50, 25)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
DARKBLUE = (0, 0, 139)
SKYBLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GOLDEN = (255, 236, 139)
LIGHT_GREEN = (100, 220, 0)


# Creating Game Window.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Designer & Developer: AKARSH PRAKASH")

# Fonts
title_font = pygame.font.SysFont(['Impact', 'Arial', 'sans-serif'], 70)
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 40)
how_to_play_heading_font = pygame.font.SysFont(['Trebuchet MS', 'Arial', 'sans-serif'], 40, bold=True)
how_to_play_font = pygame.font.SysFont(['Verdana', 'Arial', 'sans-serif'], 20)

# Alarm sound
pygame.mixer.init()                
alarm_sound = pygame.mixer.Sound('Alarm_Sound.ogg')  

# Track user clicks & Game state
current_number = 1          # Track the next number the user should click
game_over = False           # Track if the game has ended
clicked_numbers = set()     # Track which numbers have been clicked correctly

# Gradient Background
def gradient_background():
    for y in range(SCREEN_HEIGHT):
        # By Using Two colors (ORANGE & YELLOW)
        color = (
            int(255 * (1 - y / SCREEN_HEIGHT)),
            int(165 * (1 - y / SCREEN_HEIGHT)),
            int(0 * (1 - y / SCREEN_HEIGHT))
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

# Game Over Screen
def game_over_screen():
    screen.fill(RED)            # Screen Color

    game_over_text = title_font.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    score_text = small_font.render(f"Final Score: {len(clicked_numbers)}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    # Position for 'Restart' button (occupying the space)
    restart_button_x = SCREEN_WIDTH // 2 - 70
    restart_button_y = SCREEN_HEIGHT// 2 + 60
    restart_button_rect = pygame.Rect(restart_button_x, restart_button_y, 140, 50)
 
    # 'Restart' button 
    pygame.draw.rect(screen, WHITE, restart_button_rect, border_radius=15)
    restart_text = small_font.render("Restart", True, RED)
    screen.blit(restart_text, (restart_button_rect.x + 24, restart_button_rect.y)
    
    return restart_button_rect

# How to play
def how_to_play(): 
    how_to_play_x = SCREEN_WIDTH - GUIDELINES_WIDTH + 20
    how_to_play_y = TITLE_SPACE + TIMER_SPACE                 # "How to play" at the Grid's Top

    how_to_play_heading = how_to_play_heading_font.render("How to Play ", True, YELLOW)
    screen.blit(how_to_play_heading, (how_to_play_x + 80, how_to_play_y))
    how_to_play_y += how_to_play_heading_font.get_height() + 10
    
    how_to_play_text = [
                "1. Click the 'PLAY' button to start the game.",
                "2. A 5x5 grid will display numbers from 1 to 25",
                "in random order.",
                "3. Numbers will be visible for 10 seconds.",
                "4. Click the numbers in ascending order (1 to 25).",
                "5. If you click the correct number, it will turn GREEN.",
                "6. If you click the wrong number, the game will end.",
                "7. Your SCORE is the count of sequential correct clicks.",
                "8. After each turn, your score will be displayed ",
                "below the grid.",
                "9. Challenge yourself to achieve the highest",
                "score possible!",
                "10. Click 'Restart' to restart the game."
                ]
    
    
    for line in how_to_play_text:
        how_to_play_surface = how_to_play_font.render(line, True, GOLDEN)
        screen.blit(how_to_play_surface, (how_to_play_x, how_to_play_y))
        how_to_play_y += how_to_play_font.get_height() + 5  


# Grid with Numbers
def grid(numbers, visible):
    start_x = (SCREEN_WIDTH - GUIDELINES_WIDTH - GRID_SIZE) // 2
    start_y = TITLE_SPACE + TIMER_SPACE         # 'Grid' just below the title and timer

    for i in range(5):
        for j in range(5):
            number = numbers[i * 5 + j]
            x = start_x + j * (BOX_SIZE + MARGIN)
            y = start_y + i * (BOX_SIZE + MARGIN)
            
            # Change color based on whether the number has been clicked Correctly or Incorrectly
            if number in clicked_numbers:
                pygame.draw.circle(screen, LIGHT_GREEN, (x + BOX_SIZE // 2, y + BOX_SIZE // 2), BOX_SIZE // 2)
            elif game_over and number == current_number:
                pygame.draw.circle(screen, RED, (x + BOX_SIZE // 2, y + BOX_SIZE // 2), BOX_SIZE // 2)
            else:
                pygame.draw.circle(screen, SKYBLUE, (x + BOX_SIZE // 2, y + BOX_SIZE // 2), BOX_SIZE // 2)


            # For numbers inside Grid
            if visible:
                if number<10:
                    text = font.render(f'0{number}', True, DARKBLUE)
                else:
                    text = font.render(f'{number}', True, DARKBLUE)
                screen.blit(text, (x + BOX_SIZE // 2 - 20, y + BOX_SIZE // 2 - 50))


# Generating Shuffled list of numbers
def generate_numbers():
    numbers = list(range(1, 26))                # numbers  --> it is a list 
    random.shuffle(numbers)
    return numbers


# Check if the clicked number is correct(i.e in sequemce or NOT)
def check_click(number):
    global current_number, game_over
    if number == current_number:
        clicked_numbers.add(number)  # Adding the "number" to the set of correctly clicked no.s
        current_number += 1
    else:
        game_over = True
        alarm_sound.play()



async def main():                     # def main(): ---> async def main():
    global current_number, game_over, clicked_numbers
    clock = pygame.time.Clock()                      
    numbers = generate_numbers()
    show_numbers = False
    start_time = None

    # Calculating the Position for the 'Play' button below the grid (occupying the space)
    play_button_y = TITLE_SPACE + TIMER_SPACE + GRID_SIZE 
    play_button_x = SCREEN_WIDTH // 2 - GUIDELINES_WIDTH // 2 - 60
    play_button_rect = pygame.Rect(play_button_x, play_button_y, 120, 50)

    running = True
    while running:
        # screen.fill(ORANGE)           # Screen color    
        gradient_background()
        
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                running = False
            elif EVENT.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # 'Restart' button click
                    restart_button_rect = game_over_screen()
                    if restart_button_rect.collidepoint(EVENT.pos):
                        show_numbers = True
                        start_time = time.time()
                        numbers = generate_numbers()
                        current_number = 1  
                        game_over = False  
                        clicked_numbers = set() 
                elif play_button_rect.collidepoint(EVENT.pos):
                    show_numbers = True
                    start_time = time.time()
                    numbers = generate_numbers()
                    current_number = 1          # Reset --> sequence tracker  
                    game_over = False           # Reset --> game state
                    clicked_numbers = set()     # Reset --> clicked numbers
                elif show_numbers and not game_over:
                    # Checking the user clicked a number or NOT
                    mouse_x, mouse_y = EVENT.pos
                    start_x = (SCREEN_WIDTH - GUIDELINES_WIDTH - GRID_SIZE) // 2
                    start_y = TITLE_SPACE + TIMER_SPACE

                    for i in range(5):
                        for j in range(5):
                            x = start_x + j * (BOX_SIZE + MARGIN)
                            y = start_y + i * (BOX_SIZE + MARGIN)
                            if x <= mouse_x <= x + BOX_SIZE and y <= mouse_y <= y + BOX_SIZE:
                                clicked_number = numbers[i * 5 + j]
                                check_click(clicked_number)

        # Title in the Center 
        title_text = title_font.render("Sequence Sprint", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))

        if show_numbers and not game_over:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, int(10 - elapsed_time))
            if elapsed_time > 10:
                game_over = True
                show_numbers = False
                alarm_sound.play()          # Play the "Alarm Sound"
            else:
                grid(numbers, True)

            # Timer below the Title
            timer_text = small_font.render(f"Time Left: 0{remaining_time} sec", True, LIGHT_BLACK)
            screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, TITLE_SPACE + 5))

        else:
            grid(numbers, False)
        
        # 'Play' button just below the grid
        pygame.draw.rect(screen, DARK_OLIVE, play_button_rect, border_radius=15)
        play_text = small_font.render("PLAY", True, WHITE)
        screen.blit(play_text, (play_button_rect.x + 27, play_button_rect.y ))

        # How To Play
        how_to_play()
        
        # Game over screen 
        if game_over:
            restart_button_rect = game_over_screen()

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)      # Yield control to the asyncio event loop

    # Exit Pygame
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())               # Use asyncio to run the main function
