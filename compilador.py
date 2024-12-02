import sys
import re
from vm import gerar_ir  # Importando a função que gera o código LLVM IR


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
    
    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token('EOF', None)
            return
        
        char = self.source[self.position]

        if char.isdigit():
            num = ''
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token('INT', int(num))
        
        elif char.isalpha() or char == '"':
            ident = ''
            if char == '"':
                raise Exception("Strings não são suportadas.")
            else:
                while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                    ident += self.source[self.position]
                    self.position += 1
                if ident == 'printf':
                    self.next = Token('PRINTF', ident)
                elif ident == 'if':
                    self.next = Token('IF', ident)
                elif ident == 'else':
                    self.next = Token('ELSE', ident)
                elif ident == 'while':
                    self.next = Token('WHILE', ident)
                elif ident == 'int':
                    self.next = Token('INT_TYPE', ident)
                elif ident == 'true':
                    self.next = Token('TRUE', ident)
                elif ident == 'false':
                    self.next = Token('FALSE', ident)
                else:
                    self.next = Token('ID', ident)
        
        elif char == '+':
            self.next = Token('PLUS', char)
            self.position += 1
        
        elif char == '-':
            self.next = Token('MINUS', char)
            self.position += 1
        
        elif char == '*':
            self.next = Token('MULT', char)
            self.position += 1
    
        elif char == '/':
            self.next = Token('DIV', char)
            self.position += 1

        elif char == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token('EQUALS', '==')
                self.position += 2
            else:
                self.next = Token('EQUAL', char)
                self.position += 1
        
        elif char == '>':
            self.next = Token('GT', char)
            self.position += 1
        
        elif char == '<':
            self.next = Token('LT', char)
            self.position += 1
        
        elif char == '!':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token('NEQUALS', '!=')
                self.position += 2
            else:
                self.next = Token('NOT', char)
                self.position += 1
        
        elif char == '&' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
            self.next = Token('AND', '&&')
            self.position += 2
        
        elif char == '|' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
            self.next = Token('OR', '||')
            self.position += 2
        
        elif char == '(':
            self.next = Token('LPAREN', char)
            self.position += 1
        
        elif char == ')':
            self.next = Token('RPAREN', char)
            self.position += 1

        elif char == '{':
            self.next = Token('LBRACE', char)
            self.position += 1
        
        elif char == '}':
            self.next = Token('RBRACE', char)
            self.position += 1

        elif char == ';':
            self.next = Token('SEMICOLON', char)
            self.position += 1

        elif char == ',':
            self.next = Token('COMMA', char)
            self.position += 1

        elif char.isspace():
            self.position += 1
            self.selectNext()
        
        else:
            raise Exception(f"Caractere inválido: {char}")

class PrePro:
    def filter(self, source):
        return re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)

class Node:
    i = 0
    code = ''
    variables = {}
    labels = 0

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i

    @staticmethod
    def newLabel():
        Node.labels += 1
        return f"label{Node.labels}"

    def __init__(self, value):
        self.value = value
        self.id = Node.newId()
        self.children = []

    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, left, right):
        super().__init__(value)
        self.children = [left, right]

    def Evaluate(self):
        self.children[0].Evaluate()
        Node.code += 'PUSH EBX\n'
        self.children[1].Evaluate()
        Node.code += 'POP EAX\n'

        if self.value == 'PLUS':
            Node.code += 'ADD EAX, EBX\n'
        elif self.value == 'MINUS':
            Node.code += 'SUB EAX, EBX\n'
        elif self.value == 'MULT':
            Node.code += 'IMUL EBX\n'
        elif self.value == 'DIV':
            Node.code += 'IDIV EBX\n'
        elif self.value == 'AND':
            Node.code += 'AND EAX, EBX\n'
        elif self.value == 'OR':
            Node.code += 'OR EAX, EBX\n'
        elif self.value == 'EQUALS':
            Node.code += 'CMP EAX, EBX\nCALL binop_je\n'
            return
        elif self.value == 'NEQUALS':
            Node.code += 'CMP EAX, EBX\nCALL binop_jne\n'
            return
        elif self.value == 'GT':
            Node.code += 'CMP EAX, EBX\nCALL binop_jg\n'
            return
        elif self.value == 'LT':
            Node.code += 'CMP EAX, EBX\nCALL binop_jl\n'
            return
        else:
            raise Exception(f"Operação desconhecida: {self.value}")
        Node.code += 'MOV EBX, EAX\n'

class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self):
        self.children[0].Evaluate()
        if self.value == 'PLUS':
            pass
        elif self.value == 'MINUS':
            Node.code += 'NEG EBX\n'
        elif self.value == 'NOT':
            Node.code += 'NOT EBX\nAND EBX, 1\n'
        else:
            raise Exception(f"Operação unária desconhecida: {self.value}")

class IntVal(Node):
    def __init__(self, value):
        super().__init__('IntVal')
        self.value = value

    def Evaluate(self):
        Node.code += f'MOV EBX, {self.value}\n'

