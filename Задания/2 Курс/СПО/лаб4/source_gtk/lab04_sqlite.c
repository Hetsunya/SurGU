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
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }

    char *sql = "SELECT \
                  teacher.teacher_id, \
                  teacher.fio, \
                  teacher.date_of_birth, \
                  position.position_id, \
                  position.name,  \
                  department.department_id, \
                  department.name \
              FROM \
                  ((teacher \
              INNER JOIN position ON teacher.position_id = position.position_id) \
              INNER JOIN department ON teacher.department_id = department.department_id);";
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to select data\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_insert(char * fio, char * date, int pos, int dep)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }

    char sql[256];
    sprintf(sql, "INSERT INTO teacher (fio, date_of_birth, position_id, department_id) VALUES ('%s', '%s', %d, %d);", fio, date, pos, dep);
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to select data\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_delete(int teachid)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }

    char sql[256];
    sprintf(sql, "DELETE FROM teacher WHERE teacher_id = %d;", teachid);
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to select data\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_update(int teachid, char *fio, char* date, int pos_id, int dep_id)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }


    char sql_comp[255];
    sprintf(sql_comp, "UPDATE teacher SET fio = '%s', date_of_birth = '%s', position_id = %d, department_id = %d WHERE teacher_id = %d;", fio, date, pos_id,dep_id, teachid);
    rc = sqlite3_exec(db, sql_comp, NULL, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to update data in components\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}
