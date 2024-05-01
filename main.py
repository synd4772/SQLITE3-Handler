from __future__ import annotations
from sqlite3 import *
from sqlite3 import Error, Connection
from os import *


def object_check(func):
  def wrapper(*args, **kwargs):
    result = func(*args, **kwargs)
    return result
  return wrapper

class SQLHandler(object):
  def __init__(file_name:str = 'data.db'):
    self.connection = self.create_connection(file_name)

  def create_connection(self, file_name:str):
    connection = None
    try:
        connection = connect(path)
        return connection
    except Error as e:
        print(f"Error: {e}")

  def execute_query(self, query):
    cursor = self.connection.cursor()
    result = None
    try:
        cursor.execute(query)
        cursor.commit()
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: {e}")
  
class SQLHDatabase(SQLHandler):
  def __init__(self, file_name:str = 'data.db'):
    super().__init__(file_name = file_name)
    self.tables = None

  def add_table(self, table:SQLHTable):
    query_template = f"CREATE TABLE IF NOT EXISTS {table.name}("
    columns = table.get_columns()
    columns_template_strings = list()
    for column in columns:
      temp_str.append(f"{column.name} {column.type}{' PRIMARY KEY' if column.primary_key else ""} {column.constraint}")
    columns_template_strings = ",".join(columns_template_strings)
    query_template += columns_template_strings + ");"
    super().execute_query(query_template)

    records = table.get_records()
    if records is not None:
      for index, record in enumerate(records):
        tmp_list = list()
        for second_record in records:
          tmp_list.append(second_record[index])
        self.insert_table(table, tmp_list)
      
  def insert_table(self, table:SQLHTable, records):
    if table in self.tables:
      columns = table.get_columns()
      columns_names = [column.name for column in columns]
      query_template = f"INSERT INTO {table.name}({','.join(columns_names)}) VALUES({",".join(records)});"
      super().execute_query(query=query_template)

  def alter_table(self, table:SQLHTable, column:SQLHColumn, method:str = 'ADD'):
    if table in self.tables:
      if method.upper() == 'ADD':
        query_template = f"ALTER TABLE {table.name} ADD {column.name} {column.type} {column.constraint}"
        super().execute_query(query_template)

  def change_record_table(self, table, condition:list):
    """condition = [set_column, set_value, where_column, where_value]"""
    query_template = f"UPDATE {table} SET {condition[0]} = {condition[1]} WHERE {condition[2]} like {condition[3]}"
    super().execute_query(query_template)

  def column_append(self, table, column):
    if table in self.tables and column in table.get_columns():
      table_primary_key = table.primary_key()
      primary_key_records = table.get_records_by_column(table_primary_key)
      column_records = table.get_records_by_column(column)
      self.alter_table(table = table, column = column, method = "add")
      if column_records is not None:
        for index, column_record in enumerate(column_records):
          condition = [column.name, column_record, table_primary_key, primary_key_records[index]]
          self.change_record_table(table=table, condition=condition)


class SQLHTable(object):
  def __init__(self, name:str, row_id:bool):
    self.name = name
    self.columns = []
    self.primary_key = None
    self.live = False
    self.database_object:SQLHDatabase = None
    self.row_id = SQLHColumn(name="id", type="INTEGER", constraint="NOT NULL", primary_key=True) if row_id else None

  def add_column(self, column:SQLHColumn, records:list):
    primary_key_dict = self.get_column_dict(self.primary_key)
    primary_key_records = primary_key_dict['records']
    self.columns.append({"column_object":column, "records":[(records[index] if len(records) >= len(primary_key_records) else 'NULL') for index, record in enumerate(primary_key_records)]})
    if self.live and self.database_object is not None:
      self.database_object.column_append(self, column)

  def __null_row_add(self):
    for column_dict in self.columns:
      records = column_dict["records"]
      records.append(("NULL" if self.row_id is not column_dict["column_object"] else self.get_records_count + 1))

  def add_record(self, records:list):
    primary_key_records = self.get_column_dict(self.primary_key)["records"] 
    self.__null_row_add()
    for column_dict in self.columns:
      if column_dict['records'][len()]

  @staticmethod
  def __get_something(arg_list:list, key:str):
    if len(arg_list) > 1:
          return_list:list = []
          for item in arg_list:
            return_list.append(item[key])
          return return_list
    else:
      return None

  def get_records(self):
    return self.__get_something(arg_list=self.columns, key="records")

  def get_columns(self):
    return self.__get_something(arg_list=self.columns, key="column_object")

  def get_column_dict(self, column:SQLHColumn):
    if column in self.get_columns():
      for column_dict in self.columns:
        if column_dict["column_object"] is column:
          return column_dict
    return None

  def get_records_count(self):
    primary_key_records = self.get_column_dict(self.primary_key)["records"]
    
    return len(primary_key_records)

