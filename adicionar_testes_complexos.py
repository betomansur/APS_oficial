import os

# Certifique-se de que a pasta 'testes' existe
os.makedirs('testes', exist_ok=True)

# Lista de casos de teste mais complexos
test_cases = [
    # Teste 11: Função recursiva - Fatorial
    ('teste11.inv', '''
tni factorial(tni n) {
    fi (n <= 1) {
        nruter 1;
    } esle {
        nruter n * factorial(n - 1);
    }
}

tni niam() {
    tni result = factorial(5);
    ftnirp("Fatorial de 5 é %d\\n", result);
}
'''),

    # Teste 12: Função recursiva - Fibonacci
    ('teste12.inv', '''
tni fibonacci(tni n) {
    fi (n <= 0) {
        nruter 0;
    } esle fi (n == 1) {
        nruter 1;
    } esle {
        nruter fibonacci(n - 1) + fibonacci(n - 2);
    }
}

tni niam() {
    tni n = 10;
    tni result = fibonacci(n);
    ftnirp("Fibonacci de %d é %d\\n", n, result);
}
'''),

    # Teste 13: Múltiplas funções e chamadas
    ('teste13.inv', '''
tni quadrado(tni x) {
    nruter x * x;
}

tni cubo(tni x) {
    nruter x * x * x;
}

tni niam() {
    tni a = 3;
    tni sq = quadrado(a);
    tni cb = cubo(a);
    ftnirp("Quadrado de %d é %d\\n", a, sq);
    ftnirp("Cubo de %d é %d\\n", a, cb);
}
'''),

    # Teste 14: Uso de operadores lógicos
    ('teste14.inv', '''
tni niam() {
    tni a = 5;
    tni b = 10;
    fi (a < b && b > 0) {
        ftnirp("Ambas as condições são verdadeiras\\n", 0);
    }
}
'''),

    # Teste 15: Funções com múltiplos parâmetros
    ('teste15.inv', '''
tni max(tni a, tni b, tni c) {
    tni max = a;
    fi (b > max) {
        max = b;
    }
    fi (c > max) {
        max = c;
    }
    nruter max;
}

tni niam() {
    tni result = max(7, 3, 5);
    ftnirp("O máximo é %d\\n", result);
}
'''),

    # Teste 16: Funções aninhadas (se suportado)
    ('teste16.inv', '''
tni outer(tni x) {
    tni inner(tni y) {
        nruter y * y;
    }
    nruter inner(x) + x;
}

tni niam() {
    tni result = outer(5);
    ftnirp("Resultado é %d\\n", result);
}
'''),

    # Teste 17: Manipulação de escopo de variáveis
    ('teste17.inv', '''
tni x = 10;

tni niam() {
    tni x = 5;
    ftnirp("x local = %d\\n", x);
    ftnirp("x global = %d\\n", ::x);
}
'''),

    # Teste 18: Função com retorno de void (diov)
    ('teste18.inv', '''
diov saudacao() {
    ftnirp("Olá, mundo!\\n", 0);
}

tni niam() {
    saudacao();
}
'''),

    # Teste 19: Condicionais complexas
    ('teste19.inv', '''
tni niam() {
    tni a = 5;
    tni b = 10;
    tni c = 15;
    fi ((a < b || b > c) && !(a == c)) {
        ftnirp("Condição complexa satisfeita\\n", 0);
    }
}
'''),

    # Teste 20: Loop aninhado com condicional
    ('teste20.inv', '''
tni niam() {
    tni i = 0;
    elihw (i < 3) {
        tni j = 0;
        elihw (j < 3) {
            fi (i == j) {
                ftnirp("i e j são iguais: %d\\n", i);
            }
            j = j + 1;
        }
        i = i + 1;
    }
}
'''),
]

# Criar os arquivos de teste
for filename, code in test_cases:
    with open(os.path.join('testes', filename), 'w') as f:
        f.write(code.strip())
