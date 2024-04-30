# SQLite3 Handler ( Table class ) example 

example = {
  "table_name": "users",
  "columns":{
    "first_column":{
      "type":"INTEGER",
      "primary_key":True,
      "foreign_key":{
        "column":None
      },
      "constraint":"NOT NULL"
    },
    "second_column":{
      "type":"TEXT",
      "primary_key":False,
      "foreign_key":{
        "column":None
      },
      "constraint":"NOT NULL",
      "table": table
    },
    "third_column":{
      "type":"INTEGER",
      "primary_key":False,
      "foreign_key":{
        "column": Column,
      },
      "constraint":"NOT NULL"
    },
    "records":{
      "first_column":[],
      "second_column":[],
      "third_column":[]
    }
  }
}

column_records = [
  {
    column_objects:123,
    records:[]
  }
]