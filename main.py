import sys


def encode_bulk_string(s):
    if s is None:
        return encode_null_bulk_string()

    payload = s.encode("utf-8")
    return f"${len(payload)}\r\n{s}\r\n"


def encode_simple_string(s):
    return f"+{s}\r\n"


def encode_integer(n):
    return f":{n}\r\n"


def encode_null_bulk_string():
    return "-1\r\n"


def encode_error(s):
    return f"-{s}\r\n"


def cmd_ping(args):
    if len(args) == 0:
        return encode_simple_string("PONG")

    return encode_bulk_string(args[0])


def cmd_echo(args):
    if len(args) == 0:
        return encode_error("ERR wrong number of arguments for 'ECHO' command")
    return encode_bulk_string(args[0])


def cmd_docs(args):
    return encode_simple_string("OK")


def handle_command(parts):
    """Process a Redis command and return the RESP response."""
    cmd, args = parts[0].upper(), parts[1:]

    HANDLERS = {"PING": cmd_ping, "ECHO": cmd_echo, "COMMAND": cmd_docs}

    handler = HANDLERS.get(cmd)
    if handler:
        return handler(args)

    return encode_error(f"ERR unknown command '{cmd}'")


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
