from data_from_pgadmin import connection

Connection = connection()

data = Connection.get_table_data("story")