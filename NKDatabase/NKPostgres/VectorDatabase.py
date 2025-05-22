import datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from configparser import ConfigParser

# ***********************************************************************************************************************************
# ***********************************************************************************************************************************
# INSERTING
# ***********************************************************************************************************************************
# ***********************************************************************************************************************************
def insert_vectordata_nkgpt_sleeping_table(conn, items_id, title, description, content, url, source, document_id, embedding_str):
    """
    inserts vector data into nkgpt tables

    Parameters:
    conn (psycopg2.connection): The database connection object.
    items_id:  id of row
    title: title of the document
    description: description of the document
    content: content of the document
    url: url of the document
    embedded: embedded text

    Returns:

    true when update or insert is succesfull
    """
    return insert_vectordata_sleeping_table('nkgpt.insert_nkpgt_item', conn, items_id, title, description, content, url, source, document_id, embedding_str)

def insert_vectordata_hygiejnar_sleeping_table(conn, items_id, title, description, content, url, source, document_id, embedding_str):
    """
    inserts vector data into hygiejnar tables

    Parameters:
    conn (psycopg2.connection): The database connection object.
    items_id:  id of row
    title: title of the document
    description: description of the document
    content: content of the document
    url: url of the document
    embedded: embedded text

    Returns:

    true when update or insert is succesfull
    """
    return insert_vectordata_sleeping_table('nkgpt.insert_hygiejnar_item', conn, items_id, title, description, content, url, source, document_id, embedding_str)

def insert_vectordata_sleeping_table(app_procedure, conn, items_id, title, description, content, url, source, document_id, embedding_str):
    """
    inserts vector data

    Parameters:
    app_procedure: name of insert procedure
    conn (psycopg2.connection): The database connection object.
    items_id:  id of row
    title: title of the document
    description: description of the document
    content: content of the document
    url: url of the document
    embedded: embedded text

    Returns:

    true when update or insert is succesfull
    """
    try:
        if conn:
            with conn.cursor() as cursor:
                query = """
                CALL {}(%s, %s, %s, %s, %s, %s, %s, %s);
                """.format(app_procedure)

                cursor.execute(query, (items_id, title, description, content, url, source, document_id, embedding_str))




                # cursor.execute("""
                # CALL %s(%s, %s, %s, %s, %s, %s, %s, %s);
                # """, (app_procedure, items_id, title, description, content, url, source, document_id, embedding_str))

                conn.commit()
                return True
        return False

    except Exception as error:
        print(f'Error executing query: {error}')
        return False


# ***********************************************************************************************************************************
# ***********************************************************************************************************************************
# DELETING
# ***********************************************************************************************************************************
# ***********************************************************************************************************************************
def delete_data_in_nkgpt_sleeping_data(conn):
    """
    deletes all vector data in the nkgpt sleeping tables

    Returns:

    true when update or insert is succesfull
    """
    return delete_data_in_sleeping_data('nkgpt.clean_sleeping_items', conn)

def delete_data_in_hygiejnar_sleeping_data(conn):
    """
    deletes all vector data in the nkgpt sleeping tables

    Returns:

    true when update or insert is succesfull
    """
    return delete_data_in_sleeping_data('nkgpt.clean_hygiejnar_sleeping_items', conn)


def delete_data_in_sleeping_data(app_procedure, conn):
    """
    deletes all vector data in the sleeping tables

    Returns:

    true when update or insert is succesfull
    """
    try:
        if conn:
            with conn.cursor() as cursor:
                strCaller = f'call {app_procedure}();'
                cursor.execute(strCaller)
                conn.commit()
                return True
        return False

    except Exception as error:
        print(f'Error executing query: {error}')
        return False

# ***********************************************************************************************************************************
# ***********************************************************************************************************************************
# SWITCH ACTIVE TABLES
# ***********************************************************************************************************************************
# ***********************************************************************************************************************************
def switch_nkgpt_active_tables(conn):
    """
    switches sleeping tables to active tables and vice versa

    Returns:

    true when update or insert is succesfull
    """
    return switch_active_tables('nkgpt.change_active_tables', conn)

def switch_hygiejnar_active_tables(conn):
    """
    switches sleeping tables to active tables and vice versa

    Returns:

    true when update or insert is succesfull
    """
    return switch_active_tables('nkgpt.change_hygiejnar_active_tables', conn)

def switch_active_tables(app_procedure, conn):
    """
    switches sleeping tables to active tables and vice versa

    Returns:

    true when update or insert is succesfull
    """
    try:
        if conn:
            with conn.cursor() as cursor:
                strCaller = f'call {app_procedure}();'
                cursor.execute(strCaller)
                conn.commit()
                return True
        return False

    except Exception as error:
        print(f'Error executing query: {error}')
        return False
