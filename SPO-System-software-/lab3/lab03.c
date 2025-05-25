#include <windows.h>
#define ID_BEEP 1000
#define ID_QUIT 1001
#define ID_TEXT 1002
#define ID_EDIT 1003

const char g_szClassName[] = "myWindowClass";
HWND edit;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    switch (msg)
    {
        case WM_CREATE:
            edit = CreateWindowW(L"Edit", L"You can write text here",
                                 WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL,
                                 15, 15, 300, 200, hwnd, (HMENU)ID_EDIT, NULL, NULL);
            CreateWindowW(L"Button", L"Beep", WS_VISIBLE | WS_CHILD, 20, 250, 80, 25, hwnd,
                          (HMENU)ID_BEEP, NULL, NULL);
            CreateWindowW(L"Button", L"Text", WS_VISIBLE | WS_CHILD, 120, 250, 80, 25, hwnd,
                          (HMENU)ID_TEXT, NULL, NULL);
            CreateWindowW(L"Button", L"Quit", WS_VISIBLE | WS_CHILD, 220, 250, 80, 25, hwnd,
                          (HMENU)ID_QUIT, NULL, NULL);
            break;
        case WM_COMMAND:
            switch (LOWORD(wParam))
            {
                case ID_BEEP:
                    MessageBeep(MB_OK);
                    break;
                case ID_TEXT:;
                    char buff[1024];
                    GetWindowText(edit, buff, 1024);
                    MessageBox(NULL, buff, "Info!", MB_ICONINFORMATION | MB_OK);
                    break;
                case ID_QUIT:
                    PostQuitMessage(0);
                    break;
            }
            break;
        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    WNDCLASSEX wc;
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszMenuName = NULL;
    wc.lpszClassName = g_szClassName;
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc))
    {
        MessageBox(NULL, "Window Registration Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }
    HWND hwnd;
    hwnd =
        CreateWindowEx(WS_EX_CLIENTEDGE, g_szClassName, "Hello from WinAPI!", WS_OVERLAPPEDWINDOW,
                       CW_USEDEFAULT, CW_USEDEFAULT, 350, 330, NULL, NULL, hInstance, NULL);
    if (hwnd == NULL)
    {
        MessageBox(NULL, "Window Creation Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG Msg;
    while (GetMessage(&Msg, NULL, 0, 0) > 0)
    {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }
    return Msg.wParam;
}
