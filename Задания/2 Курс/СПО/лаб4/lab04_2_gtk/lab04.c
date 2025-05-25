#include "lab04_sqlite.h"

#include <gtk/gtk.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define UI_FILE "lab04.glade"

enum
{
    BOOK_ID = 0,
    NAME,
    ANNOTATION,
    NUM_PAGES,
    ISBN,
    AUTH_ID,
    AUTH,
    PUB_ID,
    PUB
};

struct MainWindowObjects
{
    GtkWindow *main_window;
    GtkTreeView *treeview;
    GtkListStore *liststore;
    GtkAdjustment *adjustment;
    GtkTreeViewColumn *column_book_id;
    GtkTreeViewColumn *column_name;
    GtkTreeViewColumn *column_annotation;
    GtkTreeViewColumn *column_ISBN;
    GtkTreeViewColumn *column_author_id;
    GtkTreeViewColumn *column_publishing_id;
    GtkTextView *lbl_name;
    GtkTextView *lbl_annotation;
    GtkTextView *lbl_num_pages;
    GtkTextView *lbl_ISBN;
    GtkTextView *lbl_author;
    GtkTextView *lbl_publishing;
} mainWindowObjects;

int callback(void *not_used, int argc, char **argv, char **col_names)
{
    GtkTreeIter iter;
    
    if (argc == 9)
    {
        gtk_list_store_append(GTK_LIST_STORE(mainWindowObjects.liststore), &iter);
        gtk_list_store_set(GTK_LIST_STORE(mainWindowObjects.liststore), &iter, BOOK_ID,
                           atoi(argv[BOOK_ID]), NAME, argv[NAME], ANNOTATION, argv[ANNOTATION], NUM_PAGES, atoi(argv[NUM_PAGES]), ISBN, argv[ISBN],
                           AUTH_ID, atoi(argv[AUTH_ID]), AUTH, argv[AUTH], PUB_ID, atoi(argv[PUB_ID]), PUB, argv[PUB], -1);
    }
    return 0;
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

    mainWindowObjects.column_name =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_name"));

    mainWindowObjects.column_annotation =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_annotation"));
    mainWindowObjects.column_ISBN =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_ISBN"));
    mainWindowObjects.column_book_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_book_id"));
    mainWindowObjects.column_author_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_author_id"));
    mainWindowObjects.column_publishing_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_publishing_id"));
    mainWindowObjects.lbl_name = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_name"));
    mainWindowObjects.lbl_num_pages = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_num_pages"));
    mainWindowObjects.lbl_annotation = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_annotation"));
    mainWindowObjects.lbl_ISBN = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_ISBN"));
    mainWindowObjects.lbl_author = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_author"));
    mainWindowObjects.lbl_publishing = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_publishing"));
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
         
        gint bookid;
        gchar *name;
        gchar *annotation;
        gint num_pages;
        gchar *isbn;
        gint auth_id;
        gint pub_id;
        
        gtk_tree_model_get(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter, BOOK_ID, &bookid,
                           NAME, &name, ANNOTATION, &annotation, NUM_PAGES, &num_pages, ISBN, &isbn, AUTH_ID, &auth_id, PUB_ID, &pub_id, -1);
        sqlite_update(bookid, name, annotation, num_pages, isbn, auth_id, pub_id);
        reader = gtk_tree_model_iter_next(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter);
    }
    gtk_list_store_clear(mainWindowObjects.liststore);
    sqlite_get_data();
}

G_MODULE_EXPORT void on_btn_add_clicked(GtkWidget *button, gpointer data)
{
    int auth_id, pub_id;
    GtkTextIter start, end;
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_name);
    gchar *name, *annotation, *num_pages, *ISBN, *author, *publishing;
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    name = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", name);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_annotation);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    annotation = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", annotation);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_num_pages);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    num_pages = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", num_pages);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_ISBN);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    ISBN = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", ISBN);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_author);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    author= gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", author);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_publishing);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    publishing = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    printf("%s\n", publishing);
    if (!strcmp(author, "Тимура Данил Станиславович")) auth_id = 3;
        else if (!strcmp(author, "Амелин Максим Евгеньевич")) auth_id = 2;
        else auth_id = 1;
    if (!strcmp(publishing, "Махаон")) pub_id = 1;
        else pub_id = 2;
    sqlite_insert(name, annotation, atoi(num_pages), ISBN, auth_id, pub_id);
}

G_MODULE_EXPORT void on_btn_del_clicked(GtkWidget *button, gpointer data)
{
    GList *_list;
	GtkTreeIter iter;
	GtkTreeModel *model;
	GtkTreeSelection *sel;


	sel = gtk_tree_view_get_selection(mainWindowObjects.treeview);

	for(_list = gtk_tree_selection_get_selected_rows(sel, &model); _list; _list = g_list_next(_list))
	{
		GtkTreePath *path = _list->data;
		int book_id;

		gtk_tree_model_get_iter(model, &iter, path);
		gtk_tree_model_get(model, &iter, BOOK_ID, &book_id, -1);
        sqlite_delete(book_id);
	}

	g_list_foreach(_list, (GFunc)gtk_tree_path_free, NULL);
	g_list_free(_list);
}

G_MODULE_EXPORT void on_annotation_edited(GtkCellRendererText *renderer, gchar *path,
                                                         gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, ANNOTATION, new_text, -1);
    }
}

G_MODULE_EXPORT void on_ISBN_edited(GtkCellRendererText *renderer, gchar *path,
                                                         gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, ISBN, new_text, -1);
    }
}

G_MODULE_EXPORT void on_num_pages_edited(GtkCellRendererText *renderer, gchar *path,
                                                         gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, NUM_PAGES, new_text, -1);
    }
}

G_MODULE_EXPORT void on_name_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, NAME, new_text, -1);
    }
}

G_MODULE_EXPORT void on_author_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        int id;
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (!strcmp(new_text, "Тимура Данил Станиславович")) id = 1;
        else if (!strcmp(new_text, "Амелин Максим Евгеньевич")) id = 2;
        else id = 3;
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, AUTH, new_text, AUTH_ID, id, -1);
    }
}

G_MODULE_EXPORT void on_publishing_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        int id;
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (!strcmp(new_text, "Махаон")) id = 1;
        else id = 2;
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, PUB, new_text, PUB_ID, id, -1);
    }
}

G_MODULE_EXPORT void on_show_hidden_toggled(GtkToggleButton *button, gpointer data)
{
    gboolean visible = gtk_toggle_button_get_active(button);
    gtk_tree_view_column_set_visible(mainWindowObjects.column_book_id, visible);
    gtk_tree_view_column_set_visible(mainWindowObjects.column_author_id, visible);
    gtk_tree_view_column_set_visible(mainWindowObjects.column_publishing_id, visible);
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
