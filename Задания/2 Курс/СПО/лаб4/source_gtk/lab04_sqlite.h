#ifndef LAB04_SQLITE_H
#define LAB04_SQLITE_H

#define DB_FILE "lab4.db"

void sqlite_insert(char * fio, char * date, int pos, int dep);
void sqlite_delete(int);
void sqlite_get_data();
void sqlite_update(int compid, char *compname, char* price, int pos_id, int dep_id);

#endif
