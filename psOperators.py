# Name: Joshua Frey

from psItems import Value, ArrayValue, FunctionValue
class Operators:
    def __init__(self, scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        self.scope = scoperule # the scope type
        
        #The builtin operators supported by our interpreter
        self.builtin_operators = {
             # TO-DO in part1
             # include the key value pairs where he keys are the PostScrip opertor names and the values are the function values that implement that operator. 
             # Make sure **not to call the functions** 
             "add":self.add,
             "sub":self.sub,
             "mul":self.mul,
             "mod":self.mod,
             "eq":self.eq,
             "lt":self.lt,
             "gt":self.gt,
             "array":self.array,
             "length":self.length,
             "getinterval":self.getinterval,
             "putinterval":self.putinterval,
             "aload":self.aload,
             "astore":self.astore,
             "pop":self.pop,
             "stack":self.stack,
             "dup":self.dup,
             "copy":self.copy,
             "count":self.count,
             "clear":self.clear,
             "exch":self.exch,
             "roll":self.roll,
             "def":self.psDef,
             "if":self.psIf,
             "ifelse":self.psIfelse,
             "for":self.psFor,
             "repeat": self.repeat,
             "forall": self.forall
        }
    #-------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        return self.opstack.pop()

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)
        
    #------- Dict Stack Operators --------------
    
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """   
    def dictPop(self):
        return self.dictstack.pop()

    """
       Helper function. Pushes the given staticLink and dictionary as a tuple onto the dictstack. 
    """   
    def dictPush(self,staticLink,d):
        self.dictstack.append((staticLink, d)) # addsa a tuple of the staticLinkIndex and dictionary to top of the dictstack

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """   
    def define(self,name,value):
        # Checks to see if dictstack is empty
        if len(self.dictstack) == 0:
            self.dictPush(0, {}) # adds tuple with a staticLinkIndex of 0 and a empty dictionary to an empty dictstack
        staticLinkIndex = self.dictstack[-1][0] # gets the staticLinkIndex at the top of the dictstack
        dictionary = self.dictstack[-1][1] # gets the dictionary at the top of the stack
        dictionary[name] = value # adds new name and value pair to the top dictionary in the dictstack
        self.dictstack[-1] = (staticLinkIndex, dictionary) # adds the new tuple/AR to the top of the dictstack
        
    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        if self.scope == "static":
            name = '/' + name
            return self.staticLookupHelper(name,len(self.dictstack)-1)
        elif self.scope == "dynamic":
            # Uses built-in function reversed to return a new reversed list so you can start from the top of the dictstack/end of list
            for (staticLinkIndex, dictionary) in reversed(self.dictstack):
                # Traverses the current dictionary in the dictstack
                for (variableName, variableValue) in dictionary.items():
                    # if the variable is in the dictionary return the value, make sure to add / to the beginning for variable lookup
                    if variableName == '/' + name:
                        return variableValue
            print("Variable doesn't exist in the dictionary stack")             
            return None # returns None if name is not found in any of the dictionaries in the dictstack    
    
    # Helper function that implements the LookUp using static scoping
    def staticLookupHelper(self,name,index):
        # if name is in the current dictionary then return its value
        if name in self.dictstack[index][1]:
            return self.dictstack[index][1][name]
        else:
            # if index is 0 then return none
            if index == 0:
                print("Variable doesn't exist in the dictionary stack") 
                return None
            else:
                # recursively calls next tuple in the dictstack using the staticLinkIndex of the current tuple
                return self.staticLookupHelper(name,self.dictstack[index][0])
    
    # Helper function that gets the staticLinkIndex from a function name
    def calculateStaticLinkHelper(self,name,index):
        # same as staticLookupHelper except it returns the staticLinkIndex
        if '/' + name in self.dictstack[index][1]:
            return self.dictstack[index][0] 
        elif index == 0:
            # print("Helper doesn't exist in the dictionary stack")
            return 0
        else:
            return self.calculateStaticLinkHelper(name,self.dictstack[index][0])
    
    #------- Arithmetic Operators --------------
    
    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """   
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: add expects 2 operands")
 
    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """   
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """    
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """ 
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: mod expects 2 operands")
            
    #---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """ 
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            # checks to see if we are comparing the same type
            if type(op1) == type(op2):
                self.opPush(op1 == op2) # returns true or false based on the comparison
            else:
                print("Error: eq - the two operands is not the same type")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: eq expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """ 
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if type(op1) == type(op2): # checks to see if we are comparing the same type
                self.opPush(op1 > op2) # returns true or false based on the comparison
            else:
                print("Error: lt - the two operands is not the same type")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: lt expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is greater than the top value, otherwise pushes "False"
    """ 
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if type(op1) == type(op2): # checks to see if we are comparing the same type
                self.opPush(op1 < op2) # returns true or false based on the comparison
            else:
                print("Error: gt - the two operands is not the same type")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: gt expects 2 operands")

    # ------- Array Operators --------------
    """ 
       Pops the array length (an int value) from the opstack and initializes an array constant (ArrayValue) having the given length. 
       Initializes the elements in the value of the ArrayValue to None. Pushes the ArrayValue to the opstack.
    """
    def array(self):
        if len(self.opstack) > 0:
            op1 = self.opPop() # pops array length 
            if isinstance(op1, int): # checks to see if array length from opstack is an int value
                newArray = [] # initializes an empty array
                # op1 is the length of the new array so for every index of the new array initialize its value as None
                for i in range(0, op1): 
                    newArray.append(None)
                newArrayValue = ArrayValue(newArray) # initializes a new array constant
                self.opPush(newArrayValue) # Pushes the arrayvalue to the opstack
            else:
                print("Error: array - the operand is not a int")
                self.opPush(op1)  # bottom value
        else:
            print("Error: array expects 1 operand")
                
    """ 
       Pops an array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support ArrayValue values.
    """
    def length(self):
        if len(self.opstack) > 0:
            op1 = self.opPop() # pops array
            if isinstance(op1, ArrayValue): # checks to see if the operand is an ArrayValue object
                array = op1.value # gets the array from ArrayValue  
                arrayLength = len(array) # gets the length of the array using count method
                self.opPush(arrayLength) # Pushes the length of the array onto the opstack
            else:
                print("Error: length - the operand is not a ArrayValue")
                self.opPush(op1)  # bottom value
        else:
            print("Error: length expects 1 operand")

    """ 
        Pops the `count` (int), an (zero-based) start `index`, and an array constant (ArrayValue) from the operand stack.  
        Pushes the slice of the array of length `count` starting at `index` onto the opstack.(i.e., from `index` to `index`+`count`) 
        If the end index of the slice goes beyond the array length, will give an error. 
    """
    def getinterval(self):
        if len(self.opstack) > 2:
            op1 = self.opPop() # pops count
            op2 = self.opPop() # pops array index
            op3 = self.opPop() # pops array
            if isinstance(op1, int) and isinstance(op2, int) and isinstance(op3, ArrayValue): # checks to see if operand 1 and 2 are int and operand 3 is a ArrayValue
                array = op3.value # gets the array from ArrayValue 
                if (op2+op1) > len(array):
                    print("Error: getinterval - end index of the slice goes beyond the array length")
                    self.opPush(op3)  # bottom value
                    self.opPush(op2)  # middle value
                    self.opPush(op1)  # top value
                else:
                    slicedArray = array[op2:(op2+op1)] # gets the slice of the arryay of length count starting at index 
                    op3.value = slicedArray # now sets the new ArrayValue for op3/array
                    self.opPush(op3) # Pushes the updated arrayvalue onto the opstack
            else:
                print("Error: getinterval - operand 1 and 2 expects an int and operand 3 expects an ArrayValue")
                self.opPush(op3)  # bottom value
                self.opPush(op2)  # middle value
                self.opPush(op1)  # top value
        else:
            print("Error: getinterval expects 3 operands")

    """ 
        Pops an array constant (ArrayValue), start `index` (int), and another array constant (ArrayValue) from the operand stack.  
        Replaces the slice in the bottom ArrayValue starting at `index` with the top ArrayValue (the one we popped first). 
        The result is not pushed onto the stack.
        The index is 0-based. If the end index of the slice goes beyond the array length, will give an error. 
    """
    def putinterval(self):
        if len(self.opstack) > 2:
            op1 = self.opPop() # pops array2
            op2 = self.opPop() # pops array index
            op3 = self.opPop() # pops array1
            if isinstance(op1, ArrayValue) and isinstance(op2, int) and isinstance(op3, ArrayValue): # checks to see if operand 1 and 3 are ArrayValues and operand 3 is an int
                array1 = op3.value # gets array1
                array2 = op1.value # gets array2
                if (op2+len(array2)) > len(array1): # checks to see if the end index of the slice goes beyond the array length
                    print("Error: putinterval - the end index of the slice goes beyond the array length")
                    self.opPush(op3)  # bottom value
                    self.opPush(op2)  # middle value
                    self.opPush(op1)  # top value
                else:
                    array1[op2:(op2+len(array2))] = array2 # replaces section of array1 with array2 starting at index
            else:
                print("Error: putinterval - operand 1 and 3 expects an ArrayValue and operand 2 expects an int")
                self.opPush(op3)  # bottom value
                self.opPush(op2)  # middle value
                self.opPush(op1)  # top value
        else:
            print("Error: putinterval expects 3 operands")
            
    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pushes all values in the array constant to the opstack in order (the first value in the array should be pushed first). 
        Pushes the orginal array value back on to the stack. 
    """
    def aload(self):
        if len(self.opstack) > 0:
            op1 = self.opPop() # pops array
            if isinstance(op1, ArrayValue): # checks to see if operand 1 is an ArrayValue
                array = op1.value # gets array2
                # pushes each value in the array onto the opstack
                for item in array:
                    self.opPush(item)
                self.opPush(op1) # pushes the original array value back on to the stack
            else:
                print("Error: aload - operand expects an ArrayValue")
                self.opPush(op1)  # top value
        else:
            print("Error: aload expects 1 operand")
        
    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pops as many elements as the length of the array from the operand stack and stores them in the array constant. 
        The value which was on the top of the opstack will be the last element in the array. 
        Pushes the array value back onto the operand stack. 
    """
    def astore(self):
        if len(self.opstack) > 0:
            op1 = self.opPop() # pops array
            if isinstance(op1, ArrayValue): # checks to see if operand 1 is an ArrayValue
                array = op1.value # gets array
                # pushes each value in the array onto the opstack, traverses each index of the array backwards
                for i in range((len(array)-1), -1, -1):
                    newOp = self.opPop()
                    array[i] = newOp
                op1.value = array # sets the ArrayValue to be the new array
                self.opPush(op1) # pushes the new array value back on to the stack
            else:
                print("Error: astore - operand expects an ArrayValue")
                self.opPush(op1)  # top value
        else:
            print("Error: astore expects 1 operand")

    #------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        self.opPop()

    """
       Prints the opstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        # traverses through the opstack list in reversed order and prints each item in the opstack
        print("===**opstack**===")
        for item in reversed(self.opstack):
            print(item)
        print("===**dictstack**===")
        dictStackIndex = len(self.dictstack)-1 # gets the index of the top of the dictStack
        for (staticLinkIndex, dictionary) in reversed(self.dictstack):
            print("----" + str(dictStackIndex) + "----" + str(staticLinkIndex) + "----")
            dictStackIndex -= 1
            for (variableName, variableValue) in dictionary.items():
                print(variableName + "\t" + str(variableValue))
        print("=================") 

    """
       Copies the top element in opstack.
    """
    def dup(self):
        top = self.opstack[-1] # copies the top element in the opstack/last element in the opstack
        self.opPush(top) # pushes the top element on to the stack

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if len(self.opstack) > 0:
            op1 = self.opPop() # pops count 
            if isinstance(op1, int): # checks to see if operand is an int
                temp = [] # creates a temporary array to store copied values
                # traverses the opstack backwards up until the count
                for i in range(-1, (-op1 - 1), -1):
                    temp.insert(0, self.opstack[i]) # inserts the copied values from the stack at the start of the array so when pushed its in the right order
                # pushes the copied values on to the opstack
                for item in temp:
                    self.opPush(item)
            else:
                print("Error: copy - operand expects an int")
                self.opPush(op1)  # top value
        else:
            print("Error: copy expects 1 operand")

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack)) # pushes the length of the opstack which is the number of elements in the opstack 

    """
       Clears the opstack.
    """
    def clear(self):
        if len(self.opstack) > 0:
            self.opstack[:] = []
        else:
            print("Error: clear expects at least 1 operand on the operand stack")
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # pops top element
            op2 = self.opPop() # pops second top element
            self.opPush(op1) # pushes top element first
            self.opPush(op2) # pushes second top element second so now its on top
        else:
            print("Error: exch expects 2 operands")

    """
        Implements roll operator.
        Pops two integer values (m, n) from opstack; 
        Rolls the top m values in opstack n times (if n is positive roll clockwise, otherwise roll counter-clockwise)
    """
    def roll(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # pops number of values getting moved
            op2 = self.opPop() # pops stack position from top
            if isinstance(op1, int) and isinstance(op2, int): # checks to see if operand 1 and 2 is an int
                # checks to see if its positive or negative
                if op1 > 0: 
                    # Rolls n times
                   for i in range(op1):
                        temp = self.opPop() # pops and stores the top element in the opstack in a temporary variable
                        self.opstack.insert(-op2+1, temp) # inserts at the bottom of opstack
                elif op1 < 0:
                    for i in range(-op1):
                        temp = self.opstack.pop(-op2) # pops at the mth value from the top of the stack
                        self.opPush(temp) # insert at the top of the stack
            else:
                print("Error: roll - operand 1 and 2 expects an int")
                self.opPush(op2)  # top value
                self.opPush(op1)
        else:
            print("Error: roll expects 2 operands")
            
    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.  
    """
    def psDef(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # pops variable value
            op2 = self.opPop() # pops variable name
            # checks to see if op2 is a string value
            if isinstance(op2, str):
                # checks to see if the variable name starts with '/'
                if op2[0] == '/':
                    self.define(op2, op1)
                else:
                    print("Error: def - operand 2 needs to start with /")
                    self.opPush(op2)
                    self.opPush(op1)
            else:
                print("Error: def - operand 2 expects a str")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: def expects 2 operands")


    # ------- if/ifelse Operators --------------
    """
       Implements if operator. 
       Pops the `ifbody` and the `condition` from opstack. 
       If the condition is True, evaluates the `ifbody`.  
    """
    def psIf(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # pops ifbody
            op2 = self.opPop() # pops condition
            # checks to see if op1 is functionvalue and op2 is a bool value
            if isinstance(op1, FunctionValue) and isinstance(op2, bool):
                # if condition is true then evaluate ifbody
                if op2 == True:
                    self.dictPush(len(self.dictstack)-1, {}) 
                    op1.apply(self)
                    self.dictPop()
            else:
                print("Error: if - operand 1 expects a FunctionValue and operand 2 expects a bool")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: if expects 2 operands")

    """
       Implements ifelse operator. 
       Pops the `elsebody`, `ifbody`, and the condition from opstack. 
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`. 
    """
    def psIfelse(self):
        if len(self.opstack) > 2:
            op1 = self.opPop() # pops elsebody
            op2 = self.opPop() # pops ifbody
            op3 = self.opPop() # pops condition
            # checks to see if op1 and op2 is a functionvalue
            if isinstance(op1, FunctionValue) and isinstance(op2, FunctionValue) and isinstance(op3, bool):
                # if condition is true then evaluate ifbody, else evaluate elsebody
                if op3 == True: 
                    self.dictPush(len(self.dictstack)-1, {})
                    op2.apply(self)
                    self.dictPop()
                else:
                    self.dictPush(len(self.dictstack)-1, {})
                    op1.apply(self)
                    self.dictPop()
            else:
                print("Error: ifelse - operand 1 and operand 2 expects a FunctionValue and operand 3 expects a bool")
                self.opPush(op3)
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: ifelse expects 3 operands")


    #------- Loop Operators --------------
    """
       Implements for operator. 
       Pops a CodeArrayValue object, the end index (end), the increment (inc), and the begin index (begin) and
       executes the code array for all loop index values ranging from `begin` to `end`.
       Pushes the current loop index value to opstack before each execution of the CodeArrayValue. 
       Will be completed in part-2.
        """
    def psFor(self):
        if len(self.opstack) > 3:
            op1 = self.opPop() # pops CodeArrayValue object
            op2 = self.opPop() # pops end index
            op3 = self.opPop() # pops increment
            op4 = self.opPop() # pops begin index
            # checks to see if op2,op3,op4 is an int value and op1 is a functionvalue
            if isinstance(op2, int) and isinstance(op3, int) and isinstance(op4, int) and isinstance(op1, FunctionValue):
                # if incrementer is positive then account for incrementing, else it is decrementing
                if op3 > 0:
                    # executes the codearray for all loop index values ranging from begin to end
                    self.dictPush(len(self.dictstack)-1, {})
                    for i in range(op4, op2+1, op3):
                        self.opPush(i) # pushes the current loop index to opstack
                        op1.apply(self)
                    self.dictPop()
                else:
                    self.dictPush(len(self.dictstack)-1, {})
                    for i in range(op4, op2-1, op3):
                        self.opPush(i) # pushes the current loop index to opstack
                        op1.apply(self)
                    self.dictPop()
            else:
                print("Error: for - operand 2, operand 3, and operand 4 expects an int and operand 1 expects a FunctionValue")
                self.opPush(op4)
                self.opPush(op3)
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: for expects 4 operands")

    """
       Implements repeat operator.   
       Pops the `loop_body` (FunctionValue) and loop `count` (int) arguments from opstack; 
       Evaluates (applies) the `loopbody` `count` times. 
       Will be completed in part-2. 
    """  
    def repeat(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # pops loop_body
            op2 = self.opPop() # pops loop count
            # checks to see if op1 is a Functionvalue and op2 is an int
            if isinstance(op1, FunctionValue) and isinstance(op2, int):
                # applies the loopbody a count number of times
                self.dictPush(len(self.dictstack)-1, {})
                for i in range(op2):
                    op1.apply(self)
                self.dictPop()
            else:
                print("Error: repeat - operand 1 expects a FunctionValue and operand 2 expects a int")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: repeat expects 2 operands")
        
    """
       Implements forall operator.   
       Pops a `codearray` (FunctionValue) and an `array` (ArrayValue) from opstack; 
       Evaluates (applies) the `codearray` on every value in the `array`.  
       Will be completed in part-2. 
    """ 
    def forall(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # pops codearray
            op2 = self.opPop() # pops array
            # checks to see if op1 is a functionvalue and op2 is a arrayvalue
            if isinstance(op1, FunctionValue) and isinstance(op2, ArrayValue):
                array = op2.value # gets the array from the arrayvalue object
                self.dictPush(len(self.dictstack)-1, {})
                for item in array:
                    self.opPush(item) # push each value in the array to the opstack
                    op1.apply(self) # apply the codearray on every value in the array
                self.dictPop()
            else:
                print("Error: forall - operand 1 expects a FunctionValue and operand 2 expects a ArrayValue")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: forall expects 2 operands")

    #--- used in the setup of unittests 
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()