class SQLHColumn(object):
  def __init__(self, name:str, type:str, constraint:str, primary_key:bool, foreign_key:SQLHColumn):
    self.name = name
    self.type = type
    self.constraint = constraint
    self.primary_key = primary_key
    self.foreign_key = foreign_key















































# dev_mode = True # стоило бы убрать после завержения, либо поставить значение на False

# def change_parameters(default_parameters:dict, new_parameters:dict):
#   return_parameters = dict(default_parameters)
#   for key, value in return_parameters.items():
#     if key in new_parameters:
#       return_parameters[key] = new_parameters[key]
#   return return_parameters



# class SQLHTable(object):
# #1. логирование действий для дальнейшей фунуции "add_changes" для класса SQLHDatabase
# #2. везде пораставить условие на то, если есть база данных и синхронизация (LIVE_CHANGING) , то делать каждый раз запрос
#   default_parameters = {
#       'ID_ROW':False,
#       'NULL_RECORD':'NULL'
#     }
#   none_record = 'NULL'
  
#   def __init__(self, name:str, parameters:dict = dict(default_parameters)):
#     self.parameters:dict = self.change_parameters(new_parameters=parameters)
#     self.name:str = name
#     self.columns:list = list()
#     self.primary_key: SQLHColumn = None
#     self.foreign_key = list()
#     self.database_object = None
#     if self.parameters['ID_ROW']:
#       id_row = SQLHColumn(name = 'id', table = self, type="INTEGER", constraint="NOT NULL", autoincrement= True)
#       self.primary_key = id_row
#       self.add_column(id_row)

#   def __len__(self):
#     primary_key = self.get_primary_key
#     if primary_key:
#       index = self.find_column(primary_key)
#       if index:
#         records = self.columns[index]['records']
#         return len(records)
#       else:
#         print(None)
#         return 0
#     else:
#       print(False)
#       return 0

#   def add_column(self, column_object:SQLHColumn): #need upgrade
#     if not self.find_column(column_object=column_object):
#       if column_object.primary_key and self.get_primary_key():
#         print("Primary key already exists.")
#         return False
#       else:
#         self.columns.append({"column_object":column_object, "records":list()})
#         if self.database_object:
#           self.database_object.add_column # NEED TO UPGRADE!!! (сделать запрос на добавления в базу данных)
#       return len(self.columns) - 1

#   def set_primary_key(self, column:SQLHColumn): # если уже есть и база данных тоже есть, не менять.
#     self.primary_key = column
#     #...
  
#   def get_primary_key(self): #need upgrade
#     return self.primary_key
    
#   def __add_null_record(self):
#     if len(self.columns):
#       for column in self.columns:
#         column_object = column['column_object']
#         records = column['records']
#         if self.primary_key is not column:
#           records.append(self.default_parameters['NULL_RECORD'])
#         else:
#           records.append(self.default_parameters[len(self.columns)])

#   def add_record(self, order:tuple, record:list):
#     self.__add_null_record()
#     last_index = len(self.columns) - 1
#     for loop_order, loop_record in zip(order, record):
#       for column in self.columns:
#         if column["column_object"] is loop_order:
#           try:
#             column["records"][last_index] = loop_record
#           except IndexError:
#             print(f"Index {last_index} does not exist in the list 'records'")
#           break

