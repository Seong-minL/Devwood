stop = False
variable = {}  # 변수와 그 값
calculator = ('+', '-', '*', '/')  # 연산자
while not stop:
    # 반복해서 입력을 받음
    enter = input()

    # 입력문구를 가지고 다른 기능 수행
    if enter.lower() == 'quit':  # 'quit'을 입력 시
        exit()  # 프로그램 종료
    # '='가 2개 이상 있을 시
    elif enter.count('=') > 1:
        # Error 발생 및 재입력
        print('Error: invalid input')
    # 'def'로 시작할 시
    elif ('def' in enter) and (enter.index('def') == 0):
        try:
            var = ''  # 변수의 이름
            num = ''  # 변수의 값
            eqindex = enter.index('=')  # '='의 위치

            # 변수의 이름을 구함
            for i in range(3, eqindex):
                var += enter[i]
            var = var.strip(' ')
            for l in calculator:
                if l in var:
                    raise ValueError

            # 변수의 값을 구함
            for j in range(eqindex + 1, len(enter)):
                num += enter[j]
            num = int(num)
            variable[var] = num
        # (특히 변수 값을 구할 때) 오류 발생 시
        except:
            # Error 발생 및 재입력
            print('Error: invalid input')
    # 'see'를 입력할 시
    elif enter == 'see':
        # 지금까지 저장된 변수와 그 값을 출력
        print('=====Variables=====')
        for k in variable.keys():
            print(k, ':', variable[k])
        print('===================')
    # 'calc'로 시작할 시
    elif ('calc' in enter) and (enter.index('calc') == 0):
        calcindex = 0
        calc = ''
        for m in calculator:
            if m in enter:
                calcindex = enter.index(m)
                calc = m
                break

        firstvar = ''
        secondvar = ''
        for n in range(4, calcindex):
            firstvar += enter[n]
        firstvar = firstvar.strip(' ')

        for o in range(calcindex + 1, len(enter)):
            secondvar += enter[o]
        secondvar = secondvar.strip(' ')

        try:
            if calc == '+':
                print(variable[firstvar] + variable[secondvar])
            elif calc == '-':
                print(variable[firstvar] - variable[secondvar])
            elif calc == '*':
                print(variable[firstvar] * variable[secondvar])
            elif calc == '/':
                print(variable[firstvar] / variable[secondvar])
        except ZeroDivisionError:
            print('Error: Can\'t divide by 0')
        except KeyError:
            print('Error: Undefined variable')
        except:
            print('Error: Invalid input')
    else:
        print('Undefined')
