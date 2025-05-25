#include "lab04_sqlite.h"

#include <gtk/gtk.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define UI_FILE "lab04.glade"

enum
{
    COUPLE_ID = 0,
    BEGIN,
    END,
    DIS_ID,
    DISCIPLINE,
    WD_ID,
    WEEKDAY
};

struct MainWindowObjects
{
    GtkWindow *main_window;
    GtkTreeView *treeview;
    GtkListStore *liststore;
    GtkAdjustment *adjustment;
    GtkTreeViewColumn *column_weekday_id;
    GtkTreeViewColumn *column_weekday;
    GtkTreeViewColumn *column_couple;
    GtkTreeViewColumn *column_discipline_id;
    GtkTreeViewColumn *column_department;
    GtkTextView *lbl_wd;
    GtkTextView *lbl_couple_№;
    GtkTextView *lbl_discipline;
} mainWindowObjects;

int callback(void *not_used, int argc, char **argv, char **col_names)
{
    GtkTreeIter iter;
    
    if (argc == 7)
    {
        gtk_list_store_append(GTK_LIST_STORE(mainWindowObjects.liststore), &iter);
        gtk_list_store_set(GTK_LIST_STORE(mainWindowObjects.liststore), &iter, COUPLE_ID,
                           atoi(argv[COUPLE_ID]), BEGIN, END, argv[BEGIN], DISCIPLINE, argv[DISCIPLINE],
                           WD_ID, atoi(argv[WD_ID]), WEEKDAY, argv[WEEKDAY], DIS_ID, atoi(argv[DIS_ID]), -1);
    }
    return 0;
}

void date_cell_data_func(GtkTreeViewColumn *col, GtkCellRenderer *renderer, GtkTreeModel *model,
                          GtkTreeIter *iter, gpointer user_data)
{
    /*gchar buf[30];
    gtk_tree_model_get(model, iter, DISCIPLINE, buf, -1);
    g_object_set(renderer, "text", buf, NULL);*/
}

void weekday_cell_data_func(GtkTreeViewColumn *col, GtkCellRenderer *renderer, GtkTreeModel *model,
                          GtkTreeIter *iter, gpointer user_data)
{
    /*gchar buf[100];
    gtk_tree_model_get(model, iter, BEGIN, buf, -1);
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

    mainWindowObjects.column_weekday =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_weekday"));
    GtkCellRenderer *cell = GTK_CELL_RENDERER(gtk_builder_get_object(builder, "weekday"));
    gtk_tree_view_column_set_cell_data_func(mainWindowObjects.column_weekday, cell,
                                            weekday_cell_data_func, NULL, NULL);

    mainWindowObjects.column_couple =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_date_of_birth"));
    GtkCellRenderer *cell1 = GTK_CELL_RENDERER(gtk_builder_get_object(builder, "date_of_birth"));
    gtk_tree_view_column_set_cell_data_func(mainWindowObjects.column_couple, cell1,
                                            date_cell_data_func, NULL, NULL);

    mainWindowObjects.column_weekday_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_weekday_id"));
    mainWindowObjects.column_discipline_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_weekday_id"));
    mainWindowObjects.lbl_wd = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_weekday"));
    mainWindowObjects.lbl_couple_№ = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_couple_№"));
    mainWindowObjects.lbl_discipline = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_discipline"));
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
        gchar *weekday;
       
        gchar *date;
        gint pos_id;
        gint dep_id;
        
        // gtk_tree_model_get(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter, WEEKDAY, &weekday,  COUPLE_ID, &coupleid,
        //                    BEGIN, &begin, END, &end,  DISCIPLINE, &discipline, DIS_ID, &dis_id, WD_ID, &wd_id, -1);
        sqlite_update(teachid, weekday, date, pos_id, dep_id);
        reader = gtk_tree_model_iter_next(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter);
    }
    gtk_list_store_clear(mainWindowObjects.liststore);
    sqlite_get_data();
}

G_MODULE_EXPORT void on_btn_add_clicked(GtkWidget *button, gpointer data)
{
    int pos_id, dep_id;
    GtkTextIter start, end;
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_wd);
    gchar *weekday, *date, *position, *department;
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    weekday = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", weekday);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_couple_№);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    date = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", date);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_discipline);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    position = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", position);
    if (!strcmp(department, "ПМ")) dep_id = 3;
        else if (!strcmp(department, "АИКС")) dep_id = 2;
        else dep_id = 1;
    if (!strcmp(department, "Профессор")) pos_id = 3;
        else if (!strcmp(department, "Доцент")) pos_id = 2;
        else pos_id = 1;
    sqlite_insert(weekday, date, pos_id, dep_id);
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
		gtk_tree_model_get(model, &iter, COUPLE_ID, &teacher_id, -1);
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
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, DISCIPLINE, new_text, -1);
    }
}

G_MODULE_EXPORT void on_weekday_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, BEGIN, new_text, -1);
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
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, WEEKDAY, new_text, WD_ID, id, -1);
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
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, DISCIPLINE, new_text, DIS_ID, id, -1);
    }
}

G_MODULE_EXPORT void on_show_hidden_toggled(GtkToggleButton *button, gpointer data)
{
    // gboolean visible = gtk_toggle_button_get_active(button);
    // gtk_tree_view_column_set_visible(mainWindowObjects.column_weekday_id, visible);
    // gtk_tree_view_column_set_visible(mainWindowObjects.column_discipline_id, visible);
    // gtk_tree_view_column_set_visible(mainWindowObjects.column_department_id, visible); ВОТ С ЭТИМ ПРОБЛЕМЫ
}

G_MODULE_EXPORT void on_btnabout_clicked(GtkButton *button, gpointer data)
{
    GtkWidget *dialog = gtk_dialog_new_with_buttons(
        "О программе", mainWindowObjects.main_window,
        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT, "_OK", GTK_RESPONSE_NONE, NULL);
    GtkWidget *content_area = gtk_dialog_get_content_area(GTK_DIALOG(dialog));
    gtk_container_set_border_width(GTK_CONTAINER(content_area), 15);
    GtkWidget *label = gtk_label_new("\nЭто как пример из 4 лабораторный. Только больше\n");
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
