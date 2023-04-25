from rply.token import BaseBox

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
    
class Identifier(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value  # how to make them all data type
    
    def set_value(self, value): 
        self.value = value
        return self.value

class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Assign(BinaryOp):
    def eval(self):
        # evaluate the right-hand side expression
        value = self.right.eval()
        
        # assign the value to the left-hand side variable
        if isinstance(self.left, Identifier):
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