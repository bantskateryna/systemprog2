import argparse
import os

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"

def uniq(filepath, count=False, duplicates=False, unique_only=False, verbose=False, color=False, from_stdin=False, stdin_lines=None):
    if from_stdin:
        lines = [ln.rstrip('\n') for ln in stdin_lines]
    else:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = [line.rstrip('\n') for line in f]
    order = {}
    for line in lines:
        order[line] = order.get(line, 0) + 1
    output = []
    for line, freq in order.items():
        show = True
        if duplicates and freq < 2:
            show = False
        if unique_only and freq > 1:
            show = False
        if show:
            if count:
                prefix = f"{YELLOW}{freq:>4}{RESET} " if color else f"{freq:>4} "
                output.append(f"{prefix}{line}")
            else:
                output.append(line)
    if verbose:
        header_name = filepath if filepath is not None else "stdin"
        header = f"{BOLD}{CYAN}==> {header_name} <=={RESET}" if color else f"\033[1m==> {header_name} <==\033[0m"
        print(header)
    print('\n'.join(output))

def read_all_stdin_text():
    chunks = []
    chunk_size = 65536
    while True:
        try:
            data = os.read(0, chunk_size)
        except OSError:
            break
        if not data:
            break
        chunks.append(data)
    if not chunks:
        return []
    try:
        text = b"".join(chunks).decode('utf-8')
    except Exception:
        text = b"".join(chunks).decode('utf-8', errors='replace')
    return text.splitlines()

def main():
    parser = argparse.ArgumentParser(description="Python version of Unix uniq", add_help=False)
    parser.add_argument('-h', '--help', action='help', help='show this help message and exit')
    parser.add_argument("filepath", nargs='?', help="Path to the file")
    parser.add_argument("-c", action="store_true", help="Prefix lines by the number of occurrences")
    parser.add_argument("-d", action="store_true", help="Only print duplicate lines")
    parser.add_argument("-u", action="store_true", help="Only print unique lines")
    parser.add_argument("-v", action="store_true", help="Verbose: show filename header")
    parser.add_argument("--color", action="store_true", help="Enable colored output")
    args = parser.parse_args()

    if args.filepath is None:
        if not os.isatty(0):
            stdin_lines = read_all_stdin_text()
            uniq(None, args.c, args.d, args.u, args.v, args.color, from_stdin=True, stdin_lines=stdin_lines)
            return
        parser.print_usage()
        return

    if not os.path.isfile(args.filepath):
        print(f"Error: File '{args.filepath}' not found.")
        return

    uniq(args.filepath, args.c, args.d, args.u, args.v, args.color)

if __name__ == "__main__":
    main()
