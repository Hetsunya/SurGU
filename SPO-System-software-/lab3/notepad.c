#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_TITLE_LENGTH 50
#define MAX_TEXT_LENGTH 1000
#define MAX_NOTES 100

struct Note {
    char title[MAX_TITLE_LENGTH];
    char text[MAX_TEXT_LENGTH];
};

struct Notebook {
    struct Note notes[MAX_NOTES];
    int num_notes;
};

// Глобальные переменные
HWND hwndEditTitle, hwndEditText;
HINSTANCE hInstance;
struct Notebook notebook;

void update_title(HWND hwnd) {
    char title[MAX_TITLE_LENGTH + 20];
    GetWindowText(hwndEditTitle, title, MAX_TITLE_LENGTH);
    sprintf(title + strlen(title), " - %d notes", notebook.num_notes);
    SetWindowText(hwnd, title);
}

void add_note() {
    if (notebook.num_notes >= MAX_NOTES) {
        MessageBox(NULL, "Notebook is full", "Error", MB_ICONERROR);
        return;
    }

    struct Note *note = &notebook.notes[notebook.num_notes];
    notebook.num_notes++;

    memset(note->title, 0, MAX_TITLE_LENGTH);
    memset(note->text, 0, MAX_TEXT_LENGTH);

    update_title(GetParent(hwndEditTitle));
}

void edit_note() {
    int index = SendMessage(hwndEditTitle, EM_GETSEL, 0, 0);
    if (index == -1) {
        MessageBox(NULL, "No note selected", "Error", MB_ICONERROR);
        return;
    }

    index = LOWORD(index);
    struct Note *note = &notebook.notes[index];

    GetWindowText(hwndEditText, note->text, MAX_TEXT_LENGTH);
    GetWindowText(hwndEditTitle, note->title, MAX_TITLE_LENGTH);
}

void delete_note() {
    int index = SendMessage(hwndEditTitle, EM_GETSEL, 0, 0);
    if (index == -1) {
        MessageBox(NULL, "No note selected", "Error", MB_ICONERROR);
        return;
    }

    index = LOWORD(index);
    notebook.num_notes--;

    // Сдвигаем все заметки на одну позицию влево, чтобы удалить выбранную заметку
    for (int i = index; i < notebook.num_notes; i++) {
        memcpy(&notebook.notes[i], &notebook.notes[i + 1], sizeof(struct Note));
    }

    SetWindowText(hwndEditTitle, "");
    SetWindowText(hwndEditText, "");
    update_title(GetParent(hwndEditTitle));
}

void view_note() {
    int index = SendMessage(hwndEditTitle, EM_GETSEL, 0, 0);
    if (index == -1) {
        MessageBox(NULL, "No note selected", "Error", MB_ICONERROR);
        return;
    }

    index = LOWORD(index);
    struct Note *note = &notebook.notes[index];

    SetWindowText(hwndEditText, note->text);
}

void list_notes() {
    char text[MAX_TEXT_LENGTH] = "";

    for (int i = 0; i < notebook.num_notes; i++) {
        char buffer[MAX_TEXT_LENGTH];
        sprintf(buffer, "%d. %s\n", i + 1, notebook.notes[i].title);
        strcat(text, buffer);
    }

    MessageBox(NULL, text, "Notes", MB_ICONINFORMATION);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE: {
            hwndEditTitle = CreateWindowEx(WS_EX_CLIENTEDGE, "EDIT", "",
                                           WS_CHILD | WS_VISIBLE