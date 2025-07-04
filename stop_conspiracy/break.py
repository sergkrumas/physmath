import datetime
import locale
locale.setlocale(locale.LC_ALL, 'RUS')

range_num = 7
format_str = "%d %B %Y %H:%M:%S"
format_str = "%d %B %Y"

def main(eingeben_datetime):
	current_datetime = eingeben_datetime
	n = 0
	current_year = current_datetime.year
	while current_datetime.date() != datetime.datetime.today().date():
		current_datetime = current_datetime + datetime.timedelta(days=1)
		year = current_datetime.year
		month = current_datetime.month
		day = current_datetime.day
		# print(year, month, day)
		year_1 = year // 100
		year_2 = year - year//100*100
		if day + month + year_1 + year_2 == 68:
			n +=1
			if current_year != current_datetime.year:
				print(current_datetime.year)
				current_year = current_datetime.year
			print("\t%s)" % n, current_datetime.strftime(format_str))
			# if n > 100: 
			# 	break



date = "01/01/1900"
datetime_data = datetime.datetime.strptime(date, '%d/%m/%Y')
main(datetime_data)
