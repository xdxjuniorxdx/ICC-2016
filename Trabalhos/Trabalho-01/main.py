# -*- coding: utf-8 -*-

from random import randint
import os
import sys
import getchar
import time
getch = getchar.getch

posY = 0
posX = 0

score = 0
arrow = 1
life = 0
gold = 0
wumpus = 1
movLeft = 0

mapa = []
actions = ("mova", "olhe", "atire")
directions = ("direita", "esquerda", "cima", "baixo")

output = ""
error = 0

# Mapa já visualizado
knownMap = []

# tamanho máximo do mapa exibido
maxSizeMapY = 15
maxSizeMapX = 20

# tamanho do mapa exibido
sizeMapX = maxSizeMapX
sizeMapY = maxSizeMapY

# posição do mapa (scroll)
posIntY = 0
posIntX = 0

# posição do cursor
cursorY = 0
cursorX = 0

# caracteres representativos
chrPers = "x "
chrcursor = "| "

# 'booleano' que indica se o usuário está movendo o cursor
cursor = 0

# comando: mova, atire, olhe e cursor (este último em especial serve para o usuário verificar o mapa já visualizado...)
command = ""

if sys.platform.startswith("win"): # Windows não imprime corretamente caracteres unicode....
  charPoint = ['<', '>', '^', 'v']
else:
  charPoint = [u'\u25c2', u'\u25b8', u'\u25b4', u'\u25be'] # caracteres unicode "triângulo pequeno"

# imprime as informações sobre a rodada
def printStatus():
  global posY, posX
  global score, life, arrow, movLeft
  global mapa
  print u"Posição: ({0}, {1})  Score: {2}  Vida: {3}  Flechas: {4}  Mov. rest: {5}  Mapa: {6}x{7}".format( posX, posY, score, life, arrow, movLeft, len(mapa), len(mapa[0]) )

# retorna String com uma lista de sensações
def listSense( x, y ):
  global knownMap
  s = ""
  for i in knownMap[y][x].split(" "):
    if i == "C":
      s += "cheiro forte "
    elif i == "cC":
      s += "cheiro medio "
    elif i == "c":
      s += "cheiro fraco "
    elif i == "B":
      s += "brisa forte "
    elif i == "bB":
      s += "brisa media "
    elif i == "b":
      s += "brisa fraca "
  if s == "":
    s = "nada "
  return s

# verifica se a posição existe na matriz
def isValidPos(x, y):
  global mapa
  if x >= 0 and y >= 0:
    if x < len(mapa[0]) and y < len(mapa):
      return 1
  return 0

# movimenta o personagem
def move(x, y):
  global posX, posY
  global score, movLeft, gold, life
  global output
  global mapa
  score -= 1
  movLeft -= 1
  
  # verifica se a posição é válida,
  # perceba que como a entrada é apenas direções,
  # não é necessário verificar se a casa é adjacente a atual
  if isValidPos(x, y):
    posY = y
    posX = x
    if ("M" in mapa[y][x].split(" ")) or ("A" in mapa[y][x].split(" ")):
      GameOver()
      return -4 # morte
    elif posX + posY == 0: # posx = 0 e posy = 0
      if life == 0:
        if gold > 0: # Sair da caverna após ter conseguido o ouro
          score += 1000 # Sair da caverna
          endGame()
          return 0 # jogo terminou
    output = mapa[y][x]
    knownMap[y][x] = mapa[y][x]
    if knownMap[y][x] == '':
      knownMap[y][x] = "!"
    return 1 # movimento sem erros
  return -6

def look(x, y):
  global mapa, knownMap
  global score, output
#  movLeft -= 1
  score -= 1
  if isValidPos(x, y):
    if ("M" in mapa[y][x].split(" ")) or ("A" in mapa[y][x].split(" ")):
      GameOver()
      return -4 # morte
    output = mapa[y][x]
    knownMap[y][x] = mapa[y][x]
    return 2 # sem problemas
  return -6 # posição inválida