class Identifier(Node):
    def __init__(self, value):
        super().__init__('Identifier')
        self.value = value

    def Evaluate(self):
        if self.value not in Node.variables:
            raise Exception(f"Variável não declarada: {self.value}")
        Node.code += f'MOV EBX, [EBP-{Node.variables[self.value]}]\n'

class NoOp(Node):
    def __init__(self):
        super().__init__('NoOp')

    def Evaluate(self):
        pass

class Assignment(Node):
    def __init__(self, identifier, expression):
        super().__init__('Assignment')
        self.identifier = identifier
        self.expression = expression

    def Evaluate(self):
        if self.identifier not in Node.variables:
            raise Exception(f"Variável não declarada: {self.identifier}")
        self.expression.Evaluate()
        Node.code += f'MOV [EBP-{Node.variables[self.identifier]}], EBX\n'

class Printf(Node):
    def __init__(self, expression):
        super().__init__('Printf')
        self.expression = expression

    def Evaluate(self):
        self.expression.Evaluate()
        Node.code += 'PUSH EBX\nCALL print\nADD ESP, 4\n'

class Block(Node):
    def __init__(self, statements):
        super().__init__('Block')
        self.statements = statements

    def Evaluate(self):
        for statement in self.statements:
            if statement is not None:
                statement.Evaluate()

class If(Node):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__('If')
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def Evaluate(self):
        else_label = Node.newLabel()
        end_label = Node.newLabel()

        self.condition.Evaluate()
        Node.code += f'CMP EBX, False\nJE {else_label}\n'
        self.true_block.Evaluate()
        Node.code += f'JMP {end_label}\n'
        Node.code += f'{else_label}:\n'
        if self.false_block:
            self.false_block.Evaluate()
        Node.code += f'{end_label}:\n'

class While(Node):
    def __init__(self, condition, block):
        super().__init__('While')
        self.condition = condition
        self.block = block

    def Evaluate(self):
        start_label = Node.newLabel()
        end_label = Node.newLabel()

        Node.code += f'{start_label}:\n'
        self.condition.Evaluate()
        Node.code += f'CMP EBX, False\nJE {end_label}\n'
        self.block.Evaluate()
        Node.code += f'JMP {start_label}\n'
        Node.code += f'{end_label}:\n'

class VarDec(Node):
    def __init__(self, declarations, var_type):
        super().__init__('VarDec')
        self.declarations = declarations
        self.var_type = var_type

    def Evaluate(self):
        for identifier, expr in self.declarations:
            if identifier in Node.variables:
                raise Exception(f"Variável já declarada: {identifier}")
            offset = 4 * (len(Node.variables) + 1)
            Node.variables[identifier] = offset
            Node.code += 'PUSH DWORD 0\n'
            if expr is not None:
                assignment = Assignment(identifier, expr)
                assignment.Evaluate()

