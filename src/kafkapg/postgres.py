import json
import psycopg2
import psycopg2.extras


def db_script(pg_uri, message):
    try:
        with psycopg2.connect(pg_uri) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                create_script = ''' CREATE TABLE IF NOT EXISTS webmetrics (
                                    id     SERIAL PRIMARY KEY,
                                    url    varchar(500) NOT NULL,
                                    response_time  float(4) NOT NULL,
                                    status_code SMALLINT NOT NULL,
                                    pattern varchar(50) NOT NULL)'''
                cur.execute(create_script)

                insert_script = 'INSERT INTO WebMetrics (url, response_time, status_code, pattern) VALUES (%s, %s, %s, %s)'
                json_message = json.loads(message)

                insert_values = (json_message["website"], json_message["response_time"], json_message["status_code"],
                                 json_message["page_pattern"])

                cur.execute(insert_script, insert_values)

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
