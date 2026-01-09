import cmd
# print(dir(cmd.Cmd))
class MyCommand(cmd.Cmd):
    prompt = "(ourcommand) > "

    def do_quit(self, arg):
        """This quits or exits the program"""
        return True

    # aliasing
    do_exit = do_quit

MyCommand().cmdloop()