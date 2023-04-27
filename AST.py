from rply.token import BaseBox

# ALL STATEMENTS
class Statements:
    def __init__(self, nodes):
        self.nodes = nodes

    def eval(self):
        for node in self.nodes:
            node.eval()

#   DATATYPES
class Real(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return float(self.value)

class Number(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)
    
class String(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return str(self.value[1:-1])

class Bool(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return True if self.value == "true" else False

#   IDENTIFIER
class Identifier(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return str(self.value) 
    
    def set_value(self, value): 
        self.value = value
        return self.value
    
#   SYNTAX TABLE
class SymbolValue(BaseBox): #   The linked "row" in the 'value' of the hash table
    def __init__(self, type, value):
        self.type = type
        self.value = value if value is not None else None 
        
    def eval(self):
        if self.value is not None:
            if self.type == "pint":
                return int(self.value)
            elif self.type == "dizzy":
                return float(self.value)
            elif self.type == "strong":
                return float(self.value)
            elif self.type == "fool":
                return bool(self.value)
            else:
                raise ValueError("Value is not a valid type")
        return None
    def checkType(self):
        return self.type
    
    #   To add new information with a given name/ID
    def assign(self, value):
        self.value = value
    
    def isNone(self):
        return self.value is None
    
    def print(self):
        print("Type:" + self.type)
        print("Value:" + self.type)
        

class SymbolTable(BaseBox):
    def __init__(self):
        self.dict = {}
        
    def declare(self, id, type, value):    # value must be assume None
        id = Identifier(id)
        self.dict[id.eval()] = SymbolValue(type, value)
        
    def assign(self, id, value):    # value must be assume None
        id = Identifier(id) # id is originally a str
        # ----
        syVal = self.dict[id.eval()]
        syVal.assign(value)
        self.dict[id.eval()] = syVal
    
    # def remove(self, id):
    def eval(self):
        return self.dict

sytab = SymbolTable()

#   OPERATORS
class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
class UnaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Declare:
    def __init__(self, type, id):
        self.type = type
        self.id = Identifier(id)
    def eval(self):    
        # print("AST Declare entries: " + self.id.eval())
        if isinstance(self.id, Identifier):  #left is type, right is ID
            # declare variable
            #   official values when declared and not assign from C++
            if self.type == 'pint' or self.type == 'fool':
                sytab.declare(self.id.eval(), self.type, 0)
            elif self.type == 'real':
                sytab.declare(self.id.eval(), self.type, 4.94066*pow(10, (-324)))   #-324
            else:   #   'string' and others
                sytab.declare(self.id.eval(), self.type, None)
        else:
            raise ValueError("Right-hand side of declaration must be an Identifier.")
        return self.id

class Assign(BinaryOp):
    def eval(self):
        # evaluate the right-hand side expression
        value = self.right.eval()
        
        id = Identifier(self.left)
        # assign the value to the left-hand side variable
        if isinstance(id, Identifier):
            # variable is assumed to be already declared
            # #checktype
            # # datatype = sytab.dict[id].checkType()
            # # if datatype == 'real':
            # #     datatype = 'float'
            # # if str(datatype) == type()
            
            # check if variable is declared in symbol table
            if(id.eval() in sytab.dict.keys()):
                sytab.assign(id.eval(), value)  #   assigns new value to declaration
            else: 
                raise RuntimeError("Variable not declared can not be assigned: ", id.eval())
        else:
            raise ValueError("Left-hand side of assignment must be an Identifier.")

        return value
    
class If:
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def eval(self):
        if self.condition.eval() is bool(1):
            return self.body.eval()
        elif self.else_body is not None:
            return self.else_body.eval()
        # return None

class WhileLoop:
    def __init__(self, condition, function):
        self.condition = condition
        self.function = function

    def eval(self):
        while(self.condition.eval() is True):   #   if true, do body
            self.function.eval()

class ForLoop:
    def __init__(self, id, condition, proc, function):
        self.id = Identifier(id.getstr())
        self.condition = condition
        self.proc = proc
        self.function = function
        
    def eval(self):
        if(self.id.eval() in sytab.dict.keys()): #   meaning a variable with name id exists
            while(self.condition.eval() is True):   #   if true, do body
                self.function.eval()
                self.proc.eval()    # applies procedure (i += 1)
        else:
            raise RuntimeError("Variable not declared can not be used in loop: ", self.id.eval())
        
class Variable:
    def __init__(self, id):
        self.id = id.getstr()
    
    def eval(self):
        if self.id in sytab.dict.keys():
            var = sytab.dict[self.id]
            return var.eval()
        else: 
            raise RuntimeError("Variable not declared:", self.id)

class And(BinaryOp):
    def eval(self):
        if isinstance(self.left.eval(), Bool) and isinstance(self.right.eval(), Bool):
            return(self.left.eval() and self.right.eval())
        else: 
            raise RuntimeError("One of the expressions is not boolean AND")
        
class Or(BinaryOp):
    def eval(self):
        if isinstance(self.left.eval(), Bool) and isinstance(self.right.eval(), Bool):
            return(self.left.eval() or self.right.eval())
        else: 
            raise RuntimeError("One of the expressions is not boolean OR")

class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()

class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()
    
class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()

class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()

#   Relational operators   
class Smaller(BinaryOp):
    def eval(self):
        return self.left.eval() < self.right.eval()
    
class Greater(BinaryOp):
    def eval(self):
        return self.left.eval() > self.right.eval()
    
class Noteq(BinaryOp):
    def eval(self):
        return self.left.eval() != self.right.eval()
    
class Equal(BinaryOp):
    def eval(self):
        return self.left.eval().__eq__(self.right.eval())

class SmallerEq(BinaryOp):
    def eval(self):
        return self.left.eval() <= self.right.eval()

class GreaterEq(BinaryOp):
    def eval(self):
        return self.left.eval() >= self.right.eval()
    

#   Print
class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())
