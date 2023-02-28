import logging
import sqlite3
from typing import Union, Tuple, List


class Database:
    databases = {}

    def __init__(self, path: str, name: str, logger: logging.Logger):
        self.path: str = path
        self.name: str = name
        self.logger: logging.Logger = logger
        self.columns = {table: self.get_columns(table) for table in self.get_tables()}

        if name in self.databases:
            raise Exception(f"Database with name {name} already exists!")

        self.databases[name] = self

    @staticmethod
    def get_database_by_name(name: str) -> "Database":
        if name not in Database.databases:
            raise Exception(f"No database named {name}!")
        return Database.databases[name]

    def get_tables(self) -> List[str]:
        with sqlite3.connect(self.path) as database:
            return [table for table in database.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone()]

    def get_columns(self, table: str) -> List[str]:
        with sqlite3.connect(self.path) as database:
            cursor = database.execute(f"SELECT * FROM {table}")
            return [description[0] for description in cursor.description]

    def create_table(self, table: str, columns: dict, if_not_exist=True):
        with sqlite3.connect(self.path) as database:
            columns_str = ("".join([f"{val_name} {val_type}, " for val_name, val_type in columns.items()]))[:-2]
            database.execute(f"CREATE TABLE {'IF NOT EXISTS' if if_not_exist else ''} {table} ({columns_str})")

        table_columns = self.get_columns(table)
        query_columns = list(columns.keys())
        if query_columns != table_columns:
            for column in query_columns:
                if column not in table_columns:
                    self.add_column(table, column, columns[column])

            for column in table_columns:
                if column not in query_columns:
                    self.remove_column(table, column)

    def drop_table(self, table: str):
        with sqlite3.connect(self.path) as database:
            database.execute(f"DROP TABLE {table}")

    def add_column(self, table: str, column_name: str, column_definition: str):
        with sqlite3.connect(self.path) as database:
            database.execute(f"ALTER TABLE {table} ADD {column_name} {column_definition}")

    def remove_column(self, table: str, column_name: str):
        with sqlite3.connect(self.path) as database:
            database.execute(f"ALTER TABLE {table} DROP COLUMN {column_name}")

    def insert(self, table: str, entries: list):
        with sqlite3.connect(self.path) as database:
            val_list = self.columns[table]
            val_list.sort()
            filtered_entries = []
            err_str = ""
            correct_str = "".join([f"{val}, " for val in val_list])[:-2]
            for entry in entries:
                keys = list(entry.keys())
                keys.sort()
                if keys == val_list:
                    filtered_entries.append(entry)
                    continue

                for key, value in entry.items():
                    err_str += f"{key}={value}\n"
                err_str = err_str[:-1] + ", \n\n"

            if err_str:
                self.logger.warning(f"Following entries cannot be inserted because of missing / incorrect fields:\n{err_str}Correct fields are: {correct_str}")

            if not filtered_entries:
                return

            for entry in filtered_entries:
                filtered_entries[filtered_entries.index(entry)] = {key: entry[key] for key in val_list}

            val_str = "("
            for val in val_list:
                val_str += f"{val}, "
            val_str = val_str[:-2] + ")"

            entry_str = ""
            final_dict = {}
            for index, entry in enumerate(filtered_entries):
                entry_str += "("
                for key, value in entry.items():
                    entry_str += f":{key}{index}, "
                    final_dict[key + str(index)] = value
                entry_str = entry_str[:-2] + "), "
            entry_str = entry_str[:-2]

            database.execute(f"INSERT INTO {table} {val_str} VALUES {entry_str}", final_dict)

    def delete(self, table: str, var_str: str, var_dict: dict):
        with sqlite3.connect(self.path) as database:
            database.execute(f"DELETE FROM {table} WHERE {var_str}", var_dict)

    def update(self, table: str, var_str: str, var_dict: dict, updated: dict):
        with sqlite3.connect(self.path) as database:
            set_str = ("".join([f"{var}=:set_{var}, " for var in updated.keys()]))[:-2]
            set_var_dict = var_dict
            for var, val in updated.items():
                set_var_dict[f"set_{var}"] = val
            database.execute(f"UPDATE {table} SET {set_str} WHERE {var_str}", set_var_dict)

    def fetch(self, table: str, var_str: str, var_dict: dict, columns: str = "*", fetchall: bool = True) -> Union[Tuple, List]:
        with sqlite3.connect(self.path) as database:
            if fetchall:
                return database.execute(f"SELECT {columns} FROM {table} WHERE {var_str}", var_dict).fetchall()
            return database.execute(f"SELECT {columns} FROM {table} WHERE {var_str}", var_dict).fetchone()

    def check_if_exists(self, table: str, var_str: str, var_dict: dict) -> bool:
        return bool(self.fetch(table, var_str, var_dict))


class NameException(Exception):
    def __init__(self, message="Invalid name!"):
        super().__init__(message)
