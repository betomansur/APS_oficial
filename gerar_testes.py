import os

# Criar o diretório 'testes' se não existir
os.makedirs('testes', exist_ok=True)

# Lista de casos de teste compatíveis com o compilador atual
test_cases = [
    # Teste 1: Declaração simples de variável
    ('teste1.inv', '''
tni niam() {
    tni a = 5;
}
'''),

    # Teste 2: Operações aritméticas simples
    ('teste2.inv', '''
tni niam() {
    tni a = 5;
    tni b = 3;
    tni c = a + b;
}
'''),

    # Teste 3: Declaração e uso de 'fi'
    ('teste3.inv', '''
tni niam() {
    tni a = 5;
    fi (a > 3) {
        ftnirp("a is greater than 3\\n", 0);
    }
}
'''),

    # Teste 4: Uso de 'fi' e 'esle'
    ('teste4.inv', '''
tni niam() {
    tni a = 2;
    fi (a > 3) {
        ftnirp("a is greater than 3\\n", 0);
    } esle {
        ftnirp("a is not greater than 3\\n", 0);
    }
}
'''),

    # Teste 5: Loop 'elihw' com incremento
    ('teste5.inv', '''
tni niam() {
    tni i = 0;
    elihw (i < 5) {
        ftnirp("%d\\n", i);
        i = i + 1;
    }
}
'''),

    # Teste 6: Atribuição de variável e impressão
    ('teste6.inv', '''
tni niam() {
    tni x;
    x = 10;
    ftnirp("x = %d\\n", x);
}
'''),

    # Teste 7: Expressões aritméticas com parênteses
    ('teste7.inv', '''
tni niam() {
    tni a = 5;
    tni b = 3;
    tni c = a * (b + 2);
    ftnirp("c = %d\\n", c);
}
'''),

    # Teste 8: Estruturas 'fi' aninhadas
    ('teste8.inv', '''
tni niam() {
    tni a = 5;
    fi (a > 0) {
        fi (a < 10) {
            ftnirp("a is between 0 and 10\\n", 0);
        }
    }
}
'''),

    # Teste 9: Uso de operadores relacionais '=='
    ('teste9.inv', '''
tni niam() {
    tni a = 5;
    tni b = 5;
    fi (a == b) {
        ftnirp("a is equal to b\\n", 0);
    }
}
'''),

    # Teste 10: Impressão de uma string simples
    ('teste10.inv', '''
tni niam() {
    ftnirp("Hello, World!\\n", 0);
}
'''),
]

# Criar os arquivos de teste
for filename, code in test_cases:
    with open(os.path.join('testes', filename), 'w') as f:
        f.write(code.strip())
