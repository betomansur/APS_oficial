@echo off
REM Limpa a tela para uma execução limpa
cls

REM Compilar o parser com o Bison
echo Compilando o arquivo invertido.y com Bison...
bison -d invertido.y -o invertido.tab.c
if errorlevel 1 (
    echo ERRO: Falha ao compilar o arquivo invertido.y com Bison.
    pause
    exit /b 1
)

REM Compilar o lexer com o Flex
echo Compilando o arquivo invertido.l com Flex...
flex -o lex.yy.c invertido.l
if errorlevel 1 (
    echo ERRO: Falha ao compilar o arquivo invertido.l com Flex.
    pause
    exit /b 1
)

REM Compilar os arquivos gerados com o GCC
echo Compilando os arquivos gerados com GCC...
gcc -o invertido_compiler.exe invertido.tab.c lex.yy.c -I.
if errorlevel 1 (
    echo ERRO: Falha ao compilar os arquivos C gerados com GCC.
    pause
    exit /b 1
)

REM Verificar se a pasta 'testes' existe
if not exist testes (
    echo ERRO: A pasta 'testes' nao existe.
    pause
    exit /b 1
)

REM Executar o compilador em cada arquivo de teste
echo Executando testes na pasta 'testes'...
for %%f in (testes\*.inv) do (
    echo -------------------------------
    echo Testando arquivo: %%~nxf
    invertido_compiler.exe < %%f
    if errorlevel 1 (
        echo ERRO ao processar o arquivo %%~nxf.
    )
    echo -------------------------------
)

echo TODOS OS TESTES FORAM EXECUTADOS.
pause
