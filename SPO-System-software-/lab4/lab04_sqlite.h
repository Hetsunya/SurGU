#ifndef LAB04_SQLITE_H
#define LAB04_SQLITE_H

#define DB_FILE "lab4.db"

void sqlite_insert(int №_couple, char * begin, char * end, int dis, int wd);
void sqlite_delete(int);
void sqlite_get_data();
void sqlite_update(int №_couple, char * begin, char * end, int dis, int wd, int coupleid);

#endif
