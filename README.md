# Linguagem de Programação

**Este projeto, desenvolvido por:**

 - Alberto Mansur
 - Bruno Falcão

## Características

- As palavras-chave são invertidas.
- Suporte a variáveis, funções, condicionais, loops e operações aritméticas.
- Exemplo de palavras-chave invertidas:
  - `tni` → `int`
  - `fi` → `if`
  - `esle` → `else`
  - `ftnirp` → `printf`
 
### Diferenças para o C
 - Implementamos o `**` -> Exponencial

## Exemplo de código

Uma função que multiplica dois números e imprime o resultado:

```c
tni multiplica(tni a, tni b) {
    nruter a * b;
}

tni resultado;
resultado = multiplica(3, 4);
ftnirp(resultado);
```

## Como Executar

```bash
flex invertido.l
bison -d invertido.y
gcc invertido.tab.c lex.yy.c -o invertido
.\invertido.exe input.txt
```


## Documentação básica
# Regras da Linguagem C Invertido

| **C**      | **C Invertido** |
|------------|-----------------|
| `int`      | `tni`           |
| `float`    | `taolf`         |
| `char`     | `rahc`          |
| `void`     | `diov`          |
| `return`   | `nruter`        |
| `printf`   | `ftnirp`        |
| `if`       | `fi`            |
| `else`     | `esle`          |
| `while`    | `elihw`         |
| `for`      | `rof`           |
| `&&`       | `dna`           |
| `\|\|`       | `ro `           |
| `! `       | `ton`           |

