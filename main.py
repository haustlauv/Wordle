import random, pygame

def load_dict(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

dict_guessing = load_dict("dictionary_wordle.txt")
dict_answers = load_dict("dictionary_wordle.txt")
answer = random.choice(dict_answers)

width = 600
height = 700
margin = 10
t_margin = 100
b_margin = 100
lr_margin = 100

grey = (70,70,80)
green = (6, 214, 160)
yellow = (255, 209, 102)

input = ""
guesses = []
alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
unguessed = alphabet
error_text = "¡Ups! La palabra que has introducido no está en la lista."
game_over = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

sq_size = (width-4*margin-2*lr_margin) // 5
font = pygame.font.SysFont("free sans bold", sq_size)
font_small = pygame.font.SysFont("free sans bold", sq_size//2)

def determine_unguessed_letters(guesses):
    guessed_letters = "".join(guesses)
    unguessed_letters = ""
    for letter in alphabet:
        if letter not in guessed_letters:
            unguessed_letters = unguessed_letters + letter
    return unguessed_letters

def determine_color(guess, j):
    letter = guess[j]
    if letter == answer[j]:
        return green
    elif letter in answer:
        n_target = answer.count(letter)
        n_correct = 0
        n_ocurrence = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_ocurrence += 1
                if letter == answer[i]:
                    n_correct += 1
        if n_target - n_correct - n_ocurrence >= 0:
            return yellow
    return grey

# create screen
screen = pygame.display.set_mode((width,height))

# Animation loop
animating = True
while animating:

    # background
    screen.fill("white")
    determine_unguessed_letters(guesses)

    # draw unguessed letters
    letters = font_small.render(unguessed, False, grey)
    surface = letters.get_rect(center = (width//2, t_margin//2))
    screen.blit(letters,surface)

    # draw and guesses
    y = t_margin
    for i in range(6):
        x = lr_margin
        for j in range(5):

            # squares
            square = pygame.Rect(x,y, sq_size, sq_size)
            pygame.draw.rect(screen, grey, square, width =2, border_radius=3)

            # letters/words that have already been guessed
            if i < len(guesses):
               color = determine_color(guesses[i], j)
               pygame.draw.rect(screen, color, square, border_radius=3)
               letter = font.render(guesses[i][j], False, (255,255,255))
               surface = letter.get_rect(center = (x+sq_size//2, y+sq_size//2)) 
               screen.blit(letter, surface)

            # User text input (next guess)
            if i == len(guesses) and j < len(input):
                letter = font.render(input[j], False, grey)
                surface = letter.get_rect(center = (x+sq_size//2, y+sq_size//2)) 
                screen.blit(letter, surface)

            x += sq_size + margin
        y += sq_size + margin

    # update the screen
    pygame.display.flip()

    # tracking of user interaction
    for event in pygame.event.get():

        # closing the window stops the animation
        if event.type == pygame.QUIT:
            animating = False
        
        # User presses key
        elif event.type == pygame.KEYDOWN:

            # escape key to quit animation
            if event.key == pygame.K_ESCAPE:
                animating = False
            
            # backspace to delete characters
            if event.key == pygame.K_BACKSPACE:
                if len(input) > 0:
                    input = input[:len(input)-1]
            
            # return key to submit a guess
            elif event.key == pygame.K_RETURN:
                if len(input) == 5 and input in dict_guessing:
                    guesses.append(input)
                    unguessed = determine_unguessed_letters(guesses)
                    game_over = True if input == answer else False
                    input = ""
                elif len(input) == 5 and input not in dict_guessing:
                    input = ""

            # regular text input
            elif len(input) < 5 and not game_over:
                input = input + event.unicode.upper()
                