def shoot(x, y):
  global score, arrow, wumpus, output
  global mapa, knownMap
  if isValidPos(x, y):
    if arrow > 0:
      arrow -= 1;
      if "M" in mapa[y][x].split(" "):
        score += 10000
        output = "G"
        wumpus = 0
        mapa[y][x] = mapa[y][x].replace("M", "")
        knownMap[y][x] = knownMap[y][x].replace("M", "")
        return 3 # Acertou 
      else:
        output = ""
        return 4 # não acertou
    else: #sem flechas
      return -5
  return -6 # Posição inválida

# converte direção para posição
def dirToPos( direction ):
  global posX, posY
  if direction == "direita":
    return (posX + 1, posY)
  elif direction == "esquerda":
    return (posX - 1, posY)
  elif direction == "cima":
    return (posX, posY - 1)
  elif direction == "baixo":
    return (posX, posY + 1)

# verifica se um comando é válido
def isValidCommand( cmd ):
  global actions, directions
  if len(cmd) == 2:
    if cmd[0] in actions:
      if cmd[1] in directions:
        return 1
  return 0 # Comando Inválida!

# maneja o comando
def handleCommand( action, x, y ):
  if action == "mova":
    return move(x, y)
  elif action == "olhe":
    return look(x, y)
  elif action == "atire":
    return shoot(x, y)

# temina o jogo sem perda de pontos
def endGame():
  global score, command, life
  print u"Sua pontuação final foi: " + str(score)
  command = "sair"
  life += 1

#termina o jogo com perda de pontos
def GameOver():
  global score, posX, posY
  score -= 10000
  print u"Você morreu!"
  i = raw_input("Você gostaria de continuar?[s-sim|N-Não] ")
  i = i.lower()

  if i == "s":
    posY = 0
    posX = 0
  else:
    endGame()

# início das funções de interfaces
def commandBaseInterface():
  global posX, posY
  global score, gold
  global error, command, output
  global mapa, knownMap
  output = ""
  if command == "sair":
    print "Saindo..."
  else:
    cmd = command.split(" para ")
    if isValidCommand( cmd ) == 1:
      newPos = dirToPos( cmd[1] )
      error = handleCommand( cmd[0], newPos[0], newPos[1] )
    else:
      print u"Comando inválido!"
    
    if error < 0:
      if error == -4:
        print u"Você Morreu..."
      elif error == -5:
        print u"Você está sem flechas..."
      elif error == -6:
        print u"Posição Inválida"
    else:
      if error == 1: # Moveu sem nunhum problema
        knownMap[posY][posX] = mapa[posY][posX]
      elif error == 2: # Olhou sem nenum problema
#        knownMap[newPos[1]][newPos[0]] = output
        print u"Você sentirá: {2}".format(listSense(newPos[0], newPos[1]))
      elif error == 3: # acertpu o tiro
        print u"Você matou Wumpus!!!"
      elif error == 4: # errou
        print u"Você não matou nada..."
    
    if "L" in mapa[posY][posX].split(" "):
      score += 1000
      print u"Você achou o ouro!"
      gold += 1
      mapa[posY][posX] = mapa[posY][posX].replace("L", "")
    print u"Você está sentindo: " + listSense(posX, posY)
    print "\n"
  printStatus();

##############################################
# caracteres com acento ou especiais contam como 2
def numSpecialChr( s ):
  j = 0
  for i in s:
    if ord(i) >= 194: # special character
      j += 1
  return j

def ctrTxt( s, n, Chr ):
  return s.center( n + numSpecialChr( s ), Chr )

def drawLine1(x1, chr1):
  global sizeMapX, mapa, posIntX
  distLC = x1 - posIntX
  distCR = (posIntX + sizeMapX - 1) - x1
  return ". "*distLC + chr1 + ". "*distCR

# retorna uma linha para ser desenhada x1 < x2
def drawLine2(x1, chr1, x2, chr2):
  global sizeMapX, mapa, posIntX
  distLP = x1 - posIntX
  distPC = x2 - x1 -1
  distCR = (posIntX + sizeMapX - 1) - x2
  return ". "*distLP + chr1 + ". "*distPC + chr2 + ". "*distCR

