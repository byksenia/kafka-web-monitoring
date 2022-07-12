import json
import sys
import unittest
import psycopg2

from kafkapg.postgres import db_script
from kafkapg.data_generator import website_data


class TestData(unittest.TestCase):
    pg_uri = ""
    website_url = ""

    def test_data_generator(self):

        metrics_result = website_data(self.website_url)
        json_result = json.loads(metrics_result)

        # Test website url matches
        self.assertTrue(self.website_url, json_result["website"])
        # Test regexp is found
        self.assertRegex(json_result["page_pattern"], "\si.\sa")
        # Test if response code is valid
        self.assertEqual(json_result["status_code"], 200)
        # Test response time
        self.assertGreater(json_result["response_time"], 0)
        self.assertLess(json_result["response_time"], 10)

    def test_table_exists(self):
        exists = False
        try:
            metrics_result = website_data(self.website_url)
            db_script(self.pg_uri, metrics_result)

            conn = psycopg2.connect(self.pg_uri)
            cur = conn.cursor()

            # Checking whether webmetrics table is created
            cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = 'webmetrics')")
            exists = bool(cur.fetchone()[0])

            # Check whether webmetrics table is created
            self.assertTrue(exists, True)

            json_result = json.loads(metrics_result)
            website_url = "'" + str(json_result["website"]) + "'"
            prep_time = str(json_result["response_time"])
            response_time = "'" + prep_time + "'"

            # Check whether the data was added
            cur.execute(
                 f'SELECT * from public.webmetrics where url={website_url} and response_time={response_time}')
            exists = bool(cur.fetchone()[0])

            self.assertTrue(exists, True)
            cur.close()

        except psycopg2.Error as e:
            print(e)
        return exists

    def test_db_connection(self):
        version = False
        try:
            conn = psycopg2.connect(self.pg_uri)
            query_sql = 'SELECT VERSION()'
            cur = conn.cursor()
            cur.execute(query_sql)
            version = len(cur.fetchone()[0])

            # Check if connection to postgreSQL is successful and version is received
            self.assertGreater(version, 0)
            cur.close()
        except psycopg2.Error as e:
            print(e)
        return version


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestData.website_url = sys.argv.pop()
        TestData.pg_uri = sys.argv.pop()
    unittest.main()
