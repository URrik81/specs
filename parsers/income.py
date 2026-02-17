import sys

def parseIncome(fullLine, origName, file, origIncome, isDl = 0):
    print(f"parse {origName} in line {fullLine}")
    fullLine = fullLine[2:]
    lines = fullLine.split(",")
    for line in lines:
      if len(line) < 3:
        continue
      numbers = line.split(' ')
      x = int(numbers[0])
      y = int(numbers[1])
      flags = 0
      landIncome = 0
      name = origName
      income = origIncome
      if (len(numbers) > 2):
        flags = int(numbers[2])
      if isDl == 1:
        with open("ANT.DAT", 'r', encoding='cp1251') as rfile:
            print(f"Finding land by {x:02d}-{y:02d}")
            lineCount = 1
            landIncomeLine = 0
            landSymbol = "xxx"
            for line in rfile:
                if lineCount == y+4:
                    landSymbol = line[x-1]
                    print(f"landSymbol is {landSymbol} lineCount: {lineCount}")
                if line[0] == landSymbol:
                    landIncomeLine = lineCount + 2
                    print(f"landIncomeLine is {landIncomeLine} lineCount: {lineCount}")
                if landIncomeLine == lineCount:
                    landIncome = int(line)
                    print(f"landIncome is {landIncome} lineCount: {lineCount}")
                    break
                lineCount += 1
      income += landIncome
      if flags >= 128:
          if isDl != 1:
              name += " (ЛВ)"
              income = 0
          else:
            name += " (Ст)"
            income += 5
      name = name + (" " * (18 - len(name)))
      fileLine = f" {name} | {x:02d}-{y:02d} |     {income:03d}    |\n"
      print(fileLine)
      file.write(fileLine)
    return income

with open(sys.argv[1], 'r', encoding='cp1251') as rfile:
    with open('income.txt', 'w', encoding='cp1251') as wfile:
        lineNumber = 1
        year = 0
        readPlayerLine = 0
        totalIncome = 0
        totalCost = 0
        for line in rfile:
            if lineNumber == 2:
                year = line
            if readPlayerLine == 1:
                wfile.write(f"Год {year}")
                wfile.writelines(line)
                wfile.write(f"--------------------|-------|------------|\n")
                wfile.write(f"      Юнит          |  X-Y  | Содержание |\n")
                wfile.write(f"--------------------|-------|------------|\n")
            elif line.startswith('г '):
                totalCost += parseIncome(line, 'Гном', wfile, -5)
            elif line.startswith('в '):
                totalCost += parseIncome(line, 'Варвар', wfile, -5)
            elif line.startswith('э '):
                totalCost += parseIncome(line, 'Ильв', wfile, -5)
            elif line.startswith('о '):
                totalCost += parseIncome(line, 'Эвогр', wfile, -5)
            elif line.startswith('п '):
                totalCost += parseIncome(line, 'Л. Пехота', wfile, -3)
            elif line.startswith('р '):
                totalCost += parseIncome(line, 'Рыцарь', wfile, -10)
            elif line.startswith('м '):
                totalCost += parseIncome(line, 'Маг', wfile, -10)
            elif line.startswith('з '):
                totalCost += parseIncome(line, 'Зомби', wfile, 0)
            elif line.startswith('д '):
                totalCost += parseIncome(line, 'Дракон', wfile, 0)
            elif line.startswith('ф '):
                totalCost += parseIncome(line, 'Корабль', wfile, -5)
            elif line.startswith('К '):
                totalIncome += parseIncome(line, 'Крепость', wfile, 0)
            elif line.startswith('Г '):
                totalIncome += parseIncome(line, 'Город', wfile, 0, 1)
            elif line.startswith('З '):
                totalIncome += parseIncome(line, 'Замок', wfile, 0, 1)
            elif line.startswith('П '):
                totalIncome += parseIncome(line, 'Поместье', wfile, 0, 1)
            elif line.startswith('Б '):
                totalIncome += parseIncome(line, 'Башня', wfile, 0, 1)
            elif line.startswith('C '):
                totalIncome += parseIncome(line, 'Медный р-к', wfile, 2)
            elif line.startswith('S '):
                totalIncome += parseIncome(line, 'Серебряный р-к', wfile, 4)
            elif line.startswith('G '):
                totalIncome += parseIncome(line, 'Золотой р-к', wfile, 6)
            elif line.startswith('M '):
                totalIncome += parseIncome(line, 'Мифриловый р-к', wfile, 8)
            if 'Player' in line:
                print(f"Player found") 
                if readPlayerLine == 0:
                    wfile.write("```" + '\n')
                else:
                    total = totalIncome + totalCost
                    wfile.write(f"--------------------|-------|------------|\n")
                    wfile.write(f"  Доход: {totalIncome:02d} / Расход: {-totalCost:02d} / Всего: {total:03d}    |\n")
                    wfile.write(f"--------------------|-------|------------|\n")
                    wfile.write("```" + '\n-----\n' + "```" + '\n')
                    totalIncome = 0
                    totalCost = 0
                readPlayerLine = 1
            elif readPlayerLine > 0:
                readPlayerLine += 1
            else: 
                readPlayerLine = 0

            if 'END' in line:
                print(f"END") 
                wfile.write('\n' + "```")
            lineNumber += 1