# desenha a interface
def draw(info):
  global cursorX, cursorY, cursor
  global posX, posY, sizeMapY, sizeMapX, posIntY, posIntX
  global mapa, score, arrow, life, movLeft, gold
  global chrPers, chrcursor
  global error
  
  os.system('cls' if sys.platform.startswith('win') else 'clear')
  print "+" + " Mundo do Wumpus ".center(78, "-") + "+"
  print "+" + "-"*78 + "+"
  print u"Posição: ({0}, {1})  Score: {2}  Vida: {3}  Flechas: {4}  Mov. rest: {5}".format( posX, posY, score, life, arrow, movLeft ).center(80, " ")
  print "+" + "-"*78 + "+"
  
  if posIntY > 0:
    print "|" + charPoint[2].center(78, " ") + "|"
  else:
    print "|" + " "*78 + "|"
  
  # imprime o mapa
  for j in range(0, sizeMapY):
    i = j + posIntY
    line = ""
    if (cursor == 0 or i != cursorY) and i != posY: # sem cursor e nem personagem
      line = ". "*sizeMapX
    elif (cursor == 1 and i == cursorY) and i == posY: # cursor e personagem na mesma linha
      if posX >= posIntX and posX < sizeMapX + posIntX: # personagem visível
        if posX < cursorX: # personagem antes do cursor
          line = drawLine2(posX, chrPers, cursorX, chrcursor)
        elif cursorX < posX: # cursor antes de personagem
          line = drawLine2(cursorX, chrcursor, posX, chrPers)
        elif posX == cursorX: # personagem e cursor na mesma posição
          line = drawLine1(cursorX, chrcursor)
      else: # apenas cursor, personagem não visível
          line = drawLine1(cursorX, chrcursor)
    elif i == posY: # apenas personagem, cursor em outra linha
      if posX >= posIntX and posX < sizeMapX + posIntX:
        line = drawLine1(posX, chrPers)
      else:
        line = ". "*sizeMapX
    else: # apenas cursor, personagem em outra linha
      line = drawLine1(cursorX, chrcursor)
    
    if j == sizeMapY/2:
      if posIntX > 0:
        if len(mapa[0]) - posIntX > sizeMapX:
          print "| " + charPoint[0] + line.center(74, " ") + charPoint[1] + " |" # \u25C2 = ◂ \u25B8 = ▸
        else:
          print "| " + charPoint[0] + line.center(74, " ") + "  |"
      else:
        if len(mapa[0]) - posIntX > sizeMapX:
          print "|  " + line.center(74, " ") + charPoint[1] + " |" # \u25B8 = ▸
        else:
          print "|  " + line.center(74, " ") + "  |"
    else:
      print "|  " + line.center(74, " ") + "  |"
  
  if len(mapa) - posIntY > sizeMapY:
    print "|" + charPoint[3].center(78, " ") + "|" # ▾
  else:
    print "|" + " "*78 + "|"
  
  info = ctrTxt(info, 76, "-")
  
  print "+ " + info + " +"

def rollMap( x, y ):
  global posIntX, posIntY, sizeMapX, sizeMapY
  if y > posIntY + sizeMapY - 1:
    posIntY = y - sizeMapY + 1
  elif y < posIntY:
    posIntY = y
  if x > posIntX + sizeMapX - 1:
    posIntX = x - sizeMapX + 1
  elif x < posIntX:
    posIntX = x

def cursorCtrl( Chr, up, down, right, left ):
  global cursorX, cursorY
  if Chr == up:
    if isValidPos( cursorX, cursorY - 1 ):
      cursorY -= 1
  elif Chr == down:
    if isValidPos( cursorX, cursorY + 1 ):
      cursorY += 1
  elif Chr == right:
    if isValidPos( cursorX + 1, cursorY ):
      cursorX += 1
  elif Chr == left:
    if isValidPos( cursorX - 1, cursorY ):
      cursorX -= 1

