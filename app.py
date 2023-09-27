import eel
import configparser
import datetime
import locale,calendar
import time
from datetime import timedelta
#locale.setlocale(locale.LC_TIME, 'ru_Ru')
# print(calendar.month_name[3].lower())
cal_list = []
def plural_days(n,list_a):
    days = list_a
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]

for i in range(1,13):
    cal_list.append(calendar.month_name[i].lower())
    
# print(cal_list)
    
ls = {cal_list[0]:None,cal_list[1]:None,cal_list[2]:None,cal_list[3]:None,cal_list[4]:None,cal_list[5]:None,cal_list[6]:None,cal_list[7]:None,cal_list[8]:None,cal_list[9]:None,cal_list[10]:None,cal_list[11]:None}

for i in range(0,11):
	exec(f"ls[cal_list[{i}]] = dict(map(lambda x: (x,[]), range(1, 31+1)))")
# print(ls[cal_list[0]])
today = datetime.datetime.today()
day = today.strftime("%Y-%m-%d") # настоящее время
# print(day)
hour1 = "10:00" # от
hour2 = "18:00" # До
hour3 = "10:00" # от
hour4 = "18:00" # До
day1,day2 = "2023-09-01","2023-09-26"
stavka = 250
stavka2 = 250
FMT = '%H:%M:%S'
# hours = today.strptime(hour2, FMT) - today.strptime(hour1, FMT)
# print(hours) # это мы получили часы работы
def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
# print(get_sec(str(hours))) #перевод в секунды
# print(stavka/60/60*get_sec(str(hours))) #итог за день в рублях
config = configparser.ConfigParser() # читаем файл с конфигурацией
config.read('file.ini', "cyrillic")
eel.init('web', allowed_extensions=['.js', '.html'])
eel.update(day,hour1,hour2,hour3,hour4,stavka,stavka2,day1,day2) # отдаем html разметку вбраузер
@eel.expose
def add(day,hour1,hour2,hour3,hour4,stavka,stavka2):
	hours1 = f"{hour1}:00" # от
	hours2 = f"{hour2}:00"# До

	hours3 = f"{hour3}:00"
	hours4 = f"{hour4}:00"
	
	FMT = '%H:%M:%S'
	hours = today.strptime(hours2, FMT) - today.strptime(hours1, FMT)
	hours0 = today.strptime(str(hours), '%H:%M:%S').strftime(f'{"%H:%M:%S"}')

	hours_c = today.strptime(hours4, FMT) - today.strptime(hours3, FMT)
	hours0_c = today.strptime(str(hours_c), '%H:%M:%S').strftime(f'{"%H:%M:%S"}')
	# print(hours0_c)

	sec = get_sec(str(hours))

	sec2 = get_sec(str(hours_c))

	summa = round(int(stavka)/60/60*sec)

	summa2 = round(int(stavka2)/60/60*sec2)
	# print(int(stavka)/60/60*sec, summa, summa2)

	month = today.strptime(day, "%Y-%m-%d").strftime("%B")
	day = today.strptime(day, "%Y-%m-%d").strftime("%d")
	# print(month,day)
	config[f"{month.lower()}"][f"{day}"] = f"{summa} {stavka} {hours0} {summa2} {stavka2} {hours0_c} {hours1} {hours2} {hours3} {hours4}"
	with open('file.ini', 'w') as configfile:
		config.write(configfile,"ansi")
