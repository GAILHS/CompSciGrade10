import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants for dark mode
WIDTH, HEIGHT = 0, 0  # Will set fullscreen resolution
WHITE = (230, 230, 230)
BLACK = (20, 20, 20)
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 180, 0)
RED = (220, 60, 60)
BUTTON_COLOR = (0, 120, 0)
BUTTON_HOVER = (0, 160, 0)

# Fonts
TITLE_FONT = pygame.font.SysFont(None, 60, bold=True)
FONT_EMOJI = pygame.font.SysFont('Segoe UI Emoji', 80)
SMALL_FONT = pygame.font.SysFont(None, 30)
INPUT_FONT = pygame.font.SysFont(None, 34)

# Slot symbols (emoji)
SYMBOLS = ['🍒', '🍋', '🔔', '🍉', '7']

# Setup fullscreen screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Slot Machine")

# Input box class with underline style
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = GRAY
        self.color_active = GREEN
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = INPUT_FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isdigit() or event.unicode == '.':
                    self.text += event.unicode
            self.txt_surface = INPUT_FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.line(screen, self.color, (self.rect.x, self.rect.bottom), (self.rect.right, self.rect.bottom), 3)

    def get_value(self):
        try:
            return float(self.text)
        except:
            return 0.0

# Button class
class Button:
    def __init__(self, x, y, w, h, text, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hovered = False
        self.txt_surface = SMALL_FONT.render(text, True, WHITE)

    def draw(self, screen):
        color = BUTTON_HOVER if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Game state
balance = 1000.0
message = ''
result_symbols = ['?', '?', '?']
spinning = False

# Layout calculations for centered UI
center_x = WIDTH // 2
input_width = 140
input_height = 45
button_width = 110
button_height = 45
input_x = center_x - input_width - 15  # input left of center by input width + gap
button_x = center_x + 15  # button right of center by gap
input_y = HEIGHT - 120
button_y = input_y

REEL_Y = HEIGHT // 2 - 70
REEL_WIDTH = 120
REEL_HEIGHT = 140
REEL_SPACING = 150
REEL_X = [center_x - REEL_SPACING, center_x, center_x + REEL_SPACING]

input_box = InputBox(input_x, input_y, input_width, input_height)
spin_button = Button(button_x, button_y, button_width, button_height, "SPIN")

def draw_slots(symbols):
    for i, sym in enumerate(symbols):
        sym_surface = FONT_EMOJI.render(sym, True, WHITE)
        rect = pygame.Rect(REEL_X[i] - REEL_WIDTH // 2, REEL_Y, REEL_WIDTH, REEL_HEIGHT)
        pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=18)
        pygame.draw.rect(screen, GRAY, rect, 4, border_radius=18)
        screen.blit(sym_surface, sym_surface.get_rect(center=rect.center))

def spin_reels_sequential(bet):
    global balance, message, result_symbols, spinning
    if spinning:
        return
    if bet <= 0:
        message = "Enter a valid bet > 0."
        return
    if bet > balance:
        message = "Insufficient balance."
        return

    spinning = True
    clock = pygame.time.Clock()
    spin_speed = 18
    spin_duration_per_reel = 1.0

    final_symbols = [random.choice(SYMBOLS) for _ in range(3)]
    reel_stop_times = [spin_duration_per_reel * i for i in range(1, 4)]
    start_time = time.time()

    current_symbols = ['?', '?', '?']
    reel_spinning = [True, True, True]

    running_spin = True
    while running_spin:
        elapsed = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i in range(3):
            if reel_spinning[i]:
                if elapsed >= reel_stop_times[i]:
                    reel_spinning[i] = False
                    current_symbols[i] = final_symbols[i]
                else:
                    current_symbols[i] = random.choice(SYMBOLS)

        screen.fill(BLACK)
        draw_ui()
        draw_slots(current_symbols)
        pygame.display.flip()
        clock.tick(spin_speed)

        if all(not s for s in reel_spinning):
            running_spin = False

    unique_symbols = len(set(final_symbols))
    if unique_symbols == 1:
        winnings = bet * 5
        balance += winnings
        message = f"Jackpot! You win ${winnings:.2f}!"
    elif unique_symbols == 2:
        winnings = bet / 2
        balance += winnings
        message = f"Two match! You win half your bet: ${winnings:.2f}!"
    else:
        balance -= bet
        message = f"No matches. You lose ${bet:.2f}."

    if balance <= 0:
        message += " You have run out of money!"

    result_symbols[:] = final_symbols
    spinning = False

def draw_ui():
    title_surface = TITLE_FONT.render("🛠 Slot Machine 🛠", True, WHITE)
    screen.blit(title_surface, title_surface.get_rect(center=(center_x, 80)))

    balance_surface = SMALL_FONT.render(f"Balance: ${balance:.2f}", True, WHITE)
    screen.blit(balance_surface, (20, 20))

    bet_label = SMALL_FONT.render("Place your bet:", True, WHITE)
    screen.blit(bet_label, (input_box.rect.x, input_box.rect.y - 25))

    if message:
        color = RED if "lose" in message or "insufficient" in message or "run out" in message else GREEN
        msg_surface = SMALL_FONT.render(message, True, color)
        screen.blit(msg_surface, (20, HEIGHT - 40))

def main():
    clock = pygame.time.Clock()
    global message

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            input_box.handle_event(event)
            spin_button.handle_event(event)
            if spin_button.is_clicked(event):
                bet = input_box.get_value()
                spin_reels_sequential(bet)

        draw_ui()
        input_box.draw(screen)
        spin_button.draw(screen)
        draw_slots(result_symbols)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
