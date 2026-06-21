import sys

def parseArmy(fullLine, origName, file):
    print(f"parse {origName} in line {fullLine}")
    fullLine = fullLine[2:]
    lines = fullLine.split(",")
    for line in lines:
      print(f"parse line {line} len {len(line)}")
      if len(line) < 3:
          continue
      numbers = line.split(' ')
      x = int(numbers[0])
      y = int(numbers[1])
      flags = 0
      na = 0
      name = origName
      if (len(numbers) > 2):
          flags = int(numbers[2])
      if flags >= 128:
          name += " (ЛВ)"
      if flags - flags//64 == 32:
          na = 1
      name = name + (" " * (14 - len(name)))
      if na == 0:
         fileLine = f" {name} | {x:02d}-{y:02d} |       |       |       |       |       |       |\n"
      else: 
         fileLine = f" {name} | {x:02d}-{y:02d} |  N/A  |  N/A  |  N/A  |  N/A  |  N/A  |  N/A  |\n" 
      print(fileLine)
      file.write(fileLine)

def parseUnitAction(fullLine, origName, file, isNotDL):
    print(f"parse {origName} in line {fullLine}")
    fullLine = fullLine[2:]
    lines = fullLine.split(",")
    for line in lines:
      print(f"parse line {line}")
      if len(line) < 3:
        continue
      numbers = line.split(' ')
      x = int(numbers[0])
      y = int(numbers[1])
      flags = 0
      na = 0
      name = origName
      if (len(numbers) > 2):
          flags = int(numbers[2])
      if flags >= 128:
          if isNotDL == 1:
              name += " (ЛВ)"
          else:
              name += " (Ст)"
      if flags - flags//64 == 32:
          na = 1
      name = name + (" " * (18 - len(name)))
      if na == 0:
         fileLine = f" {name} | {x:02d}-{y:02d} |                                       |\n"
      else: 
         fileLine = f" {name} | {x:02d}-{y:02d} |                    N/A                |\n"
      print(fileLine)
      file.write(fileLine)

with open(sys.argv[1], 'r', encoding='cp1251') as rfile:
    with open('moveOrders.txt', 'w', encoding='cp1251') as wfile:
        lineNumber = 1
        year = 0
        readPlayerLine = 0
        for line in rfile:
            if lineNumber == 2:
                year = line
            if readPlayerLine == 1:
                wfile.write(f"Год {year}")
                wfile.writelines(line)
                wfile.write(f"----------------|-------|-------|-------|-------|-------|-------|-------|\n")
                wfile.write(f"     Войско     |  X-Y  | Ход 1 | Ход 2 | Ход 3 | Ход 4 | Ход 5 | Ход 6 |\n")
                wfile.write(f"----------------|-------|-------|-------|-------|-------|-------|-------|\n")
            elif line.startswith('г '):
                parseArmy(line, 'Гном', wfile)
            elif line.startswith('в '):
                parseArmy(line, 'Варвар', wfile)
            elif line.startswith('э '):
                parseArmy(line, 'Ильв', wfile)
            elif line.startswith('о '):
                parseArmy(line, 'Эвогр', wfile)
            elif line.startswith('п '):
                parseArmy(line, 'Л. Пехота', wfile)
            elif line.startswith('р '):
                parseArmy(line, 'Рыцарь', wfile)
            elif line.startswith('м '):
                parseArmy(line, 'Маг', wfile)
            elif line.startswith('з '):
                parseArmy(line, 'Зомби', wfile)
            elif line.startswith('д '):
                parseArmy(line, 'Дракон', wfile)
            elif line.startswith('ф '):
                parseArmy(line, 'Корабль', wfile)
            if 'Player' in line:
                print(f"Player found") 
                if readPlayerLine == 0:
                    wfile.write("```" + '\n')
                else:
                    wfile.write('\n' + "```" + '\n-----\n' + "```" + '\n')
                readPlayerLine = 1
            elif readPlayerLine > 0:
                readPlayerLine += 1
            else: 
                readPlayerLine = 0

            if 'END' in line:
                print(f"END") 
                wfile.write('\n' + "```")
            
            lineNumber += 1
        wfile.write('\n' + "=============================================================" + '\n')
with open(sys.argv[1], 'r', encoding='cp1251') as rfile:
    with open('moveOrders.txt', 'a', encoding='cp1251') as wfile:
        lineNumber = 1
        year = 0
        readPlayerLine = 0
        for line in rfile:
            if lineNumber == 2:
                year = line
            if readPlayerLine == 1:
                wfile.write(f"Год {year}")
                wfile.writelines(line)
                wfile.write(f"--------------------|-------|---------------------------------------|\n")
                wfile.write(f"      Юнит          |  X-Y  |                  Действие             |\n")     
                wfile.write(f"--------------------|-------|---------------------------------------|\n")
            elif line.startswith('г '):
                parseUnitAction(line, 'Гном', wfile, 1)
            elif line.startswith('в '):
                parseUnitAction(line, 'Варвар', wfile, 1)
            elif line.startswith('э '):
                parseUnitAction(line, 'Ильв', wfile, 1)
            elif line.startswith('о '):
                parseUnitAction(line, 'Эвогр', wfile, 1)
            elif line.startswith('п '):
                parseUnitAction(line, 'Л. Пехота', wfile, 1)
            elif line.startswith('р '):
                parseUnitAction(line, 'Рыцарь', wfile, 1)
            elif line.startswith('м '):
                parseUnitAction(line, 'Маг', wfile, 1)
            elif line.startswith('з '):
                parseUnitAction(line, 'Зомби', wfile, 1)
            elif line.startswith('д '):
                parseUnitAction(line, 'Дракон', wfile, 1)
            elif line.startswith('ф '):
                parseUnitAction(line, 'Корабль', wfile, 1)
            elif line.startswith('К '):
                parseUnitAction(line, 'Крепость', wfile, 1)
            elif line.startswith('Г '):
                parseUnitAction(line, 'Город', wfile, 0)
            elif line.startswith('З '):
                parseUnitAction(line, 'Замок', wfile, 0)
            elif line.startswith('П '):
                parseUnitAction(line, 'Поместье', wfile, 0)
            elif line.startswith('Б '):
                parseUnitAction(line, 'Башня', wfile, 0)
            elif line.startswith('C '):
                parseUnitAction(line, 'Медный р-к', wfile, 1)
            elif line.startswith('S '):
                parseUnitAction(line, 'Серебряный р-к', wfile, 1)
            elif line.startswith('G '):
                parseUnitAction(line, 'Золотой р-к', wfile, 1)
            elif line.startswith('M '):
                parseUnitAction(line, 'Мифриловый р-к', wfile, 1)
            if 'Player' in line:
                print(f"Player found") 
                if readPlayerLine == 0:
                    wfile.write("```" + '\n')
                else:
                    wfile.write('\n' + "```" + '\n-----\n' + "```" + '\n')
                readPlayerLine = 1
            elif readPlayerLine > 0:
                readPlayerLine += 1
            else: 
                readPlayerLine = 0

            if 'END' in line:
                print(f"END") 
                wfile.write('\n' + "```")
            
            lineNumber += 1

