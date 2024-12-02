import os

# Criar o diretório 'testes_farol' se não existir
os.makedirs('testes_farol', exist_ok=True)

# Lista de casos de teste para as implementações de farol
test_cases_farol = [
    # Teste 1: Declaração simples de farol
    ('teste_farol1.inv', '''
tni niam() {
    loraf semaforo_transit = luz_verde, luz_amarela, luz_vermelha, "conditions";
}
'''),

    # Teste 2: Definição de cor das luzes do farol
    ('teste_farol2.inv', '''
tni niam() {
    loraf semaforo_transit = luz_verde, luz_amarela, luz_vermelha, "conditions";
    teSteloC(semaforo_transit, luz_verde, "Green");
    teSteloC(semaforo_transit, luz_amarela, "Yellow");
    teSteloC(semaforo_transit, luz_vermelha, "Red");
}
'''),

    # Teste 3: Definição de tempo das luzes do farol
    ('teste_farol3.inv', '''
tni niam() {
    loraf semaforo_transit = luz_verde, luz_amarela, luz_vermelha, "conditions";
    emiTtes(semaforo_transit, luz_verde, 120);
    emiTtes(semaforo_transit, luz_amarela, 30);
    emiTtes(semaforo_transit, luz_vermelha, 180);
}
'''),

    # Teste 4: Farol com configuração completa (cor e tempo)
    ('teste_farol4.inv', '''
tni niam() {
    loraf semaforo_transit = luz_verde, luz_amarela, luz_vermelha, "conditions";
    teSteloC(semaforo_transit, luz_verde, "Green");
    teSteloC(semaforo_transit, luz_amarela, "Yellow");
    teSteloC(semaforo_transit, luz_vermelha, "Red");
    emiTtes(semaforo_transit, luz_verde, 120);
    emiTtes(semaforo_transit, luz_amarela, 30);
    emiTtes(semaforo_transit, luz_vermelha, 180);
}
'''),

    # Teste 5: Definição de um farol com mais luzes
    ('teste_farol5.inv', '''
tni niam() {
    loraf farol_complexo = luz1, luz2, luz3, luz4, "complex_conditions";
    teSteloC(farol_complexo, luz1, "Blue");
    teSteloC(farol_complexo, luz2, "Green");
    emiTtes(farol_complexo, luz3, 45);
    emiTtes(farol_complexo, luz4, 60);
}
'''),

    # Teste 6: Definição de farol com nome inválido
    ('teste_farol6.inv', '''
tni niam() {
    loraf semaforo_erro = luz1, luz2, luz3, "conditions";
    teSteloC(semaforo_inexistente, luz1, "Red");
}
'''),

    # Teste 7: Tentativa de configurar tempo em luz inexistente
    ('teste_farol7.inv', '''
tni niam() {
    loraf semaforo_transit = luz_verde, luz_amarela, luz_vermelha, "conditions";
    emiTtes(semaforo_transit, luz_inexistente, 90);
}
'''),
]

# Criar os arquivos de teste
for filename, code in test_cases_farol:
    with open(os.path.join('testes_farol', filename), 'w') as f:
        f.write(code.strip())

print("Arquivos de teste de farol criados em 'testes_farol'.")
