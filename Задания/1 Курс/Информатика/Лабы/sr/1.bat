@echo off

if -%1== - goto NoParam
if -%2== - goto NoParam

if not %1 == %2 (
echo %1 > %1.txt
echo 1111 >> %1.txt
call B:\sr\1_3.bat
goto end) else (
md %1 
echo %2 > %1\%2.txt
echo 2222 >> %1\%2.txt
call B:\sr\1_2.bat
goto end)

:NoParam
echo Входные аргументы не заданы

:end
pause