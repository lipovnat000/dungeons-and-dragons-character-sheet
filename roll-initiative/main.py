from characterCreator import CharacterCreator

def parse_command(text):
    text = text.strip().lower()
    if " " in text:
        cmd, args = text.split(" ", 1)
    else:
        cmd, args = text, ""
    return cmd, args

if __name__ == "__main__":

    character = CharacterCreator().create()

    print("D&D Helper — type 'help' for commands.")

    while True:
        user_input = input("\n> ").strip()
        cmd, args = parse_command(user_input)

        if cmd in ("quit", "exit"):
            print("Goodbye.")
            break

        elif cmd == "help":
            print("Commands:")
            print("  roll <skill/ability/save>")
            print("  roll <check> with advantage")
            print("  roll <check> with disadvantage")
            print("  show stats")
            print("  help")
            print("  quit")

        elif cmd == "show":
            if args == "stats":
                character.summary()
            else:
                print("Unknown show command.")

        elif cmd == "roll":
            if args:
                if " with advantage" in args:
                    check = args.replace(" with advantage", "")
                    character.roll_check(check, advantage=True)
                elif " with disadvantage" in args:
                    check = args.replace(" with disadvantage", "")
                    character.roll_check(check, disadvantage=True)
                else:
                    character.roll_check(args)
            else:
                print("Usage: roll <skill/ability/save> [with advantage|with disadvantage]")

        else:
            print("Unknown command. Type 'help' for options.")