# controla a interface
def textBaseInterface():
  global movLeft
  global command
  global cursor, cursorY, cursorX
  global posIntY, posIntX
  global sizeMapY, sizeMapX
  global score, error, gold
  global mapa, knowMap
  
  info = ""
  output = ""
  error = 0
  if cursor == 0: # cursor inativo
    if command == "cursor":
      cursor = 1
      info = "Para sair desse estado pressione 's'"
    elif command == "sair":
      print "Saindo..."
    else:
      cmd = command.split(" para ")
      if isValidCommand( cmd ) == 1:
        newPos = dirToPos( cmd[1] )
        error = handleCommand( cmd[0], newPos[0], newPos[1] )
      else:
        error = -1
      
      # rola a exibição do mapa se necessário
      rollMap( posX, posY )
      
      if "L" in mapa[posY][posX].split(" "):
        score += 1000
        gold += 1
        # atualiza o mapa conhecido
        mapa[posY][posX] = mapa[posY][posX].replace("L", "")
        knownMap[posY][posX] = knownMap[posY][posX].replace("L", "")
        info = " Voce achou o ouro!!! "
    
    if error < 0:
      if error == -1:
        info = " Comando Invalido "
      elif error == -4:
        info = " Voce Morreu.... "
      elif error == -5:
        info = " Voce esta sem flechas... "
      elif error == -6:
        info = " Posicao Invalida "
    else:
      if error == 1:
        info = " Voce esta sentindo: " + listSense(posX, posY)
      elif error == 2: # Olhou sem nenum problema
#        knownMap[newPos[1]][newPos[0]] = output
        info = "Na posicao ({0}, {1}) voce sentira: {2} ".format( newPos[0], newPos[1], listSense(newPos[0], newPos[1]) )
      elif error == 3: # acertpu o tiro
        info = "Voce matou Wumpus!!!"
      elif error == 4: # errou
        info = "Voce nao matou nada..."
  else: # cursor ativo
    i = getch();
    if sys.platform.startswith("win"): # Windows
      if ord(i) == 224:
        cursorCtrl( getch(), 'H', 'P', 'M', 'K' )
    elif sys.platform.startswith("linux"): # linux
      if i == '\x1b': #teclas especiais
        getch() # isso retorna '['
        cursorCtrl( getch(), 'A', 'B', 'C', 'D' )
    info = " Voce esta sentindo: " + listSense( cursorX, cursorY )
    if i == 's':
      cursor = 0
   
    #rola a exibição do mapa se necessário
    rollMap( cursorX, cursorY )
  draw(info)

#######################################################

def getMaxIndex(a):
  maximum = 0
  index = -1
  for i,value in enumerate(a):
    if value > maximum:
      maximum = value
      index = i
  return index

def isBinaryArray(a):
  for i in a:
    if (i != 0) and (i !=  1):
      return 0
  return 1

def getIndex( elem, a ):
  if elem in a:
    return a.index( elem )
  return -1

def searchAround( x, y, elem ):
  global knownMap
  r = 0
  # direita
  if isValidPos( x + 1, y ):
    if elem in knownMap[y][ x + 1 ].split(" "):
      r += 1
  # esquerda
  if isValidPos( x - 1, y ):
    if elem in knownMap[y][ x - 1 ].split(" "):
      r += 1
  # cima
  if isValidPos( x, y - 1 ):
    if elem in knownMap[ y - 1 ][x].split(" "):
      r += 1
  # baixo
  if isValidPos( x, y + 1 ):
    if elem in knownMap[ y + 1 ][x].split(" "):
      r += 1
  return r