class Parser:
    def __init__(self):
        self.tokenizer = None

    def parseFactor(self):
        if self.tokenizer.next.type in ['PLUS', 'MINUS', 'NOT']:
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            factor = self.parseFactor()
            return UnOp(op, factor)
        
        elif self.tokenizer.next.type == 'INT':
            value = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return IntVal(value)

        elif self.tokenizer.next.type == 'TRUE':
            self.tokenizer.selectNext()
            return IntVal(1)

        elif self.tokenizer.next.type == 'FALSE':
            self.tokenizer.selectNext()
            return IntVal(0)

        elif self.tokenizer.next.type == 'LPAREN':
            self.tokenizer.selectNext()
            expr = self.parseExpression()
            if self.tokenizer.next.type != 'RPAREN':
                raise Exception("Parêntese direito esperado")
            self.tokenizer.selectNext()
            return expr
        
        elif self.tokenizer.next.type == 'ID':
            identifier = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return Identifier(identifier)

        else:
            raise Exception(f"Fator inválido: {self.tokenizer.next.type}")

    def parseTerm(self):
        node = self.parseFactor()
        
        while self.tokenizer.next.type in ['MULT', 'DIV', 'AND']:
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            node = BinOp(op, node, self.parseFactor())
        
        return node
    
    def parseExpression(self):
        node = self.parseTerm()
        
        while self.tokenizer.next.type in ['PLUS', 'MINUS', 'OR']:
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            node = BinOp(op, node, self.parseTerm())
        
        if self.tokenizer.next.type in ['EQUALS', 'NEQUALS', 'GT', 'LT']:
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            node = BinOp(op, node, self.parseExpression())

        return node

    def parseStatement(self):
        if self.tokenizer.next.type == 'INT_TYPE':
            var_type = self.tokenizer.next.type
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'ID':
                declarations = []
                while True:
                    identifier = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    expr = None
                    if self.tokenizer.next.type == 'EQUAL':
                        self.tokenizer.selectNext()
                        expr = self.parseExpression()
                    declarations.append((identifier, expr))
                    if self.tokenizer.next.type == 'COMMA':
                        self.tokenizer.selectNext()
                        continue
                    else:
                        break
                if self.tokenizer.next.type == 'SEMICOLON':
                    self.tokenizer.selectNext()
                    return VarDec(declarations, var_type)
                else:
                    raise Exception("Ponto e vírgula esperado após declaração")
            else:
                raise Exception("Identificador esperado após tipo")

        elif self.tokenizer.next.type == 'ID':
            identifier = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'EQUAL':
                self.tokenizer.selectNext()
                expression = self.parseExpression()
                if self.tokenizer.next.type != 'SEMICOLON':
                    raise Exception("Ponto e vírgula esperado após atribuição")
                self.tokenizer.selectNext()
                return Assignment(identifier, expression)
            else:
                raise Exception("Operador '=' esperado")

        elif self.tokenizer.next.type == 'PRINTF':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'LPAREN':
                self.tokenizer.selectNext()
                expression = self.parseExpression()
                if self.tokenizer.next.type != 'RPAREN':
                    raise Exception("Parêntese direito esperado em Printf")
                self.tokenizer.selectNext()
                if self.tokenizer.next.type != 'SEMICOLON':
                    raise Exception("Ponto e vírgula esperado após Printf")
                self.tokenizer.selectNext()
                return Printf(expression)
            else:
                raise Exception("Parêntese esquerdo esperado em Printf")

        elif self.tokenizer.next.type == 'IF':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'LPAREN':
                self.tokenizer.selectNext()
                condition = self.parseExpression()
                if self.tokenizer.next.type != 'RPAREN':
                    raise Exception("Parêntese direito esperado em If")
                self.tokenizer.selectNext()

                if self.tokenizer.next.type == 'LBRACE':
                    true_block = self.parseBlock()
                else:
                    true_block = self.parseStatement()

                false_block = None
                if self.tokenizer.next.type == 'ELSE':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == 'LBRACE':
                        false_block = self.parseBlock()
                    else:
                        false_block = self.parseStatement()
                return If(condition, true_block, false_block)
            else:
                raise Exception("Parêntese esquerdo esperado em If")

        elif self.tokenizer.next.type == 'WHILE':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'LPAREN':
                self.tokenizer.selectNext()
                condition = self.parseExpression()
                if self.tokenizer.next.type != 'RPAREN':
                    raise Exception("Parêntese direito esperado em While")
                self.tokenizer.selectNext()

                if self.tokenizer.next.type == 'LBRACE':
                    block = self.parseBlock()
                else:
                    block = self.parseStatement()

                return While(condition, block)
            else:
                raise Exception("Parêntese esquerdo esperado em While")

        elif self.tokenizer.next.type == 'SEMICOLON':
            self.tokenizer.selectNext()
            return NoOp()

        elif self.tokenizer.next.type == 'LBRACE':
            return self.parseBlock()

        else:
            raise Exception(f"Declaração inválida: {self.tokenizer.next.type}")

    def parseBlock(self):
        if self.tokenizer.next.type != 'LBRACE':
            raise Exception("Chave esquerda esperada no início do bloco")
        
        self.tokenizer.selectNext()
        statements = []

        while self.tokenizer.next.type != 'RBRACE':
            statements.append(self.parseStatement())

        self.tokenizer.selectNext()  
        
        return Block(statements)

    def run(self, code):
        if code.strip() == "":
            raise Exception("Código vazio")

        prepro = PrePro()
        filtered_code = prepro.filter(code)
        self.tokenizer = Tokenizer(filtered_code)
        self.tokenizer.selectNext()
        statements = []

        while self.tokenizer.next.type != 'EOF':
            statements.append(self.parseStatement())
        
        return Block(statements)

def main():
    if len(sys.argv) < 2:
        print("Uso: python compilador.py arquivo_entrada [arquivo_saida]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = 'teste1.asm'
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]

    with open(input_file, 'r') as file:
        code = file.read()
    
    parser = Parser()
    try:
        tree = parser.run(code)

        Node.code = '''; Codigo assembly gerado

; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

section .data
  msg DB "%d", 10, 0

section .bss
  res RESB 1
'''

        Node.code += '''
section .text
  global main
  extern printf

; subrotinas

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jne:
  JNE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

print:
  PUSH EBP
  MOV EBP, ESP
  PUSH EBX
  PUSH msg
  CALL printf
  ADD ESP, 8
  MOV ESP, EBP
  POP EBP
  RET

main:

  PUSH EBP
  MOV EBP, ESP

'''

        tree.Evaluate()

        Node.code += '''

  ; interrupcao de saida
  MOV ESP, EBP
  POP EBP
  MOV EAX, 0
  RET
'''

        with open(output_file, 'w') as f:
            f.write(Node.code)

        print(f"Código assembly gerado com sucesso no arquivo '{output_file}'.")
             
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()