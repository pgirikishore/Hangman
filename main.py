import pygame
import math
import urllib.request, json
import random
import config

#API init
with urllib.request.urlopen(config.api_link.format(random.randint(1, 376)))as url:
  data = json.loads(url.read().decode())

while True:
  li = random.choice(data['results'])
  if li['original_language']=='en':
    #print(li["original_title"])
    break


#init and setup
pygame.init()
width, height = 800, 500
white = 255, 255, 255
black = 0, 0, 0
#load images
images = []
for i in range(7):
  img = pygame.image.load("hangman{}.png".format(i))
  images.append(img)
print(images)

#button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((width - (RADIUS * 2 + GAP)*13) /2)
starty = 400
for i in range(26):
  x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i%13))
  y = starty + ((i// 13) * (GAP + RADIUS * 2))
  letters.append([x,y, chr(65+i), True])
  
# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Hangman")

running = True
clock = pygame.time.Clock()

#game variables
hang_status = 0
word = li['original_title'].upper().split()
#print(word)
w = "".join(word)
guessed = []

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words1 = [word1.split('  ') for word1 in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size('  ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words1:
        for word1 in line:
            word_surface = font.render(word1, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def draw():
  screen.fill(white)
  screen.blit(images[hang_status],(80,100))

  #draw title
  text = TITLE_FONT.render("HANGMAN", 1, black)
  screen.blit(text, (width/2 - text.get_width()/2, 20))


  #draw words
  display_word = ""
  for words in word:
    for letter in words:
      if letter in guessed and letter.isalpha:
        display_word += letter + " "
      elif not letter.isalpha():
        display_word +=letter+" "
      elif letter not in guessed:
        display_word +="_ "
    display_word +=" "
  #print(display_word)
  blit_text(screen,display_word, (350,200), WORD_FONT, black)


  for letter in letters:
    x,y, ltr, visible = letter
    if visible:
      pygame.draw.circle(screen,(0,0,0), (x,y), RADIUS, 3)
      text = LETTER_FONT.render(ltr,1,(0,0,0))
      screen.blit(text,(x - text.get_width()/2, y - text.get_height()/2))

while running:

  for event in pygame.event.get():
    if event == pygame.QUIT:
      running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
      m_x, m_y = pygame.mouse.get_pos()
      for letter in letters:
        x, y, ltr, visible = letter
        if visible:
          dis = math.sqrt((x-m_x)**2 + (y - m_y)**2)
          if dis<RADIUS:
            guessed.append(ltr)
            print(guessed)
            letter[3] = False 
            if ltr not in w:
              hang_status += 1
    
  won = True
  for letter in w:
    if letter.isalpha() and letter not in guessed:
      won = False
    #print(event)

  draw() 
  pygame.display.flip()

  if won:
    pygame.time.delay(1000)
    screen.fill(white)
    text = WORD_FONT.render("You WON!",1 , black)
    screen.blit(text,(width/2 - text.get_width()/2, height/2-text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    print("Won")
    break

  if hang_status == 6:
    pygame.time.delay(1000)
    screen.fill(white)
    text = WORD_FONT.render("You LOST!",1 , black)
    screen.blit(text,(width/2 - text.get_width()/2, height/2-text.get_height()/2))
    pygame.display.update()


    blit_text(screen,"Movie:{}".format(li['original_title']), (width/2 - text.get_width()/2, (height/2-text.get_height()/2) + 50), LETTER_FONT, black)
    pygame.display.update()

    pygame.time.delay(4000)
    print("Lost")
    break
  clock.tick(60)

pygame.quit()
