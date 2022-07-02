#!/usr/bin/env python3

from tkinter import Tk, ttk, StringVar, Text, END
from functools import partial

root = Tk()
stack = []
formatted_stack = StringVar()
code = StringVar(value="\n")
output = StringVar(value="\n")
n_history = 0

def format_stack(stack):
    return "\n".join(str(i) for i in stack[::-1])


def push(item):
    return stack.append(item)


def pop():
    return stack.pop()


def set_output(value, line_return="\n"):
    return output.set(f"{output.get()}{value}{line_return}")


def set_tokens(value):
    input_box.get(1.0, END)
    input_box.delete(1.0, END)
    input_box.insert(1.0, value)
    
    
def get_tokens():
    return input_box.get(1.0, END)


def parse_tokens(input_string):
    text = input_string.split()
    for index, token in enumerate(text):
        try:
            if token.isdigit(): # push number
                push(int(token))
            elif token == "+": # add
                push(pop() + pop())
            elif token == "-": # subtract
                a = pop()
                b = pop()
                push(b - a)
            elif token == "*": # multiply
                push(pop() * pop())
            elif token == "/": # divide
                a = pop()
                b = pop()
                push(b / a)
            elif token == "mod":
                a = pop()
                b = pop()
                push(b % a)
            elif token == "drop": # drop
                pop()
            elif token == "dup": # duplicate
                a = pop()
                push(a)
                push(a)
            elif token == "swap": # swap
                a = pop()
                b = pop()
                push(a)
                push(b)
            elif token == "over": # ( n1 n2 -- n1 n2 n1 )
                a = pop()
                b = pop()
                push(b)
                push(a)
                push(b)
            elif token == "rot": # ( n1 n2 n3 -- n2 n3 n1 )
                a = pop()
                b = pop()
                c = pop()
                push(b)
                push(a)
                push(c)
            elif token == "bye": # exit
                break
                
            # elif token == ":": # begin function (reserve tokens)
            # elif token == ";": # end function
            # python:
                    # def add_one(x):
                        # return x + 1
                # forth:
                    # : add_one 1 + ;
                    
            elif token == ".":
                set_output(pop(), line_return=" ")
            elif token == "emit":
                set_output(chr(pop()), line_return="")
            elif token == "cr":
                set_output("")
            # elif token == ".\"": # begin string (ends with " (not a word))
                # ." Hello, world!"
            elif token == "=":
                if pop() == pop():
                    push(-1)
                else:
                    push(0)
            elif token == ">":
                if pop() < pop():
                    push(-1)
                else:
                    push(0)
            elif token == "<":
                if pop() > pop():
                    push(-1)
                else:
                    push(0)
            elif token == "and":
                if pop() == -1 and pop() == -1:
                    push(-1)
                else:
                    push(0)
            elif token == "or":
                if pop() == -1 or pop() == -1:
                    push(-1)
                else:
                    push(0)
            elif token == "invert":
                if pop() == 0:
                    push(-1)
                else:
                    push(0)
            # elif token == "if": # only inside function, wait for 'then'
            # elif token == "else": # same deal
            
            # add words
            else:
                set_output(f"{token} ?")
                break
            if index == len(text) - 1:
                set_output(" ok")
        except IndexError:
            set_output("Stack underflow")
                   


def get_recent_items():
    if len(code.get().split("\n")) > 0:
        return code.get().split("\n")[::-1]
    else:
        return []


def select_up(event=None):
    global n_history
    if len(get_recent_items()) - 1 > n_history:
        set_tokens(get_recent_items()[n_history])
    n_history += 1
    

def select_down(event=None):
    global n_history
    if len(get_recent_items()) - 1 > n_history:
        set_tokens(get_recent_items()[n_history])
    n_history -= 1
    

def interpret(event=None):
    global n_history
    forth_code = get_tokens().strip()
    if not forth_code:
        return
    parse_tokens(forth_code)
    formatted_stack.set(format_stack(stack))
    code.set(f"{code.get()}{forth_code}\n")
    set_tokens("")
    n_history = 0


ttk.Label(root, text="Forth Code:").grid(row=0, column=0)
ttk.Label(root, textvariable=code).grid(row=1, column=0)
ttk.Label(root, text="Stack:").grid(row=0, column=2)

input_box = Text(root, height=3, width=50)
input_box.grid(row=2, column=0)
input_box.focus()

ttk.Label(root, textvariable=formatted_stack).grid(row=1, column=2)

interpret_button = ttk.Button(root, text="Interpret", command=interpret)
interpret_button.grid(row=3, column=0)

ttk.Label(root, text="Output:").grid(row=0, column=1)
ttk.Label(root, textvariable=output).grid(row=1, column=1)

root.bind("<Return>", interpret)
root.bind("<Up>", select_up)
root.bind("<Down>", select_down)
root.mainloop()
