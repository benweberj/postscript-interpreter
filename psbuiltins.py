from colors import *
from elements import StrConstant, DictConstant, CodeArray

class Stacks:
    def __init__(self):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }

    
    # Pops the top value from opstack and returns it.
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")


    # Pushes $value to the opstack.
    def opPush(self,value):
        self.opstack.append(value)


    # Pops the top dictionary from dictstack and returns it.
    def dictPop(self):
        if len(self.dictstack) > 0:
            return self.dictstack.pop()
        else:
            print('Error, no dictionaries on dictstack')


    # Pushes the given dictionary onto the dictstack. 
    def dictPush(self,d):
        self.dictstack.append(d)


    # Adds $name:$value pair to the top dictionary in the dictstack.
    def define(self, name, value):
        if len(self.dictstack) == 0:
           self.dictPush({ name: value })
        else:
            self.dictstack[-1][name] = value


    # Searches the dictstack for a variable or function and returns its value.
    def lookup(self, name):
        name = '/' + name
        ds = self.dictstack[:]
        ds.reverse()
        for entry in ds:
            if name in entry:
                return entry[name]
        return None


    # if $op1 and $op2 are numbers, add them and push the sum to the opstack.
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")


    # if $op1 and $op2 are numbers, subtract them and push the result to the opstack.
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 - op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: sub expects 2 operands")


    # if $op1 and $op2 are numbers, multiply them and push the product to the opstack.
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1*op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: sub expects 2 operands")


    # if $op1 and $op2 are numbers, mod $op1 by $op2 and push the remainder to the stack.
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 % op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: sub expects 2 operands")


    # if $op1 and $op2 are equal, push True to the opstack. Otherwise push False.
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()

            if type(op1) is not type(op2):
                self.opPush(False)
            elif isinstance(op1, StrConstant):
                self.opPush(op1.value == op2.value)
            elif isinstance(op1, DictConstant):
                self.opPush(op1 is op2)
                # self.opPush(op1.value is op2.value)
            else:
                self.opPush(op1 == op2)
        else:
            print('Error: eq expects 2 argumnents')

    # if $op2 < $op1, push True to the opstack. Otherwise push False.
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (type(op1) is not type(op2)):
                self.opPush(False)
            elif isinstance(op1, StrConstant):
                self.opPush(op2.value < op1.value)
            elif isinstance(op1, DictConstant):
                pass
            else:
                self.opPush(op2 < op1)
        else:
            print('Error: lt expects 2 arguments')


    # if $op2 > $op1, push True to the opstack. Otherwise push False.
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (type(op1) is not type(op2)):
                self.opPush(False)
            elif isinstance(op1, StrConstant):
                self.opPush(op2.value > op1.value)
            elif isinstance(op1, DictConstant):
                pass
            else:
                self.opPush(op2 > op1)
        else:
            print('Error: lt expects 2 arguments')


    # Removes the top value from the opstack
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop expects 1 argument")


    # Prints the opstack and dictstack. The end of the list is the top of the stack.
    def stack(self):
        print(OKGREEN+"**opstack**")
        for item in reversed(self.opstack):
            print(item)
        print("-----------------------"+CEND)
        print(RED+"**dictstack**")
        for item in reversed(self.dictstack):
            print(item)
        print("-----------------------"+ CEND)


    # Copies the top element in opstack and pushes it to the opstack.
    def dup(self):
        if len(self.opstack) > 0:
            self.opPush(self.opstack[-1])
        else:
            print('Error - dup expects 1 argument')


    # Copies $count number of items in the opstack and pushes them to the top
    def copy(self):
        if len(self.opstack) < 1: print('Error: copy expects 1 argument')
        else:
            count = self.opPop()
            temp = []
            for i in range(count):
                temp.append(self.opstack[-1-i])
            while len(temp) != 0:
                self.opPush(temp.pop())


    # Counts the number of elements in the opstack and pushes the count to the opstack.
    def count(self):
        self.opPush(len(self.opstack))

    # Clears the opstack.
    def clear(self):
        self.opstack[:] = []

    # swaps the top two elements in opstack
    def exch(self):
        if len(self.opstack) < 2: print('Error: exch expects 2 arguments')

        a1 = self.opPop()
        a2 = self.opPop()
        self.opPush(a1)
        self.opPush(a2)


    # pushes empty string (characters initialized to \0) to the opstack
    def string(self):
        space = 1
        if len(self.opstack) > 0 and isinstance(self.opstack[-1], int): space = int(self.opPop())

        blankStr = ''
        for i in range(space): blankStr += '\0'
        self.opPush(StrConstant(f'({blankStr})'))
    
    # pushes an empty dictionary to the opstack
    def psDict(self):
        self.opPop()
        self.opPush(DictConstant({}))


    # pushes the length of $item (string or dictionary) to the opstack
    def length(self):
        if len(self.opstack) < 1:
            print('Error: length expects 1 argument')
        else:
            item = self.opPop()
            if isinstance(item, StrConstant):
                self.opPush(len(item.value)-2) # -2 for parentheses
            elif isinstance(item, DictConstant):
                self.opPush(len(item.value))


    # if $item is a string:
    #   - pushes the ascii value of the character at index $key in string $item to the opstack
    # if $item is a dictionary:
    #   - pushes the value of the key $key to the opstack
    def get(self):
        if len(self.opstack) < 2:
            print('Error: get expects 2 arguments')
        else:
            key = self.opPop() # index or name
            item = self.opPop() # string or dict

            if isinstance(item, StrConstant) and isinstance(key, int): # string get
                self.opPush(ord(item.value[key+1])) # +1 for first parenthese
            elif isinstance(item, DictConstant): # dict get
                self.opPush(item.value[key])
            else:
                print('Error: not sure what you\'re trying to get.')


    # if $item is a string:
    #   - replaces the character at index $key with ASCII $token in the string $item
    # if $item is s dictionary:
    #   - adds or updates the key $key in dictionary $item to be $token
    def put(self):
        if len(self.opstack) < 3:
            print('Error: put requires 3 arguments')
        else:
            token = self.opPop()
            key = self.opPop() 
            item = self.opPop()

            if isinstance(item, StrConstant) and isinstance(key, int):
                st = item.value[1:-1] # raw string
                item.value = f'({st[:key] + chr(token) + st[key+1:]})'
            elif isinstance(item, DictConstant):
                item.value[key] = token
            else:
                # print(f'key: {key}, item: {item}, token: {token}')
                print('Error: not sure what you\'re trying to put into what.')
    

    # pushes to substring of $item from indices $ind to ($ind + $count) to the opstack
    def getinterval(self):
        if len(self.opstack) < 3:
            print('Error: getinterval expects 3 arguments')
        else:
            length = self.opPop()
            ind = self.opPop()
            item = self.opPop()
            
            snip = ''
            for i in range(ind+1, ind+length+1): # +1 because parentheses
                snip += item.value[i]
            self.opPush(StrConstant(f'({snip})'))


    # replaces the contents $item at the indices $index to ($index + len($substr)) with $substr
    def putinterval(self):
        if len(self.opstack) < 3:
            print('Error: putinterval expects 3 parameters')
        else:
            substr = self.opPop()
            ind = self.opPop()
            item = self.opPop()
            
            i = item.value[1:-1]
            s = substr.value[1:-1]

            item.value = f'({i[:ind] + s + i[ind+len(s):]})'


    # if $delim is a substring of $st:
    #   - split $st at first occurence of $delim and push both ends to the opstack
    #   - push True to the opstack
    # otherwise: push the originial string $st and False to the opstack
    def search(self):
        if len(self.opstack) < 2:
            print('Error: search expects 2 parameters')
        else:
            delim = self.opPop()
            st = self.opPop()
            
            if delim.value[1:-1] in st.value[1:-1]:
                spl = st.value[1:-1].split(delim.value[1:-1], 1)
                self.opPush(StrConstant(f'({spl[1]})'))
                self.opPush(StrConstant(delim.value))
                self.opPush(StrConstant(f'({spl[0]})'))
                self.opPush(True)
            else:
                self.opPush(st)
                self.opPush(False)
    

    # Defines $name to be $value in the current referencing environment (top of ditcstack)
    def psDef(self):
        if len(self.opstack) >= 2:
            value = self.opPop()
            name = self.opPop()
            if name[0] == '/':
                self.define(name, value)
            else:
                self.opPush(name)
                self.opPush(value)
                print('Error: invalid name')
        else:
            print('Error: def expected 2 arguments')


    # if operator: if $bool_value is true, executes $block, otherwise nothing is done
    def psIf(self):
        if len(self.opstack) >= 2:
            block = self.opPop()
            bool_value = self.opPop()

            if (bool_value):
                block.apply(self)
        else:
            raise Exception('psIf expects 2 operands')


    # ifelse operator: if $bool_value is true, executes $if_block, otherwise it executes $else_blkock
    def psIfelse(self):
        if len(self.opstack) >= 3:
            else_block = self.opPop()
            if_block = self.opPop()
            bool_value = self.opPop()

            if (bool_value):
                if_block.apply(self)
            else:
                else_block.apply(self)
        else:
            raise Exception('psIfElse expects 3 operands')


    # for loop operator: executes $block for indices $begin through $end, incrementing by $step.
    # Pushes current index $i to the opstack before each execution of $block
    def psFor(self):
        if len(self.opstack) >= 4:
            block = self.opPop()
            end = self.opPop()
            step = abs(self.opPop())
            begin = self.opPop()

            i = begin
            if begin <= end: # ascending
                while (i <= end):
                    self.opPush(i)
                    block.apply(self)
                    i += step
            else: # descending
                while (i >= end):
                    self.opPush(i)
                    block.apply(self)
                    i -= step
        else:
            raise Exception('psFor expects 4 operands')


    # Clears both stacks.
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []


    # Removes None value from top of opstack, if present
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

