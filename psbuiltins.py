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
            "begin":self.begin,
            "end":self.end,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
        if len(self.dictstack) > 0:
            return self.dictstack.pop()
        else:
            print('Error, no dictionaries on dictstack')

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        self.dictstack.append(d)

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self, name, value):
        if len(self.dictstack) == 0:
           self.dictPush({ name: value })
        else:
            self.dictstack[-1][name] = value

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self, name):
        name = '/' + name
        ds = self.dictstack[:]
        ds.reverse()
        for entry in ds:
            if name in entry:
                return entry[name]

        return None

    
    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
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

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
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

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
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

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
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

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of the StrConstant objects;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
        """
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

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
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


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
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

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop expects 1 argument")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print(OKGREEN+"**opstack**")
        for item in reversed(self.opstack):
            print(item)
        print("-----------------------"+CEND)
        print(RED+"**dictstack**")
        for item in reversed(self.dictstack):
            print(item)
        print("-----------------------"+ CEND)


    """
       Copies the top element in opstack.
    """
    def dup(self):
        if len(self.opstack) > 0:
            self.opPush(self.opstack[-1])
        else:
            print('Error - dup expects 1 argument')

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if len(self.opstack) < 1: print('Error: copy expects 1 argument')
        else:
            count = self.opPop()
            temp = []
            for i in range(count):
                temp.append(self.opstack[-1-i])
            while len(temp) != 0:
                self.opPush(temp.pop())

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        self.opstack[:] = []

    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack) < 2: print('Error: exch expects 2 arguments')

        a1 = self.opPop()
        a2 = self.opPop()
        self.opPush(a1)
        self.opPush(a2)

    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        space = 1
        if len(self.opstack) > 0 and isinstance(self.opstack[-1], int): space = int(self.opPop())

        blankStr = ''
        for i in range(space): blankStr += '\0'
        self.opPush(StrConstant(f'({blankStr})'))
    
    """Creates a new empty dictionary  pushes it on the opstack """
    def psDict(self):
        self.opPop()
        self.opPush(DictConstant({}))

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictConstant and StrConstant values.
    """
    def length(self):
        if len(self.opstack) < 1:
            print('Error: length expects 1 argument')
        else:
            item = self.opPop()
            if isinstance(item, StrConstant):
                self.opPush(len(item.value)-2) # -2 for parentheses
            elif isinstance(item, DictConstant):
                self.opPush(len(item.value))


    """ Pops either:
         -  "A (zero-based) index and an StrConstant value" from opstack OR 
         -  "A `name` (i.e., a key) and DictConstant value" from opstack.  
        If the argument is a StrConstant, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictConstant, gets the value for the given `name` from DictConstant's dictionary value and pushes it onto the opstack
    """
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
   
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StrConstant value from  opstack", OR
    - "An `item`, a `name`, and a DictConstant value from  opstack". 
    If the argument is a StrConstant, replaces the character at `index` of the StrConstant's string with the character having the ASCII value of `item`.
    If the argument is an DictConstant, adds (or updates) "name:item" in DictConstant's dictionary `value`.
    """
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
    """
    getinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a `count`, a (zero-based) `index`, and an StrConstant value from  opstack, and 
    extracts a substring of length count from the `value` of StrConstant starting from `index`,
    pushes the substring back to opstack as a StrConstant value. 
    """ 
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



    """
    putinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a StrConstant value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StrConstant's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
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

    """
    search is a string only operator, i.e., works only with StrConstant values. 
    Pops two StrConstant values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StrConstant values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
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

    # ------- Operators that manipulate the dictstact --------------
    """ begin operator
        Pops a DictConstant value from opstack and pushes it's `value` to the dictstack."""
    def begin(self):
        if (len(self.opstack) < 1):
            print('Error: begin expects a single argument')
        elif not isinstance(self.opstack[-1], DictConstant):
            print('Error: no dictionary in stack')
        else:
            self.dictPush(self.opPop().value)

    """ end operator
        Pops the top dictionary from dictstack."""
    def end(self):
        self.dictPop()
        
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
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


    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a Block and a boolean value, if the value is True, executes the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        if len(self.opstack) >= 2:
            block = self.opPop()
            bool_value = self.opPop()

            if (bool_value):
                block.apply(self)
        else:
            raise Exception('psIf expects 2 operands')

    """ ifelse operator
        Pops two Blocks and a boolean value, if the value is True, executes the bottom Block otherwise executes the top Block.
        Will be completed in part-2. 
    """
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


    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a Block, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the Block. 
       Will be completed in part-2. 
    """ 
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

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

