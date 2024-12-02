from llvmlite import ir

def gerar_ir():
    # Criação do módulo LLVM
    mod = ir.Module(name='top')
    
    # Definindo o tipo de função (int -> int)
    func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
    func = ir.Function(mod, func_type, name='add')

    # Criando o bloco de código da função
    block = func.append_basic_block(name='entry')
    builder = ir.IRBuilder(block)

    # Adicionando parâmetros
    a, b = func.args
    a.name = 'a'
    b.name = 'b'

    # Realizando a operação: a + b
    result = builder.add(a, b, name='result')

    # Retornando o resultado
    builder.ret(result)

    # Exibindo o código LLVM gerado
    print(mod)

gerar_ir()
