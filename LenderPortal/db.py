import psycopg2

CONN_STRING = "dbname = 'gp_prod' user = 'aumbhau' host = 'odc_dw_prod' password = 'odc'"

class DB(object):
	def query(self, q):
		conn = psycopg2.connect(CONN_STRING)
		cur = conn.cursor()
		cur.execute(q)
		results = cur.fetchall()
		conn.close()
		return results


