#include <windows.h>
#include <stdio.h>
#include <time.h>

#pragma comment(lib, "gdi32")

int CaptureScreen(char* filename, int width, int height)
{
    // Создание контекста устройства для всего экрана
    HDC hdcScreen = GetDC(NULL);
    HDC hdcMemDC = CreateCompatibleDC(hdcScreen);

    // Создание битовой карты для копирования экрана
    HBITMAP hbmScreen = CreateCompatibleBitmap(hdcScreen, width, height);
    SelectObject(hdcMemDC, hbmScreen);

    // Копирование экрана в битовую карту
    BitBlt(hdcMemDC, 0, 0, width, height, hdcScreen, 0, 0, SRCCOPY);

    // Сохранение битовой карты в файл
    int result = SaveBitmap(filename, hdcMemDC, hbmScreen);

    // Освобождение ресурсов
    DeleteObject(hbmScreen);
    DeleteDC(hdcMemDC);
    ReleaseDC(NULL, hdcScreen);

    return result;
}

int SaveBitmap(char* filename, HDC hdcMemDC, HBITMAP hbmScreen)
{
    // Сохранение битовой карты в файл
    HANDLE hFile = CreateFile(filename, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return 0;
    }

    BITMAP bmpScreen;
    GetObject(hbmScreen, sizeof(bmpScreen), &bmpScreen);

    BITMAPFILEHEADER bmfHeader;
    bmfHeader.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    bmfHeader.bfSize = bmfHeader.bfOffBits + bmpScreen.bmWidthBytes * bmpScreen.bmHeight;
    bmfHeader.bfType = 0x4d42;

    BITMAPINFOHEADER bi;
    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = bmpScreen.bmWidth;
    bi.biHeight = bmpScreen.bmHeight;
    bi.biPlanes = 1;
    bi.biBitCount = 24;
    bi.biCompression = BI_RGB;
    bi.biSizeImage = 0;
    bi.biXPelsPerMeter = 0;
    bi.biYPelsPerMeter = 0;
    bi.biClrUsed = 0;
    bi.biClrImportant = 0;

    DWORD dwBytesWritten = 0;
    WriteFile(hFile, (LPSTR)&bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);
    WriteFile(hFile, (LPSTR)&bi, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);
    WriteFile(hFile, (LPSTR)bmpScreen.bmBits, bmpScreen.bmWidthBytes * bmpScreen.bmHeight, &dwBytesWritten, NULL);

    CloseHandle(hFile);

    return 1;
}

int main()
{
    int width, height, interval;
    char filename[MAX_PATH];
    printf("Введите имя файла для сохранения скриншотов: ");
    scanf("%s", filename);
    printf("Введите ширину скриншота: ");
    scanf("%d", &width);
    printf("Введите высоту скриншота: ");
    scanf("%d", &height);
    printf("Введите интервал между скриншотами (в секундах): ");
    scanf("%d", &interval);
    printf("Для остановки создания скриншотов нажмите Ctrl+C\n");

// Бесконечный цикл для создания серии скриншотов с заданным интервалом
while (1) {
    // Получение текущего времени для использования в имени файла
    time_t rawtime;
    struct tm* timeinfo;
    time(&rawtime);
    timeinfo = localtime(&rawtime);

    // Создание имени файла в формате "screenshots_YYYYMMDD_HHMMSS.bmp"
    char timestamp[20];
    strftime(timestamp, 20, "%Y%m%d_%H%M%S", timeinfo);
    char* fullname = (char*)malloc(strlen(filename) + 1 + strlen(timestamp) + 4);
    sprintf(fullname, "%s_%s.bmp", filename, timestamp);

    // Создание скриншота и сохранение в файл
    CaptureScreen(fullname, width, height);

    // Ожидание заданного интервала времени перед созданием следующего скриншота
    Sleep(interval * 1000);

    free(fullname);
}

return 0;
}