#limpar casas marcadas como possível ?_ incorretamente
def cleanWrongMark( x, y, mark, StrongSense ):
  global knownMap
  
  if not(StrongSense in knownMap[y][x]):
    # direita
    if isValidPos( x + 1, y ):
      if mark in knownMap[y][ x + 1 ].split(" "):
        knownMap[y][ x + 1 ] = knownMap[y][ x + 1 ].replace(" " + mark, "")
    # esquerda
    if isValidPos( x - 1, y ):
      if mark in knownMap[y][ x - 1 ].split(" "):
        knownMap[y][ x - 1 ] = knownMap[y][ x - 1 ].replace(" " + mark, "")
    # cima
    if isValidPos( x, y - 1 ):
      if mark in knownMap[ y - 1 ][x].split(" "):
        knownMap[ y - 1 ][x] = knownMap[ y - 1 ][x].replace(" " + mark, "")
    # baixo
    if isValidPos( x, y + 1 ):
      if mark in knownMap[ y + 1 ][x].split(" "):
        knownMap[ y + 1 ][x] = knownMap[ y + 1 ][x].replace(" " + mark, "")

def setMark( x, y, possibleMove, mark ):
  # direita
  if possibleMove[0] > 1:
    if not(mark in knownMap[y][ x + 1 ]):
      knownMap[y][ x + 1 ] += mark
  # esquerda
  if possibleMove[1] > 1:
    if not(mark in knownMap[y][ x - 1 ]):
      knownMap[y][ x - 1 ] += mark
  # cima
  if possibleMove[2] > 1:
    if not(mark in knownMap[ y - 1 ][x]):
      knownMap[ y - 1 ][x] += mark
  # baixo
  if possibleMove[3] > 1:
    if not(mark in knownMap[ y + 1 ][x]):
      knownMap[ y + 1 ][x] += mark

def count( elem, a ):
  r = 0
  for i in a:
    if i == elem:
      r += 1
  return r

def getKnownMap(x, y):
  global knownMap
  if isValidPos(x, y) == 1:
    return knownMap[y][x]
  return ""

oldPossibleMove = [0,0,0,0]
def ai():
  global posX, posY
  global actions, directions, arrow, gold
  global knownMap
  global command
  global oldPossibleMove
  if knownMap[posY][posX] == "":
    knownMap[posY][posX] = "!"
  # 0  - movimento impossível
  # 1  - movimento já realizado
  # 2+ - por preferência
  # ?a - possível casa com abismo
  # ?w - possível casa com monstro
  
  brisa = ['b','bB','B','?a']
  cheiro = ['c','cC','C','?w']
  act = 0 # ação a ser executada segundo actions
  possibleMove = [4,5,6,3] # direita, esquerda, cima, baixo
  
  if isValidPos( posX + 1, posY ) == 0:# direita inválida
    possibleMove[0] = 0
  if isValidPos( posX - 1, posY ) == 0:# esquerda inválida
    possibleMove[1] = 0
  if isValidPos( posX, posY - 1 ) == 0:# cima inválida
    possibleMove[2] = 0
  if isValidPos( posX, posY + 1 ) == 0:# baixo inválida
    possibleMove[3] = 0
  
  cleanWrongMark(posX, posY, "?a", brisa[2])
  cleanWrongMark(posX, posY, "?w", cheiro[2])

  if (wumpus == 1) or (gold == 0):
    # casas já percorridas
    # direita
    if possibleMove[0] != 0:
      if getKnownMap(posX + 1, posY) != "":
        possibleMove[0] = 1
    # esquerda
    if possibleMove[1] != 0:
      if getKnownMap(posX - 1, posY) != "":
        possibleMove[1] = 1
    # cima
    if possibleMove[2] != 0:
      if getKnownMap(posX, posY - 1) != "":
        possibleMove[2] = 1
    # baixo
    if possibleMove[3] != 0:
      if getKnownMap(posX, posY + 1) != "":
        possibleMove[3] = 1
  
  sensations = knownMap[posY][posX].split(" ")
  if wumpus == 1:
    if cheiro[2] in sensations:
      i = searchAround(posX, posY, "?w");
      if i == 1 and arrow > 0:
        # direita
        if getIndex( "?w", getKnownMap(posX + 1, posY) ) >= 0:
          possibleMove[0] = 10
        # esquerda
        if getIndex( "?w", getKnownMap(posX - 1, posY) ) >= 0:
          possibleMove[1] = 10
        # cima
        if getIndex( "?w", getKnownMap(posX, posY - 1) ) >= 0:
          possibleMove[2] = 10
        # baixo
        if getIndex( "?w", getKnownMap(posX, posY + 1) ) >= 0:
          possibleMove[3] = 10
        act = 2 # atirar
      else:
        setMark(posX, posY, possibleMove, " ?w")
        for i, j in enumerate(possibleMove):
          if j > 2:
            possibleMove[i] = 0
  
  if brisa[2] in sensations:
    j = count(brisa[2], sensations)
    i = searchAround(posX, posY, "?a");
    # direita
    if getIndex( "?a", getKnownMap(posX + 1, posY) ) >= 0:
      possibleMove[0] = 0
    # esquerda
    if getIndex( "?a", getKnownMap(posX - 1, posY) ) >= 0:
      possibleMove[1] = 0
    # cima
    if getIndex( "?a", getKnownMap(posX, posY - 1) ) >= 0:
      possibleMove[2] = 0
    # baixo
    if getIndex( "?a", getKnownMap(posX, posY + 1) ) >= 0:
      possibleMove[3] = 0
    if j > i:
      setMark(posX, posY, possibleMove, " ?a")
      for i, j in enumerate(possibleMove):
        if j > 2:
          possibleMove[i] = 0
  print possibleMove
  if isBinaryArray(possibleMove) == 0:
    d = getMaxIndex(possibleMove)
  else:
    d = -1
    i = 0
    while (d < 0) and (i < 4):
      if oldPossibleMove[i] != 0:
        if possibleMove[i] != 0:
          d = i
      print i
      i += 1
    if d == -1:
      d = getMaxIndex(possibleMove)
  if d < 0 or act == -1 or command == "sair":
    command = "sair"
  else:
    command = actions[act] + " para " + directions[d]
  print "   Digite um comando: ", command
  oldPossibleMove = possibleMove
  time.sleep(0.2)

