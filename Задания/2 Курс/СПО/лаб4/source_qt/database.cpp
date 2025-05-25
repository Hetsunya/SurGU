#include "database.h"

DataBase::DataBase(QObject *parent) : QObject(parent)
{
}

DataBase::~DataBase()
{
}

void DataBase::connectToDataBase()
{
    if (QFile(DATABASE_NAME).exists())
    {
        this->openDataBase();
    }
}

bool DataBase::openDataBase()
{
    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setHostName(DATABASE_HOSTNAME);
    db.setDatabaseName(DATABASE_NAME);
    if (db.open())
    {
        return true;
    }
    else
    {
        qDebug() << "Cannot open database: " << db.lastError().text();
        db.close();
        return false;
    }
}

void DataBase::closeDataBase()
{
    db.close();
}
