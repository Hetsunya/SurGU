/*Эта программа создает скриншот всего экрана и сохраняет его в файл. 
Функция CaptureScreen принимает имя файла для сохранения скриншота, создает контекст устройства для всего экрана, копирует экран в битовую карту, и сохраняет е
*/

#include <windows.h>

int CaptureScreen(char* filename)
{
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
