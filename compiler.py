#CPSC 323 FINAL PROJECT


# First things first, given the grammar, it would be best to remove the left recursion
# First grammar is | <prog> -> program <identifier>; var <dec-list> begin <stat-list> end |
# we can kind of get an idea of where we are going when comparing this first line of CFG to
# what we are given in final24.txt

#                       HERE IS THE CFG GIVEN
# <prog>  program <identifier>; var <dec-list> begin <stat-list> end
# <identifier>  <letter>{<letter>|<digit>} note. This grammar is in EBNF
# <dec-list>  <dec> : <type> ;
# <dec>  <identifier>,<dec>| < identifier >
# <type>  integer
# <stat-list>  <stat> | <stat> <stat-list>
# <stat>  <write> | <assign>
# <write>  print ( <str> < identifier > );
# <str> ”value=”, | λ
# <assign>  < identifier > = <expr>;
# <expr>  <expr> + <term> | <expr> - <term> | <term>
# <term>  <term> * <factor> | <term> / <factor>| <factor>
# <factor>  < identifier > | <number> | ( <expr> )
# <number>  <sign><digit>{ <digit> } note: the grammar is in EBNF
# <sign>  + | - | λ
# <digit>  0|1|2|...|9
# <letter>  a|b|c|d|l||f


#                   LEFT RECURSION REMOVED 
# <prog> -> program <identifier>; var <dec-list> begin <stat-list> end
# <identifier> -> <letter><identifier-prime>
# <identifier-prime> -> <letter><identifier-prime>|<digit><identifier-prime> | λ
# <dec-list> -> <dec> : <type> ;
# <dec> -> <identifier><dec-prime>
# <dec-prime> -> ,<dec> | λ
# <type> -> integer
# <stat-list> -> <stat><stat-list-prime>
# <stat-list-prime> -> <stat-list> | λ
# <stat> -> <write> | <assign>
# <write> -> print ( <str> < identifier > );
# <str> -> ”value=”, | λ
# <assign> -> < identifier > = <expr>;
# <expr> -> <term><expr-prime>
# <expr-prime> -> +<term><expr-prime> | -<term><expr-prime> | λ
# <term> -> <factor><term-prime>
# <term-prime> -> *<factor><term-prime> | /<factor><term-prime> | λ
# <factor> -> < identifier > | <number> | ( <expr> )
# <number> -> <sign><digit><number-prime>                            :: Note, we have prime here due to BNF given, (<expr>) means that expr can be repeated.
# <number-prime> -> <digit><number-prime> | λ
# <sign> -> + | - | λ
# <digit> -> 0|1|2|...|9
# <letter> -> a|b|c|d|l||f


