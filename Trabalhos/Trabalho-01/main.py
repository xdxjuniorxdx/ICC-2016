# coding=UTF-8

# Permite que o programa consiga input do teclado sem [ENTER]
# i = getch()
from getchar import *
import os
# Info sobre a rodada
posY = 0
posX = 0
score = 0
arrow = 1;
life = 0 # Quanas vidas o jogador perdeu
mapa = [
["","","","",""],
["","Cc","C","Cc",""],
["","C","M","C",""],
["","Cc","C","Cc",""],
["","c","Cc","c",""],
["","","c","",""],
]

# ações e direções válidas
# um comando válido é da forma "[ação] + para + [direção]"
actions = ("mova", "olhe", "atire")
directions = ("direita", "esquerda", "cima", "baixo")

# imprime as informações sobre a rodada
def printStatus():
  print posY, posX, score

# imprime as informações que estão na posição x, y da matriz
def printMap(x, y):
  # como essa função estará dentro de outras
  # que já verificaram a existência desta posição,
  # não é necessário verificar novamente
  i = mapa[y][x]
  
  if not (i == ""):
    i = i.split(" ") # separa sensações diferentes
    print i

# verifica se a posição existe na matriz
def isValidPos(x, y):
  if x >= 0 and y >= 0:
    if x < len(mapa[0]) and y < len(mapa):
      return 1
  return 0

# movimenta o personagem
def move(x, y):
  global score
  score -= 1;
  
  # verifica se a posição é válida,
  # perceba que como a entrada é apenas direções,
  # não é necessário verificar se a casa é adjacente a atual
  if isValidPos(x, y):
    global posY # indica que a variável é a global, e não uma local
    posY = y
    
    global posX
    posX = x
    
    printMap(x, y) 

    printStatus()
    return 0
  else:
    print "Impossível de mover nessa direção!"
  return -1

def look(x, y):
  global score
  score -= 1
  if isValidPos(x, y):
    print printMap(x, y)
    return 0
  return -1

def shoot(x, y):
  global score
  global arrow
  score -= 1
  if isValidPos(x, y):
    if arrow > 0:
      if mapa[y][x] == "M":
        arrow -= 1;
        score += 10000
        print "G"
        return 0
    else:
      print "Você não tem mais flechas..."
  print "Não acertou nada..."
  return -1

def dirToPos( direction ):
  if direction == "direita":
    return (posX + 1, posY)
  elif direction == "esquerda":
    return (posX - 1, posY)
  elif direction == "cima":
    return (posX, posY - 1)
  elif direction == "baixo":
    return (posX, posY + 1)

def exeCmd( cmd, pos ):
  if cmd == "mova":
    return move(pos[0], pos[1])
  elif cmd == "olhe":
    return look(pos[0], pos[1])
  elif cmd == "atire":
    return shoot(pos[0], pos[1])
  return -1

def cmdIn( cmd ):
  if cmd[0] == "sair":
    print "Saindo... "
  else:
    if len(cmd) == 2:
      if cmd[0] in actions:
        if cmd[1] in directions:
          pos = dirToPos(cmd[1])
          return exeCmd(cmd[0], pos)
        else:
          print "Direção Inválida!"
          return -1
      else:
        print "Ação Inválida!"
        return -1
    else:
      print "Comando inválido!"
      return -1

def GameOver():
  score -= 10000
  print "Você morreu!"
  i = raw_input("Você gostaria de continuar?[s-sim|N-Não] ")
  i = i.lower()

  if i == "s":
    posY = 0
    posX = 0
  else:
    print "Saindo do jogo..."

def commandBaseInterface():
  global score
  command = "";
  while command != "sair": # Perceba que aqui command está totalmente em letras minusculas
    command = raw_input("Digite um comando: ")
    command = command.lower()
    cmd = command.split(" para ")
#    cmd = [i.lower() for i in cmd];
    
    cmdIn( cmd );
    
    if mapa[posY][posX] in ("M", "A"):
      GameOver()
    elif mapa[posY][posX] == "L":
      score += 1000
      print "Você achou o ouro!"
    printStatus();

# Mapa já visualizado
knownMap = [["" for i in range(0,len(mapa[0]))] for j in range(0,len(mapa))]

# tamanho do mapa exibido
sizeMapY = 2
sizeMapX = 3

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

# comando: mova, atire, olhe e cursor (este último em especial
# serve para o usuário verificar o mapa já visualizado...
command = ""
# desenha a interface

