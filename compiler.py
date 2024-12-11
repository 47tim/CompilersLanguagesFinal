#CPSC 323 FINAL PROJECT
#Mark Gaballa, Timothy Hyde, Dylan Zuniga
#Due Date: 12-11-2024
#Purpose: Create a compiler to parse through a file
#and output whether or not it is ready to compile


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



parsingTable = {
    "<prog>": {
        "program": "program <identifier> ; var <dec-list> begin <stat-list> end"
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
        "9": "<digit> <id-prime>", ";": "λ", ",": "λ", ":": "λ", "=": "λ", ")": "λ",
        "+": "λ", "-": "λ", "*": "λ", "/": "λ"
    },
    "<dec-list>": {
        "a": "<dec> : <type> ;", "b": "<dec> : <type>;", "c": "<dec> : <type> ;",
        "d": "<dec> : <type> ;", "l": "<dec> : <type>;", "f": "<dec> : <type> ;"
    },
    "<dec>": {
        "a": "<identifier>  <dec-prime>", "b": "<identifier> <dec-prime>",
        "c": "<identifier>  <dec-prime>", "d": "<identifier> <dec-prime>",
        "l": "<identifier>  <dec-prime>", "f": "<identifier> <dec-prime>"
    },
    "<dec-prime>": {
        ",": ", <dec>", ";": "λ", ":": "λ"
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
        "print": "<stat-list>", "end": "λ"
    },
    "<stat>": {
        "a": "<assign>", "b": "<assign>", "c": "<assign>", "d": "<assign>",
        "l": "<assign>", "f": "<assign>", "print": "<write>"
    },
    "<write>": {
        "print": "print ( <str> <identifier> ) ;"  
    },
    "<str>": {
        "“Value=”,": "“Value=”,", "a": "λ", "b": "λ", "c": "λ", "d": "λ", "l": "λ", "f": "λ"
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
        "1": "<term> <expr-prime>", "2": "<term> <expr-prime>",
        "3": "<term> <expr-prime>", "4": "<term> <expr-prime>",
        "5": "<term> <expr-prime>", "6": "<term> <expr-prime>",
        "8": "<term> <expr-prime>", "9": "<term> <expr-prime>",
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
        "1": "<factor> <term-prime>", "2": "<factor> <term-prime>",
        "3": "<factor> <term-prime>", "4": "<factor> <term-prime>",
        "5": "<factor> <term-prime>", "6": "<factor> <term-prime>",
        "8": "<factor> <term-prime>", "9": "<factor> <term-prime>",
        "(": "<factor> <term-prime>"
    },
    "<term-prime>": {
        "*": "* <factor> <term-prime>", "/": "/ <factor> <term-prime>",
        ";": "λ", ")": "λ", "+": "λ", "-": "λ"
    },
    "<factor>": {
        "a": "<identifier>", "b": "<identifier>", "c": "<identifier>",
        "d": "<identifier>", "l": "<identifier>", "f": "<identifier>",
        "(": "( <expr> )", "0": "<number>", "1": "<number>", "2": "<number>",
        "3": "<number>", "4": "<number>", "5": "<number>", "6": "<number>",
        "7": "<number>", "8": "<number>", "9": "<number>"
    },
    "<number>": {
        "0": "<digit> <number-prime>", "1": "<digit> <number-prime>",
        "2": "<digit> <number-prime>", "3": "<digit> <number-prime>",
        "4": "<digit> <number-prime>", "5": "<digit> <number-prime>",
        "6": "<digit> <number-prime>", "7": "<digit> <number-prime>",
        "8": "<digit> <number-prime>", "9": "<digit> <number-prime>"
    },
    "<number-prime>": {
        "0": "<sign> <number> <number-prime>", "1": "<sign> <number> <number-prime>",
        "2": "<sign> <number> <number-prime>", "3": "<sign> <number> <number-prime>",
        "4": "<sign> <number> <number-prime>", "5": "<sign> <number> <number-prime>",
        "6": "<sign> <number> <number-prime>", "7": "<sign> <number> <number-prime>",
        "8": "<sign> <number> <number-prime>", "9": "<sign> <number> <number-prime>",
        ";": "λ", ")": "λ", "+": "λ", "-": "λ", "*": "λ", "/": "λ"
    },
    "<sign>": {
        "+": "+", "-": "-", "0": "λ", "1": "λ",
        "2": "λ", "3": "λ", "4": "λ", "5": "λ",
        "7": "λ", "8": "λ", "9": "λ"
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
    reservedWords = ["program", "var", "begin", "end", "print"]
    stack = ["<prog>", "$"]
    


    while (stack):

        #Early exit to prevent bound error when done 
        if (stack == ["$"] and len(userIn) == 0):
            print("Ready to compile")
            quit()


        #Display
        print("{:20}{:<20}".format("USER INPUT", "STACK"))
        for a, b in zip(userIn, stack):
            print ("{:<10}{:<10}{:<10}".format(a,"||",b))

        #Check for if the top of the stack is a rule
        if (stack[0] in parsingTable):

            print("\nRule:", stack[0])

            # Decide which rule to follow
            # Deal with reserved words
            if (userIn[0] in reservedWords):
                if (userIn[0] in parsingTable[stack[0]]):
                    rule = parsingTable[stack.pop(0)][userIn[0]]
                else:
                    error(userIn[0], stack)


            # Read var. Check if key 'var' is in rule         
            elif (userIn[0][0] in parsingTable[stack[0]]):
                # THIS BREAKS APART USERIN[0] SO THAT OTHER RULES CAN USE THE INDIVIDUAL LETTERS
                rule = parsingTable[stack.pop(0)][userIn[0][0]]
                temp = userIn.pop(0)
                for x in range(len(temp)-1,-1,-1):
                    userIn.insert(0,temp[x])


            # apply individual letters/digits rule
            elif (userIn[0] in parsingTable[stack[0]]):
                rule = parsingTable[stack.pop(0)][userIn[0]]

            else:
                error(userIn[0],stack)

            #separate and push rule into stack
            for symbol in reversed(rule.split()):
                stack.insert(0, symbol)

            print("-"*30)





        # If stack and userIn top read the same, pop both and move next
        elif (stack[0] == userIn[0]):
            stack.pop(0)
            userIn.pop(0)
            print("-"*30)      

        elif(stack[0] == userIn[0][0]):
            print("-"*30)
            break

        elif(stack[0] in reservedWords and userIn[0] not in reservedWords):
            error(userIn[0],stack)

        elif(stack[0] == "λ"):
            stack.pop(0)
            print("-"*30) 



        #temp else case to prevent inf loop
        else:
            error(userIn[0],stack)
    
    print(stack)





# Managing error messages
def error(var: list[str], stackVar: list[str]):

    expected = ["program", "var", "begin", "end", "integer", "print"]
    missing = [";",",",".","(",")",":"]
    

    # Error catching cases
    if stackVar[0] in missing:
        word = ""
        match stackVar[0]:
            case ";":
                if var == ")":
                    word = "The left parentheses"
                    stackVar[0] = "("
                else:
                    word = "semicolon"
            case ",":
                word = "comma"
            case ".":
                word = "period"
            case "(":
                word = "The left parentheses"
            case ")":
                word = "The right parentheses"
            case ":":
                word = "colon"
        print(stackVar[0],word,"is missing")
        quit()
    elif (stackVar[0]) in expected:
        print(stackVar[0],"is expected")
        quit()
    else:
        match stackVar[0]:
            case "<str>":
                print("string is expected")
                quit()
            case "<number-prime>":
                print("operation is expected")
                quit()
            case "<id-prime>":
                print("; semicolon is missing")
                quit()
            case _:
                #return a list of possible words that was misspelled, pick based on if word is in key or not
                errorStr = findError(var, expected)
                for x in errorStr:
                    if x in parsingTable[stackVar[0]]:
                        print(x,"is expected")
                quit()
        quit()
    
    print("An error has occurred")
    quit()



#GIVEN A SET OF STRINGS, WHICH STRING IS THE CLOSEST TO MISSPELLED WORD
# An algorithm we can use for this is Levenshtein distance algo: https://en.wikipedia.org/wiki/Levenshtein_distance
def findError(var : str, reserved: list[str]) -> str:
    def levenshteinDistance(word1, word2):
        word1len, word2len = len(word1), len(word2)
        dp = [[0] * (word2len + 1) for _ in range(word1len + 1)]
        
        for i in range(word1len + 1):
            dp[i][0] = i
        for j in range(word2len + 1):
            dp[0][j] = j
            
        for i in range(1, word1len + 1):
            for j in range(1, word2len + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        
        return dp[word1len][word2len]
    
    closestWord = None
    minDistance = float('inf')
    
    for word in reserved:
        dist = levenshteinDistance(var, word)
        if dist < minDistance:
            minDistance = dist
            closestWord = [word]
        elif dist == minDistance:
            closestWord.append(word)
    
    return closestWord

# Parsing through final24.txt
userIn = []
with open('final24.txt', encoding="UTF-8") as f: file = f.read() #final24.txt uses UTF-8 encoding, without including this the file can not be read because open() is defaulted to CP1252 encoding
userIn = file.split()
compile(userIn)


