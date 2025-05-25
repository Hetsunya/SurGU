#include "lab04_sqlite.h"

#include <gtk/gtk.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define UI_FILE "lab04.glade"

enum
{
    TEACH_ID = 0,
    FIO,
    DATE,
    POS_ID,
    POS,
    DEP_ID,
    DEP
};

struct MainWindowObjects
{
    GtkWindow *main_window;
    GtkTreeView *treeview;
    GtkListStore *liststore;
    GtkAdjustment *adjustment;
    GtkTreeViewColumn *column_teach_id;
    GtkTreeViewColumn *column_fio;
    GtkTreeViewColumn *column_date;
    GtkTreeViewColumn *column_position_id;
    GtkTreeViewColumn *column_department_id;
    GtkTextView *lbl_fio;
    GtkTextView *lbl_date;
    GtkTextView *lbl_position;
    GtkTextView *lbl_department;
} mainWindowObjects;

int callback(void *not_used, int argc, char **argv, char **col_names)
{
    GtkTreeIter iter;
    
    if (argc == 7)
    {
        gtk_list_store_append(GTK_LIST_STORE(mainWindowObjects.liststore), &iter);
        gtk_list_store_set(GTK_LIST_STORE(mainWindowObjects.liststore), &iter, TEACH_ID,
                           atoi(argv[TEACH_ID]), FIO, argv[FIO], DATE, argv[DATE],
                           POS_ID, atoi(argv[POS_ID]), POS, argv[POS], DEP_ID, atoi(argv[DEP_ID]), DEP, argv[DEP], -1);
    }
    return 0;
}

void date_cell_data_func(GtkTreeViewColumn *col, GtkCellRenderer *renderer, GtkTreeModel *model,
                          GtkTreeIter *iter, gpointer user_data)
{
    /*gchar buf[30];
    gtk_tree_model_get(model, iter, DATE, buf, -1);
    g_object_set(renderer, "text", buf, NULL);*/
}

void fio_cell_data_func(GtkTreeViewColumn *col, GtkCellRenderer *renderer, GtkTreeModel *model,
                          GtkTreeIter *iter, gpointer user_data)
{
    /*gchar buf[100];
    gtk_tree_model_get(model, iter, FIO, buf, -1);
    printf("%s", buf);
    g_object_set(renderer, "text", buf, NULL);*/
}

int main(int argc, char **argv)
{
    GtkBuilder *builder;
    GError *error = NULL;
    gtk_init(&argc, &argv);

    builder = gtk_builder_new();

    if (!gtk_builder_add_from_file(builder, UI_FILE, &error))
    {
        g_warning("%s\n", error->message);
        g_free(error);
        return (1);
    }

    mainWindowObjects.main_window = GTK_WINDOW(gtk_builder_get_object(builder, "main_window"));
    mainWindowObjects.treeview =
        GTK_TREE_VIEW(gtk_builder_get_object(builder, "treeview_components"));
    mainWindowObjects.liststore =
        GTK_LIST_STORE(gtk_builder_get_object(builder, "liststore_components"));

    mainWindowObjects.column_fio =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_fio"));
    GtkCellRenderer *cell = GTK_CELL_RENDERER(gtk_builder_get_object(builder, "fio"));
    gtk_tree_view_column_set_cell_data_func(mainWindowObjects.column_fio, cell,
                                            fio_cell_data_func, NULL, NULL);

    mainWindowObjects.column_date =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_date_of_birth"));
    GtkCellRenderer *cell1 = GTK_CELL_RENDERER(gtk_builder_get_object(builder, "date_of_birth"));
    gtk_tree_view_column_set_cell_data_func(mainWindowObjects.column_date, cell1,
                                            date_cell_data_func, NULL, NULL);

    mainWindowObjects.column_teach_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_teacher_id"));
    mainWindowObjects.column_position_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_position_id"));
    mainWindowObjects.column_department_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_department_id"));
    mainWindowObjects.lbl_fio = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_fio"));
    mainWindowObjects.lbl_date = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_date"));
    mainWindowObjects.lbl_position = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_position"));
    mainWindowObjects.lbl_department = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_department"));
    gtk_builder_connect_signals(builder, &mainWindowObjects);
    
    g_object_unref(G_OBJECT(builder));
    gtk_widget_show_all(GTK_WIDGET(mainWindowObjects.main_window));

    sqlite_get_data();

    gtk_main();
}

