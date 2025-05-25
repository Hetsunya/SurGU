#include <windows.h>
#include <string.h>
#include <stdio.h>


struct List{
    const CHAR *letter;
    struct List *next;
};

void CreateList(List * start, char buffer[], int size)
{
    int i = 0;
    List *q;
    q = start;
    for (i = 0; i < size; i++)
    {
        List *p = (List *)malloc(sizeof(List));
       // q = (List *)malloc(sizeof(List));
        q->next = p;
        q->letter = &buffer[i];
        p->next = NULL;
        q = p;
    }

}

/*void PrintList(List * s)
{
	while (s->next != NULL)
    {
        //TextOut();
		s = s->next;
	}
}*/
/*  Declare Windows procedure  */
LRESULT CALLBACK WindowProcedure (HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    HDC         hdc;
    PAINTSTRUCT ps;
    RECT        rect;
    static char *str = NULL;
    List *start = (List *)malloc(sizeof(List));
    int size, i = 0;
    switch (message)
    {
        case WM_CREATE:
         {
                 str = (char *)(((LPCREATESTRUCT)lParam)->lpCreateParams);
                 FILE *fp;
                 fp = fopen("text.txt","r");
                 fseek(fp,0,SEEK_END);
                 size = ftell(fp);
                 rewind(fp);
                 char buffer[size];
                 fread(buffer, sizeof(char), size, fp);
                 CreateList(start, buffer, size);

                 break;
             }
        case WM_DESTROY:
        {
            PostQuitMessage (0);       /* send a WM_QUIT to the message queue */
            break;
        }
        case WM_PAINT:
        {
            hdc = BeginPaint(hwnd, &ps);
            GetClientRect(hwnd, &rect);
            TEXTMETRIC tm;
            GetTextMetrics(hdc, &tm);
            List *s;
            s = start;
            i=0;
            // while (s->next != NULL)
            // {
            //     TextOut(hdc, ++i*tm.tmAveCharWidth, 1, s->letter, 1);
            //     TextOut(hdc, ++i*tm.tmAveCharWidth, 1, s->next->letter, 1);
            // }

            EndPaint(hwnd, &ps);
            break;
        }

        default:
            return DefWindowProc (hwnd, message, wParam, lParam);
    }

    return 0;
}