#Example of how this works:
# Start with a new stack ["<prog>",$]
# Input goes in, 
parsingTable = {
    "<prog>": {
        "program": "program <identifier>; var <dec-list> begin <stat-list> end"
    },
    "<identifier>": {
        "a": "<letter> <id-prime>", "b": "<letter> <id-prime>", "c": "<letter> <id-prime>",
        "d": "<letter> <id-prime>", "l": "<letter> <id-prime>", "f": "<letter> <id-prime>"
    },
    "<id-prime>": {
        "a": "<letter> <id-prime>", "b": "<letter> <id-prime>", "c": "<letter> <id-prime>",
        "d": "<letter> <id-prime>", "l": "<letter> <id-prime>", "f": "<letter> <id-prime>",
        "0": "<digit> <id-prime>", "1": "<digit> <id-prime>", "2": "<digit> <id-prime>",
        "3": "<digit> <id-prime>", "4": "<digit> <id-prime>", "5": "<digit> <id-prime>",
        "6": "<digit> <id-prime>", "7": "<digit> <id-prime>", "8": "<digit> <id-prime>",
        "9": "<digit> <id-prime>", ";": "λ", ",": "λ", ":": "λ", "=": "λ"
    },
    "<dec-list>": {
        "a": "<dec> : <type> ;", "b": "<dec> : <type>;", "c": "<dec> : <type> ;",
        "d": "<dec> : <type> ;", "l": "<dec> : <type>;", "f": "<dec> : <type> ;"
    },
    "<dec>": {
        "a": "<identifier> <dec-prime>", "b": "<identifier> <dec-prime>",
        "c": "<identifier> <dec-prime>", "d": "<identifier> <dec-prime>",
        "l": "<identifier> <dec-prime>", "f": "<identifier> <dec-prime>"
    },
    "<dec-prime>": {
        ",": ", <dec>", ";": "λ"
    },
    "<type>": {
        "integer": "integer"
    },
    "<stat-list>": {
        "a": "<stat> <stat-list-prime>", "b": "<stat> <stat-list-prime>",
        "c": "<stat> <stat-list-prime>", "d": "<stat> <stat-list-prime>",
        "l": "<stat> <stat-list-prime>", "f": "<stat> <stat-list-prime>",
        "print": "<stat> <stat-list-prime>"
    },
    "<stat-list-prime>": {
        "a": "<stat-list>", "b": "<stat-list>", "c": "<stat-list>",
        "d": "<stat-list>", "l": "<stat-list>", "f": "<stat-list>",
        "end": "λ"
    },
    "<stat>": {
        "a": "<assign>", "b": "<assign>", "c": "<assign>", "d": "<assign>",
        "l": "<assign>", "f": "<assign>", "print": "<write>"
    },
    "<write>": {
        "print": "print(<str><identifier>);" #REVISIT 
    },
    "<str>": {
        "value=": "value=", "a": "λ", "b": "λ", "c": "λ", "d": "λ", "l": "λ", "f": "λ"
    },
    "<assign>": {
        "a": "<identifier> = <expr> ;", "b": "<identifier> = <expr> ;",
        "c": "<identifier> = <expr> ;", "d": "<identifier> = <expr> ;",
        "l": "<identifier> = <expr> ;", "f": "<identifier> = <expr> ;"
    },
    "<expr>": {
        "a": "<term> <expr-prime>", "b": "<term> <expr-prime>",
        "c": "<term> <expr-prime>", "d": "<term> <expr-prime>",
        "l": "<term> <expr-prime>", "f": "<term> <expr-prime>",
        "(": "<term> <expr-prime>", "+": "λ", "-": "λ"
    },
    "<expr-prime>": {
        "+": "+ <term> <expr-prime>", "-": "- <term> <expr-prime>",
        ";": "λ", ")": "λ"
    },
    "<term>": {
        "a": "<factor> <term-prime>", "b": "<factor> <term-prime>",
        "c": "<factor> <term-prime>", "d": "<factor> <term-prime>",
        "l": "<factor> <term-prime>", "f": "<factor> <term-prime>",
        "(": "<factor> <term-prime>"
    },
    "<term-prime>": {
        "*": "* <factor> <term-prime>", "/": "/ <factor> <term-prime>",
        ";": "λ", ")": "λ", "+": "λ", "-": "λ"
    },
    "<factor>": {
        "a": "<identifier>", "b": "<identifier>", "c": "<identifier>",
        "d": "<identifier>", "l": "<identifier>", "f": "<identifier>",
        "(": "(<expr>)", "0": "<number>", "1": "<number>", "2": "<number>",
        "3": "<number>", "4": "<number>", "5": "<number>", "6": "<number>",
        "7": "<number>", "8": "<number>", "9": "<number>"
    },
    "<number>": {
        "0": "<sign> <digit> <number-prime>", "1": "<sign> <digit> <number-prime>",
        "2": "<sign> <digit> <number-prime>", "3": "<sign> <digit> <number-prime>",
        "4": "<sign> <digit> <number-prime>", "5": "<sign> <digit> <number-prime>",
        "6": "<sign> <digit> <number-prime>", "7": "<sign> <digit> <number-prime>",
        "8": "<sign> <digit> <number-prime>", "9": "<sign> <digit> <number-prime>"
    },
    "<number-prime>": {
        "0": "<digit> <number-prime>", "1": "<digit> <number-prime>",
        "2": "<digit> <number-prime>", "3": "<digit> <number-prime>",
        "4": "<digit> <number-prime>", "5": "<digit> <number-prime>",
        "6": "<digit> <number-prime>", "7": "<digit> <number-prime>",
        "8": "<digit> <number-prime>", "9": "<digit> <number-prime>",
        ";": "λ", ")": "λ", "+": "λ", "-": "λ"
    },
    "<sign>": {
        "+": "+", "-": "-", "0": "λ", "1": "λ"
    },
    "<digit>": {
        "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
        "5": "5", "6": "6", "7": "7", "8": "8", "9": "9"
    },
    "<letter>": {
        "a": "a", "b": "b", "c": "c", "d": "d", "l": "l", "f": "f"
    }
}
def compile(userIn: list[str]):
    stack = ["<prog>", "$"]
    
    while (stack):
        #Display
        print("{:20}{:<20}".format("USER INPUT", "STACK"))
        for a, b in zip(userIn, stack):
            print ("{:<10}{:<10}{:<10}".format(a,"||",b))

        #Check for if the top of the stack is a rule
        if (stack[0] in parsingTable):
            print("rule:", stack[0])
            rule = parsingTable[stack.pop(0)][userIn[0]]

            #separate and push rule into stack
            for symbol in reversed(rule.split()):
                stack.insert(0, symbol)

            print("-"*30)

        # If stack and userIn top read the same, pop both and move next
        elif (stack[0] == userIn[0]):
            #print("stack v:", stack)
            stack.pop(0)
            userIn.pop(0)
            print("-"*30)      

        #temp else case to prevent inf loop
        else:
            print("-"*30)
            break
    print(stack)


# Parsing through final24.txt
userIn = []
with open('final24.txt', encoding="UTF-8") as f: file = f.read() #final24.txt uses UTF-8 encoding, without including this the file can not be read because open() is defaulted to CP1252 encoding
userIn = file.split()
compile(userIn)


