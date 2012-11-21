import psycopg2

CONN_STRING = "dbname='gp_prod', user='aumbhau', host='odcdwprod', password='odc'"

class DB(object):
	def query(self, q):
		conn = psycopg2.connect(CONN_STRING)
		cur = conn.cursor()
		cur.execute(q)
		results = cur.fetchall()
		return results