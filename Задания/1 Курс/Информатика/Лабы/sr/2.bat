@echo off

IF -%1==- GOTO NoParam
IF -%2==- GOTO NoParam

if not %1 == %2 (
md %1
md %1\%1
call B:\sr\2_3.bat
goto end) else (
md %1 
md %2 
echo %2 > %2\%2.txt
copy %2\%2.txt %1\%1.txt
echo %1 >> %1\%1.txt
call B:\sr\2_2.bat
goto end)

:NoParam
echo Входные аргументы не заданы

:end
pause