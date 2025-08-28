import psycopg2
from typing import Optional
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from configparser import ConfigParser


def load_config(filename="database.ini", section="postgresql"):
    """
    Purpose:
    Used for loading configuration

    Argument:
    filename -->    File containing connection values such as databaseserver, database, user and password
                    default database.ini
    section -->     Section name of ini file
                    default is postgresgl
    """
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return config


def connect(config):
    """
    Purpose:
    Connect to the PostgreSQL database server

    Argument:
    config -->  return value from load_config(filename, section)
    """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def execute_query(conn, query, params=None):
    """Execute a single query"""
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
        print("Query executed successfully.")


def fetch_query(conn, query, params=None):
    """Execute a query and fetch results"""
    with conn.cursor() as cur:
        cur.execute(query, params)
        result = cur.fetchall()
        return result


def insert_data(conn, table, columns, values):
    """Insert data into a table"""
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
    execute_query(conn, query, values)


def update_data(
    conn, table, set_columns, set_values, condition_column, condition_value
):
    """Update data in a table"""
    set_clause = ", ".join([f"{col} = %s" for col in set_columns])
    query = f"UPDATE {table} SET {set_clause} WHERE {condition_column} = %s"
    execute_query(conn, query, set_values + [condition_value])


def delete_data(conn, table, condition_column, condition_value):
    """Delete data from a table"""
    query = f"DELETE FROM {table} WHERE {condition_column} = %s"
    execute_query(conn, query, (condition_value,))


def select_with_conditions(conn, schema_name, table_name, where_conditions=None):
    """
    Select rows from a table with dynamic WHERE conditions.

    Parameters:
    conn (psycopg2.connection): The database connection object.
    schema_name (str): The schema name of the table.
    table_name (str): The name of the table to query.
    where_conditions (dict): A dictionary of columns and their values to filter by.

    Returns:
    list: A list of dictionaries representing the rows that match the conditions.
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Start building the query
            query = sql.SQL("SELECT * FROM {schema}.{table}").format(
                schema=sql.Identifier(schema_name), table=sql.Identifier(table_name)
            )

            # If there are conditions, build the WHERE clause
            if where_conditions:
                conditions = [
                    sql.SQL("{} = %s").format(sql.Identifier(k))
                    for k in where_conditions.keys()
                ]

                query = query + sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)

                # Execute the query
                cursor.execute(query, list(where_conditions.values()))
            else:
                cursor.execute(query)

            # Fetch all the rows
            rows = cursor.fetchall()
            return rows

    except Exception as error:
        raise error


def update_or_insert_vectordata(
    conn,
    schema_name,
    table_name,
    id,
    title,
    description,
    content,
    url,
    row_updated,
    embedded,
    conditions: Optional[str] = None,
) -> bool:
    """
    Updates vector data

    Parameters:
        conn (psycopg2.connection): The database connection object.
        schema_name (str): The schema name of the table.
        table_name (str): The name of the table to query.
        id = id of row
        title = title of the document
        description = description of the document
        content = content of the document
        url = url of the document
        row_updated = datetime typically now()
        embedded = embedded text

    Returns:
        true when update or insert is succesfull
    """

    try:
        results = select_with_conditions(conn, schema_name, table_name, conditions)
        conn.commit()

        if len(results) == 0:
            print("inserting")
            insert_data(
                conn,
                f"{schema_name}.{table_name}",
                [
                    "id",
                    "title",
                    "description",
                    "content",
                    "url",
                    "row_updated",
                    "embedding",
                ],
                [id, title, description, content, url, row_updated, embedded],
            )
        else:
            print("Updating")
            update_data(
                conn,
                f"{schema_name}.{table_name}",
                [
                    "id",
                    "title",
                    "description",
                    "content",
                    "url",
                    "row_updated",
                    "embedding",
                ],
                [id, title, description, content, url, row_updated, embedded],
                "id",
                id,
            )

        conn.commit()

        return True
    except Exception as error:
        print(f"Error executing query: {error}")
        return False
