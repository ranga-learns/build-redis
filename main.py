import sys


def handle_command(parts):
    """Process a Redis command and return the RESP response."""
    cmd, args = parts[0].upper(), parts[1:]

    if cmd == "PING":
        if args:
            payload = args[0].encode("utf-8")
            return f"${len(payload)}\r\n{args[0]}\r\n"

        return "+PONG\r\n"

    return "-ERR unknown command\r\n"

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        args = parse_args(line)
        response = handle_command(args)
        sys.stdout.write(response)
        sys.stdout.flush()

def parse_args(line):
    """Split a command line into arguments, handling quoted strings."""
    args = []
    current = ""
    in_quotes = False
    for ch in line:
        if ch == '"' and not in_quotes:
            in_quotes = True
        elif ch == '"' and in_quotes:
            in_quotes = False
        elif ch == ' ' and not in_quotes:
            if current:
                args.append(current)
                current = ""
        else:
            current += ch
    if current:
        args.append(current)
    return args

if __name__ == "__main__":
    main()
