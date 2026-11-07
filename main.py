import sys


def encode_bulk_string(s):
    if s is None:
        return "$-1\r\n"

    payload = s.encode("utf-8")
    return f"${len(payload)}\r\n{s}\r\n"


def encode_simple_string(s):
    return f"+{s}\r\n"


def cmd_ping(args):
    if len(args) == 0:
        return encode_simple_string("PONG")

    return encode_bulk_string(args[0])


def cmd_echo(args):
    if len(args) == 0:
        #TODO: Raise error, echo needs 1 argument
        return
    return encode_bulk_string(args[0])


def handle_command(parts):
    """Process a Redis command and return the RESP response."""
    cmd, args = parts[0].upper(), parts[1:]

    HANDLERS = {"PING": cmd_ping, "ECHO": cmd_echo}

    if cmd in HANDLERS:
        return HANDLERS[cmd](args)

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
        elif ch == " " and not in_quotes:
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
