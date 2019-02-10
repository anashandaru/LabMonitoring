import MySQLdb

def Insert2db(tabel,bacaan):
	# prepare SQL query to insert data
	sql = "INSERT INTO %s(bacaan) VALUES(%.2f);"%(tabel, bacaan)

	try:
		# open database connection
		db = MySQLdb.connect("localhost","root","anashandaru","labbpptkg")
		
		
	except:
		print('Database Connection Error')
		return

	try:
		# prepare cursor
		cursor = db.cursor()

		# execute SQL command
		cursor.execute(sql)

		# Commit Changes in database
		db.commit()
	except:
		print('Insert Database Error')
		# Rollback in case there is any error
		db.rollback()
	
	# disconnect from server
	db.close()