#######################################################
def leituraArquivo():
  with open(sys.argv[0].replace("mainWin.py","") + 'matriz.txt', 'r') as f:
    l = int(f.readline())
    c = int(f.readline())
    i = 0
    z = 0
    matriz = []
    m = f.read().splitlines()
    stop = l*c
    for i in range (l):
      j = 0
      linha = []
      for j in range (c):
        linha.append(m[z])
        z = z + 1
        
      matriz = matriz + [linha]
    f.close()
  return matriz

def main():
  global sizeMapX, sizeMapY
  global maxSizeMapX, maxSizeMapY
  global mapa, knownMap
  global movLeft, command
  mapa = leituraArquivo()
  for i in mapa:
    print i
  knownMap = [["" for i in range(0,len(mapa[0]))] for j in range(0,len(mapa))]
  knownMap[0][0] = mapa[0][0];
  movLeft = len(mapa) * len(mapa[0])
  
  if maxSizeMapX > len(mapa[0]):
    sizeMapX = len(mapa[0])
  if maxSizeMapY > len(mapa):
    sizeMapY = len(mapa)
  
  i = raw_input("Voce quer executar a Interface Textual? [s(im)|N(ao)] ");
  i = i.lower()
  
  j = raw_input("Voce quer executar a AI? [s(im)|N(ao)] ")
  j.lower()
  
  if i == "s":
    print u"Redimensione seu terminal de modo que a linha abaixo fique contínua (80 caracteres).\nPressione [ENTER] quando estiver pronto"
    print "-"*80
    raw_input() # esperar até que o usuario tecle [ENTER]
    
    draw(" Voce esta sentindo: " + listSense(0,0))
    while command != "sair":
      output = ""
      if movLeft <= 0:
        print u"Você não pode mais se movimentar"
        endGame()
      else:
        if j != 's':
          if cursor == 0:
            command = raw_input("   Digite um comando: ")
            command = command.lower()
        else:
          ai()
        textBaseInterface()
  else:
    printStatus();
    while command != "sair":
      if movLeft <= 0:
        print u"Você não pode mais se movimentar"
        endGame()
      else:
        if j != 's':
          command = raw_input("Digite um comando: ")
          command = command.lower()
        else:
          ai()
        commandBaseInterface()

main()
