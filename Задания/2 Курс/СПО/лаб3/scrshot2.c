#include <windows.h>
#include <stdio.h>
//  gcc -o scrshot2 scrshot2.c -l gdi32
// Функция создания скриншота



void captureScreenshot(const char* filename) {
    // Получение размеров экрана
    int width = GetSystemMetrics(SM_CXSCREEN);
    int height = GetSystemMetrics(SM_CYSCREEN);

    // Создание контекста устройства для всего экрана
    HDC hdcScreen = GetDC(NULL);
    HDC hdcMemDC = CreateCompatibleDC(hdcScreen);

    // Создание битовой карты для копирования экрана
    HBITMAP hbmScreen = CreateCompatibleBitmap(hdcScreen, width, height);
    SelectObject(hdcMemDC, hbmScreen);

    // Копирование экрана в битовую карту
    BitBlt(hdcMemDC, 0, 0, width, height, hdcScreen, 0, 0, SRCCOPY);

    // Сохранение битовой карты в файл
    BITMAPINFOHEADER bih;
    bih.biSize = sizeof(BITMAPINFOHEADER);
    bih.biWidth = width;
    bih.biHeight = height;
    bih.biPlanes = 1;
    bih.biBitCount = 24;
    bih.biCompression = BI_RGB;
    bih.biSizeImage = 0;
    bih.biXPelsPerMeter = 0;
    bih.biYPelsPerMeter = 0;
    bih.biClrUsed = 0;
    bih.biClrImportant = 0;

    BITMAPFILEHEADER bfh;
    bfh.bfType = 0x4D42;
    bfh.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    bfh.bfSize = bfh.bfOffBits + (width * height * 3);

    HANDLE fileHandle = CreateFile(filename, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    DWORD bytesWritten;
    WriteFile(fileHandle, &bfh, sizeof(BITMAPFILEHEADER), &bytesWritten, NULL);
    WriteFile(fileHandle, &bih, sizeof(BITMAPINFOHEADER), &bytesWritten, NULL);
    WriteFile(fileHandle, (LPVOID)(hbmScreen), (width * height * 3), &bytesWritten, NULL);
    CloseHandle(fileHandle);

    // Освобождение ресурсов
    DeleteObject(hbmScreen);
    DeleteDC(hdcMemDC);
    ReleaseDC(NULL, hdcScreen);
}

int main() {
    int interval = 500; // Интервал между скриншотами в миллисекундах
    int count = 5; // Количество скриншотов

    for (int i = 0; i < count; i++) {
        char filename[100];
        sprintf_s(filename, sizeof(filename), "screenshot%d.bmp", i);

        captureScreenshot(filename);
        Sleep(interval);
    }

    return 0;
}