#     #NEED TO UPGRADE (добавить запрос на добавление в базу данных)


#   def set_database(self, new_database:SQLHDatabase): # если уже есть база данных, ничего не добавлять
#     if isinstance(new_database, SQLHDatabase):
#       self.database_object = new_database
#     else:
#       print(f"(set_database) | Isn't SQLHDatabase class")

#   def change_parameters(self, new_parameters:dict):
#     return_parameters = dict(self.default_parameters)
#     for key, value in return_parameters.items():
#       if key in new_parameters:
#         return_parameters[key] = new_parameters[key]
#     return return_parameters

#   def find_column(self, column_object:str|SQLHColumn):
#     if len(self.columns):
#       for index, loop_column in enumerate(self.columns):
#         if isinstance(column_object, str):
#           if loop_column['column_object'].name == column_object:
#             return index
#         elif isinstance(column_object, SQLHColumn):
#           if loop_column['column_object'] is column_object:
#             return index
#         else:
#           if dev_mode:
#             print("Wrong class, you need a str or SQLHColumn class.")
#           return False
#       return None
#     else:
#       if dev_mode:
#         print(f"There are no fields in the {self.name}")
#       return False

#   def make_dict(self): #need upgrade
#     pass 


# class SQLHColumn(object):
#   default_parameters = {
#     "type":"TEXT",
#     "constraint":"",
#     "primary_key":None,
#     "foreign_key":None
#   }
#   def __init__(self, name:str, table:SQLHTable, type:str = default_parameters['type'], constraint:str = default_parameters['constraint'], foreign_key:list = None, primary_key:bool = False, autoincrement:bool = False):
#     self.name: str = name
#     self.type: str = type
#     self.constraint: str = constraint
#     self.table: SQLHandler = table
#     self.foreign_key = None
#     if foreign_key and not primary_key:
#         if foreign_key[0]:
#           self.foreign_key: SQLHColumn = foreign_key
#           if self.table is not None:
#             self.table.foreign_key.append({"own": self, "foreign":self.foreign_key})
#     self.primary_key = None
#     if isinstance(table, SQLHTable):
#       if primary_key and not table.get_primary_key:
#         self.primary_key: bool = primary_ke
#         prmr_column = table.get_primary_key
#         table.set_primary_key(self)
#         self.autoincrement: bool = autoincrement
#       else:
#         self.primary_key = False
    
#     if self.table is not None:
#       self.table.add_column(self)
    
#   def make_dict(self):
#     dict_template = {
#       'name':self.name,
#       'type':self.type,
#       'constraint':self.constraint,
#       'primary_key':self.primary_key,
#       'foreign_key':self.foreign_key,
#       'table_object':self.table
#     }
#     return dict_template

# class SQLHandler(object):
#   def __init__(self, database_name:str = None):
#     self.connection: Connection = self.create_connection(name = database_name)

#   def create_connection(self, path_str:str = None, name:str = None) -> Connection:
#     if path_str:
#       self.connection: Connection = connect(path_str)
#       return self.connection
#     elif name:
#       filename = path.abspath(__file__)
#       dbdir = filename.rstrip('main.py')
#       dbpath = path.join(dbdir, name)
#       self.connection: Connection = connect(dbpath)
#       return self.connection
#     else:
#       return False

#   def get_connection(self) -> Connection:
#     return self.connection

#   def close_connection(self) -> None:
#     if self.connection:
#       self.connection.close()
#       return True
#     return False

#   def execute_query(self, query:str):
#     """ NOT RECOMMENDED FOR USE! ALL TABLES WILL NOT BE WRITTEN """
#     cursor = self.connection.cursor()
#     try:
#       cursor.execute(query)
#       result = cursor.fetchall()
#       self.connection.commit()
#       return result
#     except Error as e:
#       print(f'Query "{query}" have error: {e}')

#   def execute_create_table_query(self, table: SQLHTable):
#     name:str = table.name
#     columns_count:int = len(table.columns)
#     primary_key:SQLHColumn = table.primary_key

