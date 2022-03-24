import sqlite3
import random
from datetime import datetime, date, timedelta, time
from Names import first_name, last_name, middle_name, Destination, Destination_extr

#инициализация
Tipy_Sobitiy = []
DateTime_null = datetime(2020, 2, 21, 0, 0)
Reisy = []
Sobitiya = []
Brigady_busy_time = {}
BigLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Reisy_sort = []
Sobitiya_sort = []
Reisy_tuples = []
Sobitiya_tuples = []
Pass = []
digit = '0123456789'


conn = sqlite3.connect("C:/Users/petry/YandexDisk/учёба/Бойко/Управление базами данных/ДЗ/БД_аэропорта.db")
cur = conn.cursor()

#Добавление данных в базу
def insert_into_table(table_name, data):
    sql = """INSERT INTO """ + table_name + """ VALUES(""" + "?,"*(len(data) - 1) + """?);"""
    res = cur.execute(sql, data)
    conn.commit()
    return res

#Генерация случайной даты с ограничением по годам
def random_date(year_min, year_max):
    year = random.randint(year_min, year_max)
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:
        if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    return date(year, month, day)

#загрузка типов событий из базы данных
def Type_sob_load():
    Tipy_Sobitiy_tuples = cur.execute("""SELECT * FROM [Типы событий]""").fetchall()
    Tipy_Sobitiy_time = [15, 20, 30, 10, 30, 30, 15, 15, 10, 30, 40, 15, 5, 0, 0]
    for i in range(len(Tipy_Sobitiy_tuples)):
        Tipy_Sobitiy.append([Tipy_Sobitiy_tuples[i], Tipy_Sobitiy_time[i]])
    #for i in Tipy_Sobitiy:
        #print(i)

#загрузка перечня бригад из базы данных
def Brig_Init():
    Brigady = cur.execute("""SELECT * FROM [Бригады]""").fetchall()
    for br in Brigady:
        if br[1] not in Brigady_busy_time:
            Brigady_busy_time[br[1]] = {br[0]: DateTime_null}
        else:
            Brigady_busy_time[br[1]][br[0]] = DateTime_null
    del(Brigady)

#генерация случайной последовательность из y символов, входящих в строку s
def random_char(y, s):
    return ''.join(random.choice(s) for x in range(y))

#Добавление события в список событий
def Add_Sobitie(type_sob, reis_id, brigada_name, DateTime):
    DateTime_start = DateTime
    brigada_id = None
    if brigada_name is not None:
        free_brig = False
        for brig, time_busy in Brigady_busy_time[brigada_name].items():
            if DateTime >= time_busy:
                DateTime_start = DateTime
                free_brig = True
                #print(time_busy)
                break
        if not free_brig:
            brig = min(Brigady_busy_time[brigada_name].keys())
            DateTime_start = Brigady_busy_time[brigada_name][brig]

        brigada_id = brig

    DateTime_finish = DateTime_start + timedelta(minutes=Tipy_Sobitiy[type_sob - 1][1]) + timedelta(
        seconds=random.randint(60 * int(-Tipy_Sobitiy[type_sob - 1][1] / 10),
                               60 * int(Tipy_Sobitiy[type_sob - 1][1] / 10)))

    if brigada_name is not None:
        Brigady_busy_time[brigada_name][brig] = DateTime_finish

    #('type =', type_sob, 'IN:', DateTime, 'Start:', DateTime_start, 'Finish:', DateTime_finish)

    Sobitiya.append([0, type_sob, reis_id, brigada_id, DateTime_start,
                     DateTime_finish])  # Событию всегда добавляется id_reis = номеру рейса и id = 0, чтобы в конце было возможно переназначение идентификаторов
    return DateTime_finish

