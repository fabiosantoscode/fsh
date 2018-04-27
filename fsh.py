import re
import sys
import os
from collections import namedtuple
import subprocess

token_re = "\\w+=|[\\$-_\\w]+|\\s+|\"(?:[^\\\\].|\\\\.)*\"|'(?:[^\\\\].|\\\\.)*'|\\{|\\}"

Statement = namedtuple('Statement', 'func args')
SetVariable = namedtuple('SetVariable', 'name value')
Function = namedtuple('Function', 'name params body')

def tokenise(s):
    return [x.group(0) for x in re.finditer(token_re, s)]

def parse_statement(tokens):
    if tokens[-1] == '\n':
        tokens.remove('\n')
        return None

    func = tokens[-1]
    tokens.remove(func)

    args = []

    while tokens and tokens[-1] != '\n':
        if not re.match(r'\s+', tokens[-1]):
            args.append(tokens[-1])
        tokens.remove(tokens[-1])

    if args and args[0] == '=':
        return SetVariable(func.replace('$', ''), args[1])

    return Statement(func, args)

def parse(s):
    tokens = list(reversed(tokenise(s)))

    out = []

    while tokens:
        statement = parse_statement(tokens)
        if statement is not None:
            out.append(statement)

    return out

def read_variable(value, variables):
    varname = value.replace('$', '')
    if value[0] == '$' and varname in variables:
        return variables[varname]
    return value

def execute(commands, variables, functions):
    for command in commands:
        if isinstance(command, Statement):
            command_list = [
                read_variable(command.func, variables),
                *[read_variable(v, variables) for v in command.args]
            ]
            if command_list[0] == 'cd':
                old_pwd = variables['PWD']
                variables['PWD'] = os.getcwd()
                if len(command_list) == 1:
                    os.chdir(os.path.expanduser('~/'))
                elif command_list[1] == '-':
                    os.chdir(old_pwd)
                else:
                    os.chdir(command_list[1])
                continue
            subprocess.run(command_list)
        elif isinstance(command, SetVariable):
            variables[command.name] = command.value

def main():
    try:
        inp = open(sys.argv[1])
    except IndexError:
        inp = sys.stdin

    variables = {}
    functions = {}

    variables['PWD'] = os.getcwd()

    for line in inp:
        execute(parse(line), variables, functions)


if __name__ == '__main__':
    main()