#     query_template = f"""CREATE TABLE IF NOT EXISTS {name}"""
#     column_template_list: list = []
#     temp_foreign_list: list = []
    
#     for record in table.columns:
#       column = record['column_object']
#       if column.foreign_key is not None:
#         temp_foreign_list.append([column, column.foreign_key])
#       temp_str:str = f"{column.name} {column.type}{f" PRIMARY KEY{" AUTOINCREMENT" if column.autoincrement else ""}" if column.primary_key else ""}{f" {column.constraint}" if column.constraint else ''}"
#       if column.primary_key:
#         column_template_list.insert(0, temp_str)
#       else:
#         column_template_list.append(temp_str)
#     for column in temp_foreign_list:
#       temp_str:str = f"FOREIGN KEY ({column[0].name}) REFERENCES {column[1].table.name}({column[1].name})"
#       column_template_list.append(temp_str)
#     query_template += "(\n"
#     for index, column_template in enumerate(column_template_list):
#       query_template += column_template + (',\n' if index + 1 != len(column_template_list) else '\n')
#     query_template += ");"
#     self.execute_query(query_template)
  
#   def execute_insert_query(self, name:str, records:list):
#     query_template = f"INSERT INTO {name}("
#     record_strings: list = [record['column_object'].name for record in records]
#     for index, record in enumerate(record_strings):
#       query_template += record + (',' if index + 1 != len(record_strings) else '')
#     query_template += ') VALUES'
#     value_template:list = list()
#     for i in range(len(records[0]['records'])):
#       temp_string = "("
#       for index, record in enumerate(records):
#         print(records)
#         crnt_rec = record['records'][i + 1]
#         temp_string += f"{("'" + str(crnt_rec) + "'" if isinstance(crnt_rec, str) and crnt_rec != 'NULL' else str(crnt_rec))}" + (',' if index + 1 != len(records) else '')
#       temp_string += ')'
#       value_template.append(temp_string)

#     for index, i in enumerate(value_template):
#       query_template += i + (',' if index + 1 != len(value_template) else '')
#     self.execute_query(query_template)
#     return query_template

#   def execute_select(self, name:str, columns_select:list|str, condition:str = None):
#     #['id','name'] ( it's for columns_select if you want to select only few or more columns )
#     query_template:str = f"SELECT "
#     if isinstance(columns_select, str):
#       if columns_select == 'ALL':
#         query_template += '*' 
#       else:
#         query_template += columns_select
#     elif isinstance(columns_select, list):
#       for index, column in enumerate(columns_select):
#         query_template += column + (',' if index + 1 != len(columns_select) else '')
#     query_template += f" FROM {name}"
#     if condition:
#       query_template += f"WHERE {condition}"
    
#     return self.execute_query(query_template)

#   def execute_alter_table(self, table:SQLHTable, method:str = 'ADD'):
#     if method == "ADD":
#         query_template: str = f"ALTER TABLE {table} {method} {column.name} {column.type} {column.constraint}"
        

#     elif method == "DROP":
#         pass
#   def execute_add_column_records(self, table:SQLHTable, column_dict:dict):
#     column:SQLHColumn = column_dict["column_object"]
#     records:list = column_dict["records"]
#     primary_key = table.get_primary_key()
#     if primary_key:
#         primary_key_records = table.get_records_by_column()
#         for index, record in enumerate(records):
#             update_template = {
#             "column_object":column,
#             "value":record,
#             "condition":[table.get_primary_key().name, primary_key_records[index]]
#             }
#             self.execute_update_table(table = table, update_template=update_template)

#   def execute_update_table(self, table:SQLHTable, update_template:dict=dict(), condition_query:str = None):
#       #update_template = {
#       #    "column_object":column,
#       #    "value":"some value",
#       #    "condition":["id", 4]
#       #}
#       condition = update_template['condition']
#       value = update_template['value']

#       query_template = f"UPDATE {table.name} SET {update_template["column_object"].name} = {value}"
#       if len(condition):
#           query_template += f" WHERE {condition[0]} like {condition[1]}"
#       elif condition_query:
#           query_template += f" WHERE {condition_query}"
#       execute_query(query_template)