##  Генерация рейсов и соответствующих событий, а также сортировка и запись их в базу данных
def Reisy_and_sob_generate(N):
    DateTime = DateTime_null
    for i in range(1, N, 2):
        reis_number_in = random_char(3, BigLetters) + str(random.randint(100, 999))
        reis_number_out = random_char(3, BigLetters) + str(random.randint(100, 999))
        samolet_number = random.randint(1, 500)
        Punct_otpravleniya = random.choice(Destination)
        Punct_naznacheniya = random.choice(Destination)
        AC_isp = cur.execute("""SELECT [Авиакомпания-владелец] FROM [Самолёты] WHERE [Номер самолёта] = ?""",
                             (samolet_number,)).fetchall()

        Reisy.append([i, reis_number_in, samolet_number, AC_isp[0][0], 1, Punct_otpravleniya, DateTime])

        DateTime_sob = DateTime
        DateTime_sob = Add_Sobitie(1, i, None, DateTime_sob)

        DateTime_sob_1 = Add_Sobitie(2, i, None, DateTime_sob)
        DateTime_sob_2 = Add_Sobitie(3, i, "Погрузочная", DateTime_sob)
        DateTime_sob = max(DateTime_sob_1, DateTime_sob_2)

        DateTime_sob_1 = Add_Sobitie(4, i, "Санитарная", DateTime_sob)
        DateTime_sob_2 = Add_Sobitie(5, i, "Клининговая", DateTime_sob)
        DateTime_sob_3 = Add_Sobitie(6, i, "Ремонтная", DateTime_sob)
        DateTime_sob = max(DateTime_sob_1, DateTime_sob_2, DateTime_sob_3)

        DateTime_sob = Add_Sobitie(7, i + 1, "Заправочная", DateTime_sob)

        DateTime_sob_1 = Add_Sobitie(8, i + 1, "Водного обеспечения", DateTime_sob)
        DateTime_sob_2 = Add_Sobitie(9, i + 1, "Провиантная", DateTime_sob)
        DateTime_sob = max(DateTime_sob_1, DateTime_sob_2)

        DateTime_sob_1 = Add_Sobitie(10, i + 1, "Погрузочная", DateTime_sob)
        DateTime_sob_2 = Add_Sobitie(11, i + 1, None, DateTime_sob)
        DateTime_sob = max(DateTime_sob_1, DateTime_sob_2)

        DateTime_sob = Add_Sobitie(13, i + 1, "Противообледенительной обработки", DateTime_sob)

        DateTime_sob = Add_Sobitie(12, i + 1, None, DateTime_sob)

        Reisy.append([i + 1, reis_number_out, samolet_number, AC_isp[0][0], 2, Punct_naznacheniya, DateTime_sob])
        DateTime = DateTime + timedelta(minutes=10) + timedelta(seconds=random.randint(-90, 90))

    for i in Reisy:
        print('Рейс:', i)

    for i in Sobitiya:
        print('Событие:', i)
    
    #Сортировка рейсов и событий по времени (для событий по времени начала)
    Reisy_sort = sorted(Reisy, key=lambda x: x[6])
    Sobitiya_sort = sorted(Sobitiya, key=lambda x: x[4])

    for i in Reisy_sort:
        print(i)

    for i in Sobitiya_sort:
        print(i)
        i.append(0)

    for i in range(len(Reisy_sort)):
        for sob in Sobitiya_sort:
            if (sob[2] == Reisy_sort[i][0]) & (not sob[-1]):
                sob[2] = i + 1
                sob[-1] = 1
        Reisy_sort[i][0] = i + 1
    
    #Удаление старых данных из базы
    cur.execute("""DELETE FROM 'Рейсы';""")
    cur.execute("""DELETE FROM 'События';""")
    
    #Запись данных в базу
    for i in range(len(Reisy_sort)):
        Date = date(Reisy_sort[i][6].year, Reisy_sort[i][6].month, Reisy_sort[i][6].day)
        Time = time(Reisy_sort[i][6].hour, Reisy_sort[i][6].minute, Reisy_sort[i][6].second)
        Reisy_tuples.append((Reisy_sort[i][0], Reisy_sort[i][1], Reisy_sort[i][2], Reisy_sort[i][3], Reisy_sort[i][4], Reisy_sort[i][5], str(Date), str(Time),  str(Date), str(Time)))
        print(Reisy_tuples[i])
        insert_into_table('Рейсы', Reisy_tuples[i])
    
    for i in range(len(Sobitiya_sort)):
        Date_start = date(Sobitiya_sort[i][4].year, Sobitiya_sort[i][4].month, Sobitiya_sort[i][4].day)
        Date_finish = date(Sobitiya_sort[i][5].year, Sobitiya_sort[i][5].month, Sobitiya_sort[i][5].day)
        Time_start = time(Sobitiya_sort[i][4].hour, Sobitiya_sort[i][4].minute, Sobitiya_sort[i][4].second)
        Time_finish = time(Sobitiya_sort[i][5].hour, Sobitiya_sort[i][5].minute, Sobitiya_sort[i][5].second)
        Sobitiya_tuples.append((i + 1, Sobitiya_sort[i][1], Sobitiya_sort[i][2], Sobitiya_sort[i][3], str(Date_start), str(Time_start), str(Date_finish), str(Time_finish), None))
        print(Sobitiya_tuples[i])
        insert_into_table('События', Sobitiya_tuples[i])

# генерация списка пассажиров по рейсам и запись их в базу данных
def Passengers_generate():
    id_pass = 1
    for reis in Reisy_tuples:
        #Получение максимальной вместимости самолёта данного рейса
        number_of_pass = cur.execute("""SELECT [Модели самолётов].[Пассажиры эконом],
                            [Модели самолётов].[Пассажиры первый],
                            [Модели самолётов].[Пассажиры бизнес]
                        FROM [Самолёты] INNER JOIN [Модели самолётов]
                        ON [Самолёты].[Модель самолёта] = [Модели самолётов].[Идентификатор]
                        WHERE [Самолёты].[Номер самолёта] = ?""", (reis[2],)).fetchall()
        
        #Генерация случайного количества пассажиров для данного рейса (но не менее 2/3 от максимальной вместимости)
        for number in range(sum(number_of_pass[0]) - random.randint(0, int(sum(number_of_pass[0]) / 3))):
            BD_date = random_date(1940, 2005)

            if reis[5] in Destination_extr:
                Num_doc = random_char(2, digit) + ' ' + random_char(7, digit)
            else:
                year = (random.randint(BD_date.year + 14, 2020)) % 100
                if year < 10:
                    year = '0' + str(year)
                else:
                    year = str(year)
                Num_doc = random_char(2, digit) + ' ' + year + ' ' + random_char(6, digit)

            gender_id = random.randint(1, 2)
            if gender_id == 1:
                gender = 'm'
            else:
                gender = 'f'
            Last = random.choice(last_name[gender])
            First = random.choice(first_name[gender])
            Middle = random.choice(middle_name[gender])

            BD = str(BD_date)

            Pass.append((id_pass, Num_doc, Last, First, Middle, gender_id, BD, reis[0], number + 1, 0, None, None))
            id_pass += 1
    
    print(Pass[0:10])
    #Удаление старых данных из базы и запись новых
    cur.execute("""DELETE FROM 'Пассажиры';""")
    for passenger in Pass:
        insert_into_table('Пассажиры', passenger)

def main():
    Brig_Init()
    Type_sob_load()
    Reisy_and_sob_generate(100)
    Passengers_generate()

main()