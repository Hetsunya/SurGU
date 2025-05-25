@echo off

if exist help.txt goto help 
else (
echo Файл не найден в каталоге
pause )

if exist if.txt goto if 
else (
echo Файл не найден в каталоге
pause)

if exist goto.txt goto goto
else (
echo Файл не найден в каталоге
pause)

:help 
cls
echo cодержимое первого файла
type B:\BatchFile\lab1\bat_file\help.txt
copy B:\BatchFile\lab1\bat_file\goto.txt + B:\BatchFile\lab1\bat_file\if.txt B:\BatchFile\lab1\bat_file\copy_help.txt
echo содержимое объединяемых файлов
type B:\BatchFile\lab1\bat_file\goto.txt
type B:\BatchFile\lab1\bat_file\if.txt
echo содержимое объединённого файла
type B:\BatchFile\lab1\bat_file\copy_help.txt
pause

:if
cls
echo cодержимое первого файла
type B:\BatchFile\lab1\bat_file\if.txt
copy B:\BatchFile\lab1\bat_file\goto.txt + B:\BatchFile\lab1\bat_file\help.txt B:\BatchFile\lab1\bat_file\copy_if.txt
echo содержимое объединяемых файлов
type B:\BatchFile\lab1\bat_file\goto.txt
type B:\BatchFile\lab1\bat_file\help.txt
echo содержимое объединённого файла
type B:\BatchFile\lab1\bat_file\copy_if.txt
pause

:goto
cls
echo cодержимое первого файла
type B:\BatchFile\lab1\bat_file\goto.txt
copy B:\BatchFile\lab1\bat_file\if.txt + B:\BatchFile\lab1\bat_file\help.txt B:\BatchFile\lab1\bat_file\copy_goto.txt
echo содержимое объединяемых файлов
type B:\BatchFile\lab1\bat_file\if.txt
type B:\BatchFile\lab1\bat_file\help.txt
echo содержимое объединённого файла
type B:\BatchFile\lab1\bat_file\copy_goto.txt
pause

