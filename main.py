from __future__ import annotations
from sqlite3 import *
from sqlite3 import Error, Connection
from os import *


class SQLHTable(object):
  none_record = 'NULL'

  def __init__(self, table_name:str):
    self.datebase_object = None
    self.table_name = table_name
    self.columns = []
    self.records_number = 0
    self.primary_key = None
    self.records:list = list()
    self.datebase_object = None

  def set_database(self, database:SQLHDatebase):
    if isinstance(database, SQLHDatebase):
      database.add_table(self)
      self.datebase_object = database

  def add_column(self, column:SQLHColumn, records:list):
    dtbs_arg = list()
    if not column.column_name in self.columns_name():
      self.columns.append(column)
      self.records.append({'column_object':column, 'records':records})
      if self.datebase_object:
        self.datebase_object._add_column(table = self, column=column, records=records)
      return self.columns
    else:

      return False

  def set_primary_key(self, column:SQLHColumn):
    if self.primary_key:
      self.primary_key.primary_key = False
      self.primary_key = None
    self.primary_key = column
    self.primary_key.primary_key = True
    pass

  def get_primary_key(self):
    return self.primary_key

  def set_table(self, table:SQLHTable):
    self.table = table

  def find_column(self, column_name:str = None, column_object: SQLHColumn = None):
    if column_object:
      for index, column in enumerate(self.columns):
        if column is column_object:
          return index
    elif column_name:
      for index, column in enumerate(self.columns):
        if column.column_name is column_name:
          return index

  def make_dict(self):
    table_dict = {
      'table_name':self.table_name,
      'columns':[i for i in self.columns],
      'primary_key':self.get_primary_key(),
      'table_object':self
    }
    return table_dict

  def add_records(self, orders:list, order_records:list):
    for record in self.records:
      added = False
      for index, order in enumerate(orders):
        if isinstance(order, str):
          if order == record['column_object'].column_name:
            for order_record in order_records:
              if order_record == '#_':
                record['records'].append(len(self) + 1)
              else:
                record['records'].append(order_record[index])
            added = True
        elif isinstance(order, SQLHColumn):
          if order is record['column_object']:
            for order_record in order_records:
              if order_record[index] == '#_':
                record['records'].append(len(self) + 1)
              else:
                record['records'].append(order_record[index])
            added = True
        if index + 1 == len(orders) and not added:
          for order_record in order_records:
              record['records'].append(self.none_record)
       # new_rows: list = list()
    # for i in range(0, len(order_records)):
    #   self.records.append([])
    #   for column in self.columns:
        
    #     self.records[-1].append({'column_object':column, 'record':self.none_record})
    #   new_rows.append((len(self.records) - 1 if len(self.records) else 1))

    # for row in new_rows:
    #   current_row_columns = self.records[row]
    #   for c_index, column in enumerate(current_row_columns):
    #     for o_index, order in enumerate(orders):
    #       added = False
    #       # print(f'{row + 1} row \n{c_index} column - {column['column_object'].column_name}\n{o_index} order - {order}\n')
    #       if isinstance(order, SQLHColumn):
    #         if column['column_object'] is order:
    #           column['record'] = order_records[o_index]
    #           print(column['column_object'].column_name, order.column_name)
    #           break
    #       elif isinstance(order, str):
    #         if column['column_object'].column_name == order:
    #           column['record'] = order_records[o_index]
    #           print(column['column_object'].column_name, order)
    #           break

  def count_records(self):
    if len(self.records):
      for index, record in enumerate(self.records):
        if record['column_object'].primary_key:
          return len(record['records'])
      return len(records[0]['records'])
    else:
      return 0
    

  def columns_name(self):
    return_list:list = list()
    for column in self.columns:
      column:SQLHColumn = column
      return_list.append(column.column_name)
    return return_list

  def __len__(self):
    return self.count_records()
