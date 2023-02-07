import snowflake.connector
from transform_1 import get_snowflake_connector



def main():
	con = get_snowflake_connector()
	query="""


	"""
	con.cursor().execute(query)