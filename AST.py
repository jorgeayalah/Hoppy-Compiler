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
        return True if self.value == True else False

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
        if self.type == "int":
            return int(self.value)
        elif self.type == "real":
            return float(self.value)
        elif self.type == "string":
            return float(self.value)
        elif self.type == "bool":
            return float(self.value)
        else:
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
        print(id.eval())
        self.dict[id.eval()] = SymbolValue(type, value)
        print("Values: ")
        print(self.dict.values())
        
    def assign(self, id, value):    # value must be assume None
        # id = Identifier(id) # id is originally a str
        
        print("First id:" + id)
        id = Identifier(id)
        print("After: " + id.eval())
        # self.dict[id.eval()].assign(value)
        # self.dict[id.eval()].print()
        # ----
        print(sytab.dict.keys())
        print(type(id.eval()))
        syVal = self.dict[id.eval()]
        syVal.assign(value)
        self.dict[id.eval()] = syVal
        print("y la q asigne")
        
    # def remove(self, id):

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
        print("AST Declare entries: " + self.id.eval())
        if isinstance(self.id, Identifier):  #left is type, right is ID
            # declare variable
            sytab.declare(self.id.eval(), self.type, None)
            print("declared successful")
            print(sytab.dict.keys())
        else:
            raise ValueError("Right-hand side of declaration must be an Identifier.")
        # return None

class Assign(BinaryOp):
    # def __init__(self, id, value):
    #     self.id = Identifier(id)
    #     self.value = value
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
            
            # assign variable
            
            sytab.assign(str(self.left), value)
            print("assignment successful")
        else:
            raise ValueError("Left-hand side of assignment must be an Identifier.")

        return value
    
class If:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def eval(self):
        if self.condition.eval() == "true":
            return self.body.eval()
        elif self.else_body is not None:
            return self.else_body.eval()
        return Null()

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
        return self.left.eval() == self.right.eval()

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
