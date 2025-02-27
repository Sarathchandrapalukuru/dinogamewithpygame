import pygame
import random
import pandas as pd

# Initialize Pygame
pygame.init()

# Get the system's screen width and height
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Create a window that is maximized based on the system's resolution
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Chrome Dino Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define fonts
font = pygame.font.SysFont(None, 30)

# Load dinosaur image
dino_img = pygame.image.load('dinosaur.png')  # Replace with your PNG file
dino_img = pygame.transform.scale(dino_img, (40, 60))  # Resize image (adjust as needed)

# Dino class
class Dino:
    def __init__(self):
        self.x = 50
        self.y = screen_height - 100
        self.width = 40
        self.height = 60
        self.vel_y = 0
        self.jumping = False
    
    def draw(self):
        screen.blit(dino_img, (self.x, self.y))  # Draw the dinosaur image

    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True

    def update(self):
        if self.jumping:
            self.vel_y += 1
            self.y += self.vel_y

            if self.y >= screen_height - 100:
                self.y = screen_height - 100
                self.jumping = False
                self.vel_y = 0

# Cactus class
# Load cactus image and resize it
cactus_img = pygame.image.load('cactus.webp')  # Replace with your cactus image file
cactus_img = pygame.transform.scale(cactus_img, (50, 80))  # Resize cactus to a larger size (adjust as needed)

# Cactus class
class Cactus:
    def __init__(self):
        self.x = screen_width
        self.y = screen_height - 100  # Adjust the Y position to fit with the ground
        self.width = 50  # Width of the cactus
        self.height = 80  # Height of the cactus
        self.vel_x = -10  # Speed of the cactus movement to the left

    def draw(self):
        screen.blit(cactus_img, (self.x, self.y))  # Draw the resized cactus image

    def update(self):
        self.x += self.vel_x  # Move the cactus to the left


# Function to display score
def show_score(score):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

# Function to display text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Name Entry Screen Function
def name_entry_screen():
    running = True
    name_input_active = False
    name = ""
    
    while running:
        screen.fill(WHITE)

        # Draw name entry prompt
        draw_text("Enter Your Name", font, BLACK, screen, screen_width // 2, screen_height // 2 -10)
        pygame.draw.rect(screen, BLACK, (screen_width // 2 - 100, screen_height // 2 + 20, 200, 40), 2)
        draw_text(name, font, BLACK, screen, screen_width // 2, screen_height // 2 + 40)

        draw_text("Press ENTER to Start", font, GREEN, screen, screen_width // 2, screen_height // 2 +100)
        draw_text("Press ESC to Exit", font, RED, screen, screen_width // 2, screen_height // 2 + 150)

        pygame.display.update()

        # Event handling for name entry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to start the game
                    if name != "":
                        game_loop(name)  # Start the game with the entered name
                        running = False
                if event.key == pygame.K_ESCAPE:  # Escape key to exit the game
                    running = False
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # Delete last character
                elif event.key != pygame.K_RETURN and not name_input_active:
                    name_input_active = True  # Activate name input
                elif event.unicode.isalpha() or event.key == pygame.K_SPACE:
                    name += event.unicode  # Add typed character

# Function to save score to Excel
def save_score(name, score):
    # Read existing scores from Excel (if it exists)
    try:
        df = pd.read_excel("high_scores.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Score"])

    # Append the new score
    new_row = pd.DataFrame({"Name": [name], "Score": [score]})
    df = pd.concat([df, new_row], ignore_index=True)

    # Sort the dataframe by score in descending order
    df = df.sort_values(by="Score", ascending=False)

    # Save the updated high scores to the Excel file
    df.to_excel("high_scores.xlsx", index=False)

# Function to show high scores
# def show_high_scores():
#     try:
#         df = pd.read_excel("high_scores.xlsx")
#         screen.fill(WHITE)
#         draw_text("High Scores", font, BLACK, screen, screen_width // 2, screen_height // 4)
#         y_pos = screen_height // 3
#         for index, row in df.iterrows():
#             draw_text(f"{row['Name']} - {row['Score']}", font, BLACK, screen, screen_width // 2, y_pos)
#             y_pos += 30
#         pygame.display.update()
#     except FileNotFoundError:
#         draw_text("No High Scores Yet", font, BLACK, screen, screen_width // 2, screen_height // 2)
#         pygame.display.update()
# Function to show high scores (limit to last 5 scores)
def show_high_scores():
    try:
        df = pd.read_excel("high_scores.xlsx")
        # Sort the dataframe by score in descending order and select only the top 5
        df = df.sort_values(by="Score", ascending=False).head(5)

        screen.fill(WHITE)
        draw_text("High Scores", font, BLACK, screen, screen_width // 2, screen_height // 4)
        y_pos = screen_height // 3

        # Loop through the top 5 scores and display them
        for index, row in df.iterrows():
            draw_text(f"{row['Name']} - {row['Score']}", font, BLACK, screen, screen_width // 2, y_pos)
            y_pos += 30

        pygame.display.update()
    except FileNotFoundError:
        draw_text("No High Scores Yet", font, BLACK, screen, screen_width // 2, screen_height // 2)
        pygame.display.update()

# Main Game Loop
def game_loop(name):
    clock = pygame.time.Clock()
    dino = Dino()
    cacti = [Cactus()]
    score = 0
    run_game = True

    while run_game:
        screen.fill(WHITE)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        # Update Dino
        dino.update()
        dino.draw()

        # Update Cacti
        for cactus in cacti[:]:
            cactus.update()
            cactus.draw()

            # Check for collision
            if (dino.x + dino.width > cactus.x and dino.x < cactus.x + cactus.width and
                dino.y + dino.height > cactus.y):
                run_game = False  # Collision, end the game

            # Remove cactus if it's off the screen
            if cactus.x < -cactus.width:
                cacti.remove(cactus)
                score += 1  # Increase score when cactus is passed

        # Spawn new cacti
        if random.randint(1, 100) == 1:
            cacti.append(Cactus())

        # Display Score
        show_score(score)

        pygame.display.update()

        # Set FPS
        clock.tick(45)

    # Save score to Excel after game over
    save_score(name, score)
    
    # After the game ends, show the high scores and restart option
    show_high_scores()
    draw_text("Press R to Restart or ESC to Exit", font, BLACK, screen, screen_width // 2, screen_height // 1.5)
    pygame.display.update()

    # Event Handling for Restart
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_restart = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press R to restart the game
                    game_loop(name)
                    waiting_for_restart = False
                if event.key == pygame.K_ESCAPE:  # Press ESC to exit the game
                    waiting_for_restart = False

    pygame.quit()
    quit()

# Start the game by showing the name entry screen
name_entry_screen()