G_MODULE_EXPORT void on_btnsave_clicked(GtkWidget *button, gpointer data)
{
    GtkTreeIter iter;
    gboolean reader =
        gtk_tree_model_get_iter_first(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter);
    while (reader)
    {
         
        gint teachid;
        gchar *fio;
       
        gchar *date;
        gint pos_id;
        gint dep_id;
        
        gtk_tree_model_get(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter, TEACH_ID, &teachid,
                           FIO, &fio, DATE, &date, POS_ID, &pos_id, DEP_ID, &dep_id, -1);
        sqlite_update(teachid, fio, date, pos_id, dep_id);
        reader = gtk_tree_model_iter_next(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter);
    }
    gtk_list_store_clear(mainWindowObjects.liststore);
    sqlite_get_data();
}

G_MODULE_EXPORT void on_btn_add_clicked(GtkWidget *button, gpointer data)
{
    int pos_id, dep_id;
    GtkTextIter start, end;
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_fio);
    gchar *fio, *date, *position, *department;
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    fio = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", fio);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_date);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    date = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", date);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_position);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    position = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", position);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_department);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    department = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", department);
    if (!strcmp(department, "ПМ")) dep_id = 3;
        else if (!strcmp(department, "АИКС")) dep_id = 2;
        else dep_id = 1;
    if (!strcmp(department, "Профессор")) pos_id = 3;
        else if (!strcmp(department, "Доцент")) pos_id = 2;
        else pos_id = 1;
    sqlite_insert(fio, date, pos_id, dep_id);
}

G_MODULE_EXPORT void on_btn_del_clicked(GtkWidget *button, gpointer data)
{
    GList *_list;
	GtkTreeIter iter;
	GtkTreeModel *model;
	GtkTreeSelection *sel;


	sel = gtk_tree_view_get_selection(mainWindowObjects.treeview);

	// create local selection
	for(_list = gtk_tree_selection_get_selected_rows(sel, &model); _list; _list = g_list_next(_list))
	{
		GtkTreePath *path = _list->data;
		int teacher_id;

		gtk_tree_model_get_iter(model, &iter, path);
		gtk_tree_model_get(model, &iter, TEACH_ID, &teacher_id, -1);
        sqlite_delete(teacher_id);
	}

	g_list_foreach(_list, (GFunc)gtk_tree_path_free, NULL);
	g_list_free(_list);
}

G_MODULE_EXPORT void on_date_of_birth_edited(GtkCellRendererText *renderer, gchar *path,
                                                         gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, DATE, new_text, -1);
    }
}

G_MODULE_EXPORT void on_fio_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, FIO, new_text, -1);
    }
}

G_MODULE_EXPORT void on_position_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        int id;
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (!strcmp(new_text, "Профессор")) id = 3;
        else if (!strcmp(new_text, "Доцент")) id = 2;
        else id = 1;
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, POS, new_text, POS_ID, id, -1);
    }
}

G_MODULE_EXPORT void on_department_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        int id;
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (!strcmp(new_text, "ПМ")) id = 3;
        else if (!strcmp(new_text, "АИКС")) id = 2;
        else id = 1;
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, DEP, new_text, DEP_ID, id, -1);
    }
}

G_MODULE_EXPORT void on_show_hidden_toggled(GtkToggleButton *button, gpointer data)
{
    gboolean visible = gtk_toggle_button_get_active(button);
    gtk_tree_view_column_set_visible(mainWindowObjects.column_teach_id, visible);
    gtk_tree_view_column_set_visible(mainWindowObjects.column_position_id, visible);
    gtk_tree_view_column_set_visible(mainWindowObjects.column_department_id, visible);
}

G_MODULE_EXPORT void on_btnabout_clicked(GtkButton *button, gpointer data)
{
    GtkWidget *dialog = gtk_dialog_new_with_buttons(
        "О программе", mainWindowObjects.main_window,
        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT, "_OK", GTK_RESPONSE_NONE, NULL);
    GtkWidget *content_area = gtk_dialog_get_content_area(GTK_DIALOG(dialog));
    gtk_container_set_border_width(GTK_CONTAINER(content_area), 15);
    GtkWidget *label = gtk_label_new("\nЭто как ваша лабораторная работа №4, только меньше\n");
    gtk_container_add(GTK_CONTAINER(content_area), label);
    gtk_widget_show(label);
    gtk_dialog_run(GTK_DIALOG(dialog));
    gtk_widget_destroy(dialog);
}

G_MODULE_EXPORT void on_window_destroy(GtkWidget *window, gpointer data)
{
    gtk_main_quit();
}

G_MODULE_EXPORT void on_btnexit_clicked(GtkWidget *window, gpointer data)
{
    gtk_main_quit();
}