# print(day,hour1,hour2,stavka)
@eel.expose()
def result(day1,day2):
	global ls
	month_start = today.strptime(day1, "%Y-%m-%d").strftime("%m")
	month_end = today.strptime(day2, "%Y-%m-%d").strftime("%m")
	day_start = today.strptime(day1, "%Y-%m-%d").strftime("%d")
	day_end = today.strptime(day2, "%Y-%m-%d").strftime("%d")
	# print(int(f"{int(day_start):00}") )

	num_day = 0

	summa = 0
	summa_2 = 0
	hours3 = 0
	hours3_2 = 0
	i_i = int(f"{int(month_end):00}") - int(f"{int(month_start):00}")
	if int(f"{int(month_end):00}") == int(f"{int(month_start):00}"):
		print("это один и тот же месяц")
		for m in range(int(f"{int(month_start):00}")-1, int(f"{int(month_end):00}")):
			# print(config[cal_list[m]])
			for i in range(int(f"{int(day_start):00}"),int(f"{int(day_end):00}")+1):
				daycheck = str(f'{i:02}') in config[cal_list[m]]
				# print(daycheck)
				if daycheck == True:
					num_day +=1
					x = {i:config[cal_list[m]][str(f'{i:02}')].split()[0:]} # {1: ['2000', '145']}
					print(x)
					# print(today.strptime(str(x[i][2]),"%H:%M:%S"))
					ls[cal_list[m]][i] = x #{'январь': {1: ['2000', '145']}}
					
					summa += int(x[i][0])
					hours3 += get_sec(today.strptime(str(x[i][2]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
					
					summa_2 += int(x[i][3])
					hours3_2 += get_sec(today.strptime(str(x[i][5]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
					# print(timedelta(seconds=hours3_2))
					d = datetime.datetime(1,1,1) + timedelta(seconds=hours3_2)
					s = datetime.datetime(1,1,1) + timedelta(seconds=hours3)
					# print(summa,num_day,'%d:%d:%d' % (s.day*24 + s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % (24*d.day + d.hour, d.minute, d.second))
					eel.result(summa,num_day,'%d:%d:%d' % ((s.day-1)*24+s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % ((d.day-1)*24+d.hour, d.minute, d.second))

	elif int(f"{int(month_end):00}") - int(f"{int(month_start):00}") == 1:
		print("месяца близкие друг к другу")
		# for x in range(int(f"{int(day_start):00}"),32):
		# 	print(x, "day elif 1")
		m = int(f"{int(month_start):00}")-1
			# print(config[cal_list[m]])
		for i in range(int(f"{int(day_start):00}"),32):
			print(i)
			daycheck = str(f'{i:02}') in config[cal_list[m]]
			# print(daycheck)
			if daycheck == True:
				num_day +=1
				x = {i:config[cal_list[m]][str(f'{i:02}')].split()[0:]} # {1: ['2000', '145']}
				print(x)
				# print(today.strptime(str(x[i][2]),"%H:%M:%S"))
				ls[cal_list[m]][i] = x #{'январь': {1: ['2000', '145']}}
				
				summa += int(x[i][0])
				hours3 += get_sec(today.strptime(str(x[i][2]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
					
				summa_2 += int(x[i][3])
				hours3_2 += get_sec(today.strptime(str(x[i][5]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
		for i in range(1,int(f"{int(day_end):00}")+1):
			print(i)
			daycheck = str(f'{i:02}') in config[cal_list[m+1]]
			# print(daycheck)
			if daycheck == True:
				num_day +=1
				x = {i:config[cal_list[m+1]][str(f'{i:02}')].split()[0:]} # {1: ['2000', '145']}
				print(x)
				# print(today.strptime(str(x[i][2]),"%H:%M:%S"))
				ls[cal_list[m+1]][i] = x #{'январь': {1: ['2000', '145']}}
				
				summa += int(x[i][0])
				hours3 += get_sec(today.strptime(str(x[i][2]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
				
				summa_2 += int(x[i][3])
				hours3_2 += get_sec(today.strptime(str(x[i][5]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты

		# for x in range(1,int(f"{int(day_end):00}")+1):
		# 	print(x, "day elif 1_1")

		d = datetime.datetime(1,1,1) + timedelta(seconds=hours3_2)
		s = datetime.datetime(1,1,1) + timedelta(seconds=hours3)
		# print(summa,num_day,'%d:%d:%d' % (s.day*24 + s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % (24*d.day + d.hour, d.minute, d.second))
		eel.result(summa,num_day,'%d:%d:%d' % ((s.day-1)*24+s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % ((d.day-1)*24+d.hour, d.minute, d.second))

	else:

		print("интервал от 1 месяца")
		m = int(f"{int(month_start):00}")-1
		# print(config[cal_list[m]])
		for i in range(int(f"{int(day_start):00}"),32):
			daycheck = str(f'{i:02}') in config[cal_list[m]]
			# print(config[cal_list[m]])
			# print(i, config[cal_list[m]])
			if daycheck == True:
				# print(i)
				num_day +=1
				x = {i:config[cal_list[m]][str(f'{i:02}')].split()[0:]} # {1: ['2000', '145']}
				print(x)
				# print(today.strptime(str(x[i][2]),"%H:%M:%S"))
				ls[cal_list[m]][i] = x #{'январь': {1: ['2000', '145']}}
				
				summa += int(x[i][0])
				hours3 += get_sec(today.strptime(str(x[i][2]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
				
				summa_2 += int(x[i][3])
				hours3_2 += get_sec(today.strptime(str(x[i][5]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
		for s in range(i_i-1):
			m += 1
			for i in range(1,32):
				# print(i, config[cal_list[m]])
				daycheck = str(f'{i:02}') in config[cal_list[m]]
				if daycheck == True:
					num_day +=1
					x = {i:config[cal_list[m]][str(f'{i:02}')].split()[0:]} # {1: ['2000', '145']}
					print(x)
					# print(today.strptime(str(x[i][2]),"%H:%M:%S"))
					ls[cal_list[m]][i] = x #{'январь': {1: ['2000', '145']}}
					
					summa += int(x[i][0])
					hours3 += get_sec(today.strptime(str(x[i][2]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
					
					# print(hours3)
					summa_2 += int(x[i][3])
					hours3_2 += get_sec(today.strptime(str(x[i][5]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
					# print(timedelta(seconds=hours3_2))
		for i in range(1,int(f"{int(day_end):00}")+1):
			m = int(f"{int(month_end):00}")-1
			# print(i, config[cal_list[m]])
			# print(config[cal_list[m]])
			daycheck = str(f'{i:02}') in config[cal_list[m]]
			# print(daycheck)
			if daycheck == True:
				num_day +=1
				x = {i:config[cal_list[m]][str(f'{i:02}')].split()[0:]} # {1: ['2000', '145']}
				print(x)
				# print(today.strptime(str(x[i][2]),"%H:%M:%S"))
				ls[cal_list[m]][i] = x #{'январь': {1: ['2000', '145']}}
				
				summa += int(x[i][0])
				hours3 += get_sec(today.strptime(str(x[i][2]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
				
				summa_2 += int(x[i][3])
				hours3_2 += get_sec(today.strptime(str(x[i][5]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты

		d = datetime.datetime(1,1,1) + timedelta(seconds=hours3_2)
		s = datetime.datetime(1,1,1) + timedelta(seconds=hours3)
		# print(summa,num_day,'%d:%d:%d' % (s.day*24 + s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % (24*d.day + d.hour, d.minute, d.second))
		eel.result(summa,num_day,'%d:%d:%d' % ((s.day-1)*24+s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % ((d.day-1)*24+d.hour, d.minute, d.second))

	# for m in range(1, 12):
		# for i in range(1,31):
		# 	daycheck = str(f'{i:02}') in config[cal_list[m]]
		# 	if daycheck == True:
		# 		num_day +=1
		# 		x = {i:config[cal_list[m]][str(f'{i:02}')].split()[0:]} # {1: ['2000', '145']}
		# 		# print(today.strptime(str(x[i][2]),"%H:%M:%S"))
		# 		ls[cal_list[m]][i] = x #{'январь': {1: ['2000', '145']}}
				
		# 		summa += int(x[i][0])
		# 		hours3 += get_sec(today.strptime(str(x[i][2]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
				
		# 		# print(hours3)
		# 		summa_2 += int(x[i][3])
		# 		hours3_2 += get_sec(today.strptime(str(x[i][5]),"%H:%M:%S").strftime(f'{"%H:%M:%S"}')) # переводим наши отработанные часы в минуты
		# 		# print(timedelta(seconds=hours3_2))
	# 			d = datetime.datetime(1,1,1) + timedelta(seconds=hours3_2)
	# 			s = datetime.datetime(1,1,1) + timedelta(seconds=hours3)
	# 			# print(summa,num_day,'%d:%d:%d' % (s.day*24 + s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % (24*d.day + d.hour, d.minute, d.second))
	# 			eel.result(summa,num_day,'%d:%d:%d' % ((s.day-1)*24+s.hour, s.minute, s.second),summa_2,'%d:%d:%d' % ((d.day-1)*24+d.hour, d.minute, d.second))
# plural_days(%d,['день', 'дня', 'дней'])
#eel.browsers.set_path("chrome", "C:/Users/admin/Documents/chrome-win/chrome.exe")
eel.start('index.html',mode="browser",port=0,size=(1,1))
