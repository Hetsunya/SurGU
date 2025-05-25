#include <gtk/gtk.h>

// Обработчик события "клик мыши" по кнопке
void on_button_clicked(GtkWidget *widget, gpointer data)
{
    g_print("Кнопка нажата\n");
}

int main(int argc, char *argv[])
{
    GtkWidget *window;
    GtkWidget *button;
    GtkWidget *grid;

    // Инициализация GTK
    gtk_init(&argc, &argv);

    // Создание окна
    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Простое приложение");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);

    // Создание сетки для размещения элементов
    grid = gtk_grid_new();
    gtk_container_add(GTK_CONTAINER(window), grid);

    // Создание кнопки
    button = gtk_button_new_with_label("Нажми меня!");
    gtk_grid_attach(GTK_GRID(grid), button, 0, 0, 1, 1);

    // Привязка обработчика к событию "клик мыши" по кнопке
    g_signal_connect(button, "clicked", G_CALLBACK(on_button_clicked), NULL);

    // Отображение окна и запуск цикла обработки событий
    gtk_widget_show_all(window);
    gtk_main();

    return 0;
}