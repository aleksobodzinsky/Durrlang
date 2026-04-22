import sys

def run_durrlang(code):
    tokens = code.split()
    memory = [0] * 30000
    ptr = 0
    pc = 0
    loop_stack = []
    output = []

    bracket_pairs = {}
    stack = []
    for i, tok in enumerate(tokens):
        if tok == 'durr.':
            stack.append(i)
        elif tok == 'durr..':
            if not stack:
                raise SyntaxError("Unmatched 'durr..'")
            start = stack.pop()
            bracket_pairs[start] = i
            bracket_pairs[i] = start

    if stack:
        raise SyntaxError("Unmatched 'durr.'")

    while pc < len(tokens):
        tok = tokens[pc]
        if tok == 'durr':
            memory[ptr] = (memory[ptr] + 1) & 0xFF
        elif tok == 'durr?':
            memory[ptr] = (memory[ptr] - 1) & 0xFF
        elif tok == 'durr!':
            output.append(chr(memory[ptr]))
        elif tok == 'durr...':
            ptr += 1
            if ptr >= len(memory):
                ptr = 0  # wrap around
        elif tok == 'DURR':
            ptr -= 1
            if ptr < 0:
                ptr = len(memory) - 1
        elif tok == 'durr.':
            if memory[ptr] == 0:
                pc = bracket_pairs[pc]
        elif tok == 'durr..':
            if memory[ptr] != 0:
                pc = bracket_pairs[pc]
        else:
            # Ignore unknown tokens (might give a warning idk)
            pass
        pc += 1

    return ''.join(output)

def main():
    if len(sys.argv) != 2:
        print("Usage: durrlang.py <filename.durr>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    try:
        result = run_durrlang(code)
        print(result, end='')
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