class SQLHColumn(object):

  def __init__(self, column_name:str, table:SQLHTable = None, column_type:str = 'TEXT', column_constraint:str = '', primary_key:bool = False, autoincrement: bool = False, foreign_key:SQLHColumn = None):
    self.column_name: str = column_name
    self.column_type: str = column_type
    self.column_constraint: str = column_constraint
    self.foreign_key = None
    if isinstance(table, SQLHTable):
      if primary_key:
        self.primary_key: bool = primary_key
        table.set_primary_key(self)
        self.autoincrement: bool = autoincrement if self.primary_key else None
      else:
        self.primary_key = False
      self.table: SQLHandler = table
      self.table.column_add([self])
    if foreign_key and not primary_key:
      if foreign_key.primary_key:
        self.foreign_key: SQLHColumn = foreign_key if not self.primary_key else None

  def make_dict(self):
    column_dict = {
      'column_name':self.column_name,
      'type':self.column_type,
      'primary_key':self.primary_key,
      'foreign_key':{
        'column':self.foreign_key
      },
      'constraint':self.column_constraint,
      'records':self.records,
      'column_object': self,
      'table_object': self.table
    }
    return column_dict

  def make_primary_key(self):
    if self.table:
      pass
    else:
      pass

  def change_table(self):
    if self.table:
      pass

class SQLHandler(object):
  def create_connection(self, path_str:str = None, name:str = None) -> Connection:
    if path_str:
      self.connection: Connection = connect(path_str)
      return self.connection
    elif name:
      filename = path.abspath(__file__)
      dbdir = filename.rstrip('main.py')
      dbpath = path.join(dbdir, name)
      self.connection: Connection = connect(dbpath)
      return self.connection
    else:
      return False

  def get_connection(self) -> Connection:
    return self.connection

  def close_connection(self) -> None:
    if self.connection:
      self.connection.close()
      return True
    return False

  def execute_query(self, query:str):
    """ NOT RECOMMENDED FOR USE! ALL TABLES WILL NOT BE WRITTEN """
    cursor = self.connection.cursor()
    try:
      cursor.execute(query)
      result = cursor.fetchall()
      self.connection.commit()
      return result
    except Error as e:
      print(f'Error: {e}')

  def execute_create_table_query(self, table: SQLHTable):
    table_name:str = table.table_name
    columns_count:int = len(table.columns)
    primary_key:SQLHColumn = table.primary_key

    query_template = f"""CREATE TABLE IF NOT EXISTS {table_name}"""
    column_template_list: list = []
    temp_foreign_list: list = []
    
    for column in table.columns:
      if column.foreign_key:
        temp_foreign_list.append([column, column.foreign_key])
      temp_str:str = f"{column.column_name} {column.column_type}{f" PRIMARY KEY{" AUTOINCREMENT" if column.autoincrement else ""}" if column.primary_key else ""}{f" {column.column_constraint}" if column.column_constraint else ''}"
      if column.primary_key:
        column_template_list.insert(0, temp_str)
      else:
        column_template_list.append(temp_str)
    for column in temp_foreign_list:
      temp_str:str = f"FOREIGN KEY ({column[0].column_name}) REFERENCES {column[1].table.table_name}({column[1].column_name})"
      column_template_list.append(temp_str)
    query_template += "(\n"
    for index, column_template in enumerate(column_template_list):
      query_template += column_template + (',\n' if index + 1 != len(column_template_list) else '\n')
    query_template += ");"
    self.execute_query(query_template)
  
  def execute_insert_query(self, table_name:str, records:list):
    query_template = f"INSERT INTO {table_name}("
    record_strings: list = [record['column_object'].column_name for record in records]
    for index, record in enumerate(record_strings):
      query_template += record + (',' if index + 1 != len(record_strings) else '')
    query_template += ') VALUES'
    value_template:list = list()
    for i in range(len(records[0]['records'])):
      temp_string = "("
      for index, record in enumerate(records):
        crnt_rec = record['records'][i]
        temp_string += f"{("'" + str(crnt_rec) + "'" if isinstance(crnt_rec, str) and crnt_rec != 'NULL' else str(crnt_rec))}" + (',' if index + 1 != len(records) else '')
      temp_string += ')'
      value_template.append(temp_string)

    for index, i in enumerate(value_template):
      query_template += i + (',' if index + 1 != len(value_template) else '')
    self.execute_query(query_template)
    return query_template

  def execute_select(self, table_name:str, columns_select:list|str, condition:str = None):
    #['id','name'] ( it's for columns_select if you want to select only few or more columns )
    query_template:str = f"SELECT "
    if isinstance(columns_select, str):
      if columns_select == 'ALL':
        query_template += '*' 
      else:
        query_template += columns_select
    elif isinstance(columns_select, list):
      for index, column in enumerate(columns_select):
        query_template += column + (',' if index + 1 != len(columns_select) else '')
    query_template += f" FROM {table_name}"
    if condition:
      query_template += f"WHERE {condition}"
    
    return self.execute_query(query_template)

  def execute_alter_table(self, table:str, column: SQLHColumn, records:list, method:str = 'ADD'):
    query_template: str = f"ALTER TABLE {table} {method} {column.column_name} {column.column_constraint} {column.column_constraint}"