def draw():
  global cursorX
  global cursorY
  global posX
  global posY
  global cursor
  global sizeMapY
  global sizeMapX
  global posIntY
  global posIntX

  os.system('cls' if os.name == 'nt' else 'clear')
  print "+" + " Mundo do Wumpus ".center(78, "-") + "+"
  print "+" + "-"*78 + "+"
  print "Posição: ({0}, {1})  Score: {2}  Vida: {3}  Flechas: {4}".format( posX, posY, score, life, arrow ).center(80, " ")
  print "+" + "-"*78 + "+"
  
  # imprime o mapa
  for j in range(0, sizeMapY):
    i = j + posIntY
    line = ""
    if (cursor == 0 or i != cursorY) and i != posY: # sem cursor e nem personagem
      line = ". "*sizeMapX
    elif (cursor == 1 and i == cursorY) and i == posY: # cursor e personagem na mesma linha
      if posX >= posIntX and posX < sizeMapX + posIntX: # personagem visível
        if posX < cursorX: # personagem antes do cursor
          distLP = posX - posIntX
          distPC = cursorX - posX -1
          distCR = (posIntX + sizeMapX - 1) - cursorX
          line = ". "*distLP + chrPers + ". "*distPC + chrcursor + ". "*distCR
        elif cursorX < posX: # cursor antes de personagem
          distLC = cursorX - posIntX
          distCP = posX - cursorX - 1
          distPR = (posIntX + sizeMapX - 1) - posX
          line = ". "*distLC + chrcursor + ". "*distCP + chrPers + ". "*distPR
        elif posX == cursorX: # personagem e cursor na mesma posição
          distLC = cursorX - posIntX
          distCR = (posIntX + sizeMapX - 1) - cursorX
          line = ". "*distLC + chrcursor + ". "*distCR
      else: # apenas cursor, personagem não visível
          distLC = cursorX - posIntX
          distCR = (posIntX + sizeMapX - 1) - cursorX
          line = ". "*distLC + chrcursor + ". "*distCR
    elif i == posY: # apenas personagem, cursor em outra linha
      if posX >= posIntX and posX < sizeMapX + posIntX:
        distLP = posX - posIntX
        distPR = (posIntX + sizeMapX - 1) - posX
        line = ". "*distLP + chrPers + ". "*distPR
      else:
        line = ". "*sizeMapX
    else: # apenas cursor, personagem em outra linha
      distLC = cursorX - posIntX
      distCR = (posIntX + sizeMapX - 1) - cursorX
      line = ". "*distLC + chrcursor + ". "*distCR
    print "| " + line.center(76, " ") + " |"
  
  print "+" + " {0} ".format(knownMap[cursorY][cursorX]).center(78, "-") + "+"

# controla a interface
def textBaseInterface():
  global command
  global cursor
  global cursorY
  global cursorX
  global posIntY
  global posIntX
  print "Redimensione seu terminal de modo que a linha abaixo fique contínua (80 caracteres)"
  print "-"*80
  command = "";
  
  while command != "sair":
    draw()
    if cursor == 0:
      command = raw_input("   Digite um comando: ")
      command = command.lower()
      if command == "cursor":
        cursor = 1
        print "Para sair desse estado pressione 's'"
      else:
        cmd = command.split(" para ")
#        cmd = [i.lower() for i in cmd];
        
        cmdIn( cmd )
        # atualiza o mapa conhecido
        knownMap[posY][posX] = mapa[posY][posX]
        
        # rola a exibição do mapa se necessário
        if posY > posIntY + sizeMapY - 1:
          posIntY = posY - sizeMapY + 1
        elif posY < posIntY:
          posIntY = posY
        if posX > posIntX + sizeMapX - 1:
          posIntX = posX - sizeMapX + 1
        elif posX < posIntX:
          posIntX = posX
        print posY, posX, posIntY, posIntX

        
        if mapa[posY][posX] in ("M", "A"):
          GameOver()
        elif mapa[posY][posX] == "L":
          score += 1000
          print "Você achou o ouro!"
    else:
      i = getch();
      if i == '\x1b': #teclas especiais
        getch() # isso retorna '['
        i = getch() # é necessário 3 "lidas" no Linux
        if i == 'A': # seta para cima
          cursorY -= 1 
          print "up"
        elif i == 'B': # seta para baixo
          cursorY += 1
          print "down"
        elif i == 'C': # seta para direita
          cursorX += 1
          print "right"
        elif i == 'D': # seta para a esquerda
          cursorX -= 1
          print "left"
        
        # determina limites para o cursor
        if cursorY < 0:
          cursorY = 0
        elif cursorY >= len(mapa):
          cursorY = len(mapa) -1 # cursor inicia no 0
        if cursorX < 0:
          cursorX = 0
        elif cursorX >= len(mapa[0]):
          cursorX = len(mapa[0]) - 1 # cursor inicia no 0
        # rola a exibição do mapa se necessário
        if cursorY > posIntY + sizeMapY - 1:
          posIntY = cursorY - sizeMapY + 1
        elif cursorY < posIntY:
          posIntY = cursorY
        if cursorX > posIntX + sizeMapX - 1:
          posIntX = cursorX - sizeMapX + 1
        elif cursorX < posIntX:
          posIntX = cursorX
        print cursorY, cursorX, posIntY, posIntX
      elif i == 's':
        cursor = 0
        print "Voltando ao modo normal..."

def main():
  i = raw_input("Você quer executar a Interface Textual? [s(im)|N(ão)] ");
  i = i.lower()
  if i == "s":
    textBaseInterface()
  else:
    commandBaseInterface()

main()
