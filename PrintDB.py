from datetime import date, datetime, time, timedelta
from Database import ReadFromDB

end = datetime.now()
start = end - timedelta(hours=1)

result = ReadFromDB(start, end)