import sys

import pygame
import random
from pygame.locals import *
pygame.init()
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PINK = (255, 128, 128)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
DARKGREY = (43, 43, 43)
colours = {0: GREEN, 1: PINK, 2:BLUE, 3:RED, 4:WHITE, 5:ORANGE, 6:YELLOW, 7:PURPLE}
SCREENWIDTH = 600
SCREENHEIGHT = 600
FPS = 30
FONT = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption("MASTERMIND")
fpsClock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))


reds = 0
whites = 0
tries = 0

def setColourGuide(colours):
  colourGuide = []
  y = 10
  x = 50
  for i in range(len(colours)):
    colourGuide.append(Peg(28, 28, i))
    colourGuide[i].draw_peg(x, y)
    y += 40
  return colourGuide

def initialiseCode():
  code = []
  for i in range(4):
    digit = random.randint(0, 7)
    while digit in code:
      digit = random.randint(0, 7)
    code.append(digit)
  print(code)
  return code

def initialiseGrid():
  grid = []
  y = 20
  for i in range(12):
    row = []
    x = 172
    for j in range(4):
      row.append(Peg(28, 28, 0))
      row[j].draw_peg(x, y)
      row[j].square.x = x
      row[j].square.y = y
      x +=40
    y +=40
    grid.append(row)
  return grid

def checkWhichPeg(grid, eventPos, tries):
  for i in range(4):
    if grid[tries][i].square.collidepoint(eventPos):
      return i + 1
  return False

def checkCorrects(grid, tries, code):
  correct = 0
  for i in range(0, len(grid[tries])):
    if grid[tries][i].colour == code[i]:
      correct +=1
  return correct

def checkAnswer(grid, tries, code):
  wrongPlace = 0
  rightPlace = 0
  #for i in range(0, len(grid[tries])):
   # if grid[tries][i].colour in code and not(grid[tries][i].colour == code[i]):
    #  wrongPlace += 1
  colourList = []
  for i in range(0, len(grid[tries])):
    colourList.append(grid[tries][i].colour)
 # for i in range(0, len(code)):
 #   if colourList[i] in code and not(code[i] == colourList[i]):
  #    wrongPlace += 1
  codeCheck = code.copy()
  for i in range(len(codeCheck)):
    if codeCheck[i] in colourList:
      if codeCheck[i] == colourList[i]:
        rightPlace += 1
      else:
        wrongPlace += 1
      colourList[i] = "x"
      codeCheck[i] = "x"
  return wrongPlace, rightPlace

def applyPegs(pegList, grid, tries, reds, whites):
  tempList = []
  y = grid[tries][3].square.y 
  x = grid[tries][3].square.x + 40
  for i in range(4):
    if reds > 0:
      reds = reds - 1
      tempList.append(Peg(13, 13, 3))
      tempList[i].draw_peg(x, y)
    elif whites > 0:
      whites = whites - 1
      tempList.append(Peg(13, 13, 4))
      tempList[i].draw_peg(x, y)
  pegList.append(tempList)
  return pegList

def checkWin(reds):
  if reds == 4:
    return True
  else:
    return False

def buttonClicked(button, event):
  if event.type == MOUSEBUTTONDOWN and event.button == 1 and button.button.collidepoint(event.pos):
    return True
  else:
    return False

def drawResults(pegList):
  for i in range(len(pegList)):
    if len(pegList[i]) > 0:
      x = pegList[i][0].square.x
      y = pegList[i][0].square.y
      count = 0
      for j in range(len(pegList[i])):
        if count == 2:
          y = pegList[i][0].square.y + 14
          x = pegList[i][0].square.x
        pegList[i][j].draw_peg(x, y)
      
        x += 14
        count += 1

def endMessage(font, tries, win):
  if win == True:
    endText = Text(400, 200, font, f"Success after {tries} tries!", WHITE)
  else:
    endText = Text(400, 200, font, f"Game Over.", RED)
  return endText


class Peg:
  def __init__(self, length, width, colour):
    self.colour = colour
    self.length = length
    self.width = width
  def draw_peg(self, xPos, yPos):
    self.xPos = xPos
    self.yPos = yPos
    self.square = pygame.draw.rect(SCREEN, colours[self.colour], pygame.rect.Rect(self.xPos, self.yPos, self.length, self.width))
    #self.square = pygame.draw.circle(SCREEN, colours[self.colour], (self.xPos, self.yPos), self.length/2)

class Board:
  def __init__(self, length, width, colour, xPos, yPos):
    self.length = length
    self.width = width
    self.colour = colour
    self.xPos = xPos
    self.yPos = yPos
  def draw_board(self):
    self.base = pygame.draw.rect(SCREEN, self.colour, pygame.rect.Rect(self.xPos, self.yPos, self.width, self.length))
    self.holeY = self.yPos + 10
    for i in range(12):
      self.holeX = self.xPos + 10
      for j in range(5):
        pygame.draw.rect(SCREEN, DARKGREY, pygame.rect.Rect(self.holeX, self.holeY, 30, 30))
        self.holeX += 40
      self.holeY += 40
        
        


class Texture:
  def __init__(self, image):
    self.image = pygame.image.load(image)
  def resize(self, width, height):
    self.width = width
    self.height = height
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
  def draw_texture(self, xPos, yPos):
    self.xPos = xPos
    self.yPos = yPos
    SCREEN.blit(self.image, (self.xPos, self.yPos))

class Text:
  def __init__(self, length, width, font, text, colour):
    self.length = length
    self.width = width
    self.font = font
    self.text = text
    self.colour = colour
  def draw_text(self, xPos, yPos):
    self.xPos = xPos
    self.yPos = yPos
    self.render_text = self.font.render(self.text, True, self.colour)
    self.render_text.get_width()
    SCREEN.blit(self.render_text, ((self.xPos + (self.width -self.render_text.get_width())//2) , self.yPos))

class Button(Text):
  def __init__(self, length, width, font, text, textColour, buttonColour):
    super().__init__(length, width, font, text, textColour)
    self.buttonColour = buttonColour
  def draw_button(self, xPos, yPos):
    self.xPos = xPos
    self.yPos = yPos
    self.button = pygame.draw.rect(SCREEN, self.buttonColour, pygame.rect.Rect(self.xPos, self.yPos, self.width, self.length))

    

submitButton = Button(30, 100, FONT, "Submit", BLACK, RED)
board = Board(490, 210, GREY, 160, 8)
arrow = Texture("arrow.png")
arrow.resize(28, 28)
arrowY = 20
pegList = []
gameEnd = False
code = initialiseCode()
grid = initialiseGrid()
colourGuide = setColourGuide(colours)
playAgainButton = Button(30, 150, FONT, "Play Again", WHITE, BLUE)
playAgainButton.draw_button(300, 250)
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if gameEnd == False:
      if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
          if checkWhichPeg(grid, event.pos, tries) != False:
            i = checkWhichPeg(grid, event.pos, tries) - 1
            grid[tries][i].colour = (grid[tries][i].colour + 1) % 8
              
  
      if buttonClicked(submitButton, event):
        whites, reds = checkAnswer(grid, tries, code)
        #reds = checkCorrects(grid, tries, code)
        pegList = applyPegs(pegList, grid, tries, reds, whites)
        tries += 1
        arrowY += 40
        if checkWin(reds) == True:
          gameEnd = True
          endText = endMessage(FONT, tries, True)
          endText.draw_text(200, 200)
        elif tries == 12:
          gameEnd = True
          endText = endMessage(FONT, tries, False)
          endText.draw_text(200,200)
          
    if gameEnd == True:
      if buttonClicked(playAgainButton, event):
        gameEnd = False
        code = initialiseCode()
        grid = initialiseGrid()
        tries = 0
        pegList = []
        arrowY = 20
    
  SCREEN.fill(BLACK)
  if gameEnd == False:
    board.draw_board()
    for i in range(len(grid)):
      for j in range(len(grid[i])):
        grid[i][j].draw_peg(grid[i][j].square.x, grid[i][j].square.y)
    for i in range(len(colourGuide)):
      colourGuide[i].draw_peg(colourGuide[i].square.x, colourGuide[i].square.y)
    arrow.draw_texture(142, arrowY)
    submitButton.draw_button(400, 150)
    submitButton.draw_text(400, 150)
    drawResults(pegList)
  else:
    endText.draw_text(200, 200)
    playAgainButton.draw_button(300, 250)
    playAgainButton.draw_text(300, 250)
  pygame.display.flip()
  fpsClock.tick(FPS)  