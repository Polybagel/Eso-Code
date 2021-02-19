def evaluate(code):
    code = cleanup(list(code))
    bracemap = buildbracemap(code)

    output = ""

    cells = [0]*30000
    codeptr = 0
    cellptr = 0

    while codeptr < len(code):
        command = code[codeptr]

        if command == ">":
            cellptr += 1
        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1
        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        if command == "[" and cells[cellptr] == 0:
            codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0:
            codeptr = bracemap[codeptr]
        if command == ".":
            output += chr(cells[cellptr])
        if command == ",":
            pass ### input not supported yet!!

        codeptr += 1

    return output


def cleanup(code):
    return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))


def buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[": temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start

    return bracemap
