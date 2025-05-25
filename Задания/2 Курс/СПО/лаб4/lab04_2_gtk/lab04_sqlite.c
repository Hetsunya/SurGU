#include <sqlite3.h>
#include <stdio.h>
#include "lab04_sqlite.h"

int callback(void *, int, char **, char **);
void sqlite_get_data()
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        
        sqlite3_close(db);
    }

    char *sql = "SELECT \
                  book.book_id, \
                  book.name, \
                  book.annotation, \
                  book.num_pages, \
                  book.ISBN, \
                  author.author_id, \
                  author.fio,  \
                  publishing.publishing_id, \
                  publishing.name \
              FROM \
                  ((book \
              INNER JOIN author ON book.author_id =  author.author_id) \
              INNER JOIN publishing ON book.publishing_id = publishing.publishing_id);";
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_insert(char *name, char* annotation, int num_pages, char* ISBN, int auth_id, int pub_id)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        
        sqlite3_close(db);
    }

    char sql[256];
    sprintf(sql, "INSERT INTO book (name, annotation, num_pages, ISBN, author_id, publishing_id) VALUES ('%s', '%s', %d, '%s', %d, %d);", name, annotation, num_pages, ISBN, auth_id, pub_id);
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_delete(int bookid)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        
        sqlite3_close(db);
    }

    char sql[256];
    sprintf(sql, "DELETE FROM book WHERE book_id = %d;", bookid);
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_update(int bookid, char *name, char* annotation, int num_pages, char* ISBN, int auth_id, int pub_id)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        
        sqlite3_close(db);
    }


    char sql_comp[255];
    sprintf(sql_comp, "UPDATE book SET name = '%s', annotation = '%s', num_pages = %d, ISBN = '%s', author_id = %d, publishing_id = %d WHERE book_id = %d;", name, annotation, num_pages, ISBN, auth_id, pub_id, bookid);
    rc = sqlite3_exec(db, sql_comp, NULL, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}