class SQLHDatebase(SQLHandler):
  def __init__(self, connection: Connection = None, datebase_name:str = None, tables:list = None):
    self.connection: Connection = None
    self.datebase_name = None
    self.tables = list()
    if isinstance(connection, Connection):
      self.connection = connection
    elif datebase_name:
      self.connection = super().create_connection(name = datebase_name)
    if tables:
      for table in tables:
        self.tables.append(table)
        super().execute_create_table_query(table)

  def add_table(self, table:SQLHTable):
    if isinstance(table, SQLHTable):
      self.tables.append(table)
      super().execute_create_table_query(table)
      if len(table) != 0:
        super().execute_insert_query(table_name=table.table_name, records=table.records)
    
  def find_table(self, table:str|SQLHTable):
    if len(self.tables):
      for dtbs_table in self.tables:
        if isinstance(table, str):
          if dtbs_table.table_name == table:
            return dtbs_table
        elif isinstance(table, SQLHTable):
          if table is dtbs_table:
            return dtbs_table
    return None

  def __insert_records(self, table: SQLHTable, records:list):
    if self.find_table(table):
      super().execute_insert_query(table_name=table.table_name, records=records)
    pass
  def remove_table(self, table:str|SQLHTable):
    if isinstance(table, str):
      for index, table_object in enumerate(self.tables):
        if table.table_name == table:
          super().execute_query(F"DROP TABLE IF EXISTS {table_object.table_name}")
          self.tables.pop(index)
          pass
    elif isinstance(table, SQLHTable):
      for index, table_object in enumerate(self.tables):
        if table_object is table:
          super().execute_query(F"DROP TABLE IF EXISTS {table_object.table_name}")
          self.tables.pop(index)
          pass
  def select_table(self, table:str|SQLHTable, columns_select:list|str='ALL'):
    if self.find_table(table):
      if isinstance(table, str):
        return super().execute_select(table, columns_select=columns_select)
      elif isinstance(table, SQLHTable):
        return super().execute_select(table.table_name, columns_select=columns_select)
    else:
      return False

  def _add_column(self, table:str|SQHLTable, column:SQLHColumn, records:list):

    pass


datebase = SQLHDatebase(datebase_name='data.db')
users_table = SQLHTable(table_name="users")
id_column = SQLHColumn(column_name = 'id', table = users_table, column_type = 'INTEGER', column_constraint= 'NOT NULL', autoincrement= True, primary_key= True)
nickname_column = SQLHColumn(column_name = 'name', table = users_table)
something_column = SQLHColumn(column_name = 'something', table = users_table)
correct_order = [id_column, 'name', something_column]
users_table.add_records(orders=correct_order, order_records=[['#_', 'John Doe', 'something'], ["#_", 'Jane Doe', 'hmm'], ["#_", 'Jane Doe', 'hmm']])
something_column = SQLHColumn(column_name = 'anothersomething', table = users_table)

users_table.set_database(database=datebase)

users_table.add_column()