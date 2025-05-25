#ifndef LAB04_SQLITE_H
#define LAB04_SQLITE_H

#define DB_FILE "lab4_2.db"

void sqlite_insert(char *name, char* annotation, int num_pages, char* ISBN, int auth_id, int pub_id);
void sqlite_delete(int);
void sqlite_get_data();
void sqlite_update(int bookid, char*name, char*annotation, int num_pages, char*, int, int);

#endif