# class SQLHDatabase(SQLHandler):
#   def __init__(self, database_name:str = None, tables:list = None):
#     super().__init__(database_name)
#     self.database_name = database_name
#     self.tables = list()
#     if tables:
#       for table in tables:
#         self.tables.append(table)
#         super().execute_create_table_query(table)

#   def add_table(self, table:SQLHTable):
#     if isinstance(table, SQLHTable):
#       if len(table.columns) and table.primary_key:
#         self.tables.append(table)
#         super().execute_create_table_query(table)
#         print(len(table), 123)
#         if len(table) is not None:
#           super().execute_insert_query(name=table.name, records=table.columns)
#     else:
#       if dev_mode:
#         print(f"The {table.name} table doesn't have columns or primary key.")
#       return False
      
#   def find_table(self, table:str|SQLHTable):
#     if len(self.tables):
#       for dtbs_table in self.tables:
#         if isinstance(table, str):
#           if dtbs_table.name == table:
#             return dtbs_table
#         elif isinstance(table, SQLHTable):
#           if table is dtbs_table:
#             return dtbs_table
#     return None

#   def insert_records(self, table: SQLHTable, records:list):
#     if self.find_table(table):
#       super().execute_insert_query(name=table.name, records=records)
#     pass

#   def remove_table(self, table:str|SQLHTable):
#     if isinstance(table, str):
#       for index, table_object in enumerate(self.tables):
#         if table.name == table:
#           super().execute_query(F"DROP TABLE IF EXISTS {table_object.name}")
#           self.tables.pop(index)
#           pass
#     elif isinstance(table, SQLHTable):
#       for index, table_object in enumerate(self.tables):
#         if table_object is table:
#           super().execute_query(F"DROP TABLE IF EXISTS {table_object.name}")
#           self.tables.pop(index)
#           pass
#   def select_table(self, table:str|SQLHTable, columns_select:list|str='ALL'):
#     if self.find_table(table):
#       if isinstance(table, str):
#         return super().execute_select(table, columns_select=columns_select)
#       elif isinstance(table, SQLHTable):
#         return super().execute_select(table.name, columns_select=columns_select)
#     else:
#       return False


#   def add_column(self, table:SQHLTable|str, column:SQLHColumn, records:list):
#     arg_table = None
#     if isinstance(table, str):
#         arg_table: SQLHTable = self.find_table(table = table)
#     elif isinstance(table, SQLHTable):
#         arg_table: SQLHTable= table.name
#     arg_dict: dict = {"column_object":column, "records":records}
#     super().execute_alter_table(table = arg_table, method = "ADD")
#     super().execute_add_column_records(table = table, column_dict = arg_dict)


# database = SQLHDatabase(database_name = "data.db")

# status_table = SQLHTable(name="status", parameters={"ID_ROW": True})
# status_column = SQLHColumn(name = "status", type="TEXT", constraint="NOT NULL", table=status_table)
# status_table.add_column(column_object=status_column)


# users_table = SQLHTable(name="status", parameters={"ID_ROW": True})
# user_nickname = SQLHColumn(name="nickname", type="TEXT", constraint="NOT NULL", table=users_table)
# user_status = SQLHColumn(name="status_id", type="INTEGER", constraint="NOT NULL", foreign_key=[status_table.get_primary_key(), status_column], table=users_table)
# users_table.add_column(column_object=user_nickname)
# users_table.add_column(column_object=user_status)

# records = ['user','admin','artist']
# for record in records:
#   status_table.add_record(order=('default'), record=[record])

# users_table.add_record(order=(user_nickname, user_status), record=['John Doe', 2])

# database.add_table(table=status_table)
# database.add_table(table=users_table)

# all_users = users_table.get_record(limit = "*", replacement=True)





#ОСНОВНЫЕ ЗАДАЧИ

#1.Доделать классы и запросы
#2.Сделать ЭКСПОРТ ДАННЫХ из базы данных для дальнейшнего обновления . Возможно хранить все экземпляры в отдельном файле, но можно и через похуизм, а тоесть через классы
