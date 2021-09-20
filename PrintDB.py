from datetime import date, datetime, time, timedelta
from Database import ReadFromDB

end = datetime.now()
start = end - timedelta(days=2)

result = ReadFromDB(start, end)
