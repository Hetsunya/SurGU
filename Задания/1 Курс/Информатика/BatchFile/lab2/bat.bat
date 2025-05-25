@echo off
:start
echo.
echo.
echo.
echo.
echo.
echo             **********************************************************
echo             *                                                        *
echo             *            1 - калькулятор.                            *
echo             *            2 - Программа "Блокнот."                    *
echo             *            3 - Часы.                                   *
echo             *            4 - Антивирусная прогмма DrWeb.             *
echo             *            5 - Моя собственная программа.              *
echo             *            6 - Выход из программы.                     *
echo             *                                                        *
echo             *   Нажмите нужную клавишу для запуска программы.        *
echo             *                                                        *
echo             **********************************************************
echo                       Завершение программы через 5 секунд.

choice /C 123456 /T 5 /D 6 /N

if errorlevel 6 goto 6
if errorlevel 5 goto 5
if errorlevel 4 goto 4
if errorlevel 3 goto 3
if errorlevel 2 goto 2
if errorlevel 1 goto 1

:1
C:\Windows\System32\calc.exe
pause
cls
goto start

:2 
C:\Windows\System32\notepad.exe
pause
cls
goto start

:3
time /T
pause
cls
goto start

:4
P:\DrWeb
pause
cls
goto start

:5
call B:\BatchFile\lab2\1.jpg
pause
cls
goto start 

:6
exit