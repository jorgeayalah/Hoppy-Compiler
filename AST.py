from rply.token import BaseBox

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
        id = Identifier(id)
        self.dict[id.eval()].assign(value)
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
            sytab.declare(self.id, self.type, None)
            print("declared successful")
        else:
            raise ValueError("Right-hand side of declaration must be an Identifier.")
        # return None

class Assign(BinaryOp):
    def eval(self):
        # evaluate the right-hand side expression
        value = self.right.eval()
        
        self.left = Identifier(self.left)
        # assign the value to the left-hand side variable
        if isinstance(self.left, Identifier):
            # declare variable
            sytab.declare(self.left.eval(), type, None)
            print("declared successful")
            # assign variable
            sytab.assign(self.left.eval(), value)
            print("assignment successful")
            #old set value
            self.left.set_value(value)
        else:
            raise ValueError("Left-hand side of assignment must be an Identifier.")

        return value

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
