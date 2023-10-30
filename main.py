import sqlite3
import pandas as pd
import functions_framework

def query_from_db():

#comment to check

    db_file1 = 'quransingle.db'
    db_file2 = 'hadissingle.db'
    db_file3 = 'duasingle.db'

    connection1 = sqlite3.connect(db_file1)
    connection2 = sqlite3.connect(db_file2)
    connection3 = sqlite3.connect(db_file3)

    table_name1 = 'tbl_QuranComplete'
    table_name2 = 'tbl_Bukhari'
    table_name3 = 'tbl_dua'

    query1 = f"SELECT * FROM {table_name1};"
    query2 = f"SELECT * FROM {table_name2};"
    query3 = f"SELECT * FROM {table_name3};"

    df_quran = pd.read_sql_query(query1, connection1)
    df_hadis = pd.read_sql_query(query2, connection2)
    df_dua = pd.read_sql_query(query3, connection3)

    connection1.close()
    connection2.close()
    connection3.close()

    df_random_quran = df_quran.sample(n=2)
    df_random_hadis = df_hadis.sample(n=2)
    df_random_dua = df_dua.sample(n=2)

    quran_dict = df_random_quran.to_dict(orient='records')
    hadis_dict = df_random_hadis.to_dict(orient='records')
    dua_dict = df_random_dua.to_dict(orient='records')

    json_output = {
        "ayat_of_the_day": quran_dict,
        "hadees_of_the_day": hadis_dict,
        "dua_of_the_day": dua_dict
    }
    
    return json_output

@functions_framework.http
def cors_enabled_function(request):
    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        print("HERE")
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}
    
    return (query_from_db(), 200, headers)

