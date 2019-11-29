import telebot
import pymysql
import datetime
from pymysql.cursors import DictCursor

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='timetablebot',
    charset='utf8mb4',
    cursorclass=DictCursor
)
print(connection)

# finally:
#   connection.close()
try:
    bot = telebot.TeleBot('843636336:AAGpTur1jadwV1dGrEsDUtFPKuorkXcYwYQ')
    weekkey = {}
except:
    print("Папапапам")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    lessonname = ""
    timestart = ""
    timeend = ""
    teacherinfo = ''
    classroomid = -1
    if message.text.lower() == "привет" or message.text.lower() == "/start":
        bot.send_message(message.from_user.id, "Привет, я бот, который поможет тебе с твоим расписанием.\n"
                                               "Ты можешь добавить расписание своих занятий и по команде "
                                               "получать информацию о расписании на сегодня.\n"
                                               "Чтобы создать расписание напиши /createdatetime\n"
                                               "Чтобы посмотреть расписание на сегодня, напиши /today")
    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Привет, я бот, который поможет тебе с твоим расписанием.\n"
                                               "Ты можешь добавить расписание своих занятий и по команде "
                                               "получать информацию о расписании на сегодня.\n"
                                               "Чтобы создать расписание напиши /createdatetime\n"
                                               "Чтобы посмотреть расписание на сегодня, напиши /today")
    elif message.text.lower() == "/createdatetime":
        bot.send_message(message.from_user.id, "Расписание составляется с помощью отправки сообщений с предметом.\n"
                                               
                                               "Напишите через запятую:\n День недели, Название предмета,"
                                               " время начала, время конца, \n"
                                               "ФИО преподавателя, номер аудитории, в четную/нечетную неделю происходит занятие\n"
                                               "В зависимости от недели напишите 0, нечетная - 1, четная - 2.\n\n"
                                               "Пожалуйста, пишите расписание по порядку: Сначала пары, которые начинаются раньше, потом те, что начинаются позже.\n"
                                               "Не пропускайте какие-то пункты!")
    elif(message.text.lower() =="/timetable"):
        for x in ["monday", "tuesday", "wednesday", "thusday", "friday", "saturday", "sunday","понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]:
            sqlget = "SELECT * FROM `users` WHERE `User` = %s AND `day` = '%s'"
            with connection.cursor() as cursor:
                cursor.execute(sqlget,(message.from_user.id,x))
                connection.commit()
                message1="Расписание на"+x+":"
                odd = (datetime.date(now.year, now.month, now.day).isocalendar()[1] -
                       datetime.date(2019, 9, 1).isocalendar()[
                           1]) % 2
                tmn=''
                if(odd==1): tmn ="нечетная"
                elif(odd==2): tmn ="четная"
                else: tmn='каждая'
                for row in cursor:
                    message1 = message1 + row['timestart'] + "->" + row['timeend'] + ": " + row[
                        'Name'] + ", аудитория:" + row['classroom'] + ", ведет:" + row['teacher']+"неделя: "+tmn+ "\n"



    elif (message.text.lower() == "/today"):
        now = datetime.datetime.now()
        print(now)
        odd = (datetime.date(now.year, now.month, now.day).isocalendar()[1] - datetime.date(2019, 9, 1).isocalendar()[
            1]) % 2
        sqlget = "SELECT * FROM `users` WHERE `User` = '%s' AND `day` = '%s'"
        with connection.cursor() as cursor:
            try:
                cursor.execute(sqlget, (message.from_user.id, now.weekday()))
                connection.commit()
                message1 = "Расписание на сегодня:\n\n"
                for row in cursor:
                    if(int(row['odd']) == 0 or (int(row['odd'])%2) == odd):
                        message1 = message1 + row['timestart']+"->"+row['timeend']+": "+row['Name']+", аудитория:"+row['classroom']+", ведет:"+row['teacher']+"\n"
                        print(row['timestart']+"->"+row['timeend']+": "+row['Name']+", аудитория:"+row['classroom']+", ведет:"+row['teacher']+"\n")
                bot.send_message(message.from_user.id,message1)
                if(message1 == "Расписание на сегодня:\n\n"):
                    bot.send_message(message.from_user.id,"Занятий нет")
            except(BaseException) as e:
                print(e.args)
                bot.send_message(message.from_user.id,"Расписание на этот день отсутствует.")

        # 0-четная, 1-неч

    else:
        objs = message.text.split(",")
        tmp = ["monday", "tuesday", "wednesday", "thusday", "friday", "saturday", "sunday","понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        if (objs[0].lower() not in tmp):
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        else:
            try:
                if (objs[5] == ""): bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
                try:
                    print(objs[0].lower())
                    if (objs[0].lower() == "monday" or objs[0].lower() == "понедельник"):
                        with connection.cursor() as cursor:

                            try:
                                sql1 = "INSERT INTO `users` (`User`,`Name`,`timestart`,`timeend`,`teacher`,`classroom`, `odd`,`day`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(sql1, (
                                message.from_user.id, objs[1], objs[2], objs[3], objs[4], objs[5], objs[6], "0"))
                                connection.commit()
                                bot.send_message(message.from_user.id, "Успешно добавлена новая пара.")

                            except(BaseException) as e:
                                bot.send_message(message.from_user.id, e.args)

                    elif (objs[0].lower() == "tuesday" or objs[0].lower() == "вторник"):
                        with connection.cursor() as cursor:
                            try:
                                sql1 = "INSERT INTO `users` (`User`,`Name`,`timestart`,`timeend`,`teacher`,`classroom`, `odd`,`day`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(sql1, (
                                message.from_user.id, objs[1], objs[2], objs[3], objs[4], objs[5], objs[6], "1"))
                                connection.commit()
                                bot.send_message(message.from_user.id, "Успешно добавлена новая пара.")


                            except(BaseException) as e:
                                bot.send_message(message.from_user.id, e.args)

                    elif (objs[0].lower() == "wednesday" or objs[0].lower() == "среда"):
                        with connection.cursor() as cursor:
                            try:
                                sql1 = "INSERT INTO `users` (`User`,`Name`,`timestart`,`timeend`,`teacher`,`classroom`, `odd`,`day`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(sql1, (
                                message.from_user.id, objs[1], objs[2], objs[3], objs[4], objs[5], objs[6], "2"))
                                connection.commit()
                                bot.send_message(message.from_user.id, "Успешно добавлена новая пара.")


                            except(BaseException) as e:
                                bot.send_message(message.from_user.id, e.args)
                    elif (objs[0].lower() == "thusday" or objs[0].lower() == "четверг"):
                        with connection.cursor() as cursor:
                            # Read a single record
                            try:
                                tmp_time=objs[3].split(":")
                                sql1 = "INSERT INTO `users` (`User`,`Name`,`timestart`,`timeend`,`teacher`,`classroom`, `odd`,`day`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(sql1, (
                                message.from_user.id, objs[1], objs[2], objs[3], objs[4], objs[5], objs[6], "3"))
                                connection.commit()
                                bot.send_message(message.from_user.id, "Успешно добавлена новая пара.")


                            except(BaseException) as e:
                                bot.send_message(message.from_user.id, e.args)
                    elif (objs[0].lower() == "friday" or objs[0].lower() == "пятница"):
                        with connection.cursor() as cursor:
                            try:
                                tm_=int(objs[6])
                                sql1 = "INSERT INTO `users` (`User`,`Name`,`timestart`,`timeend`,`teacher`,`classroom`, `odd`,`day`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(sql1, (
                                message.from_user.id, objs[1], objs[2], objs[3], objs[4], objs[5], tm_, "4"))
                                connection.commit()
                                bot.send_message(message.from_user.id, "Успешно добавлена новая пара.")


                            except(BaseException) as e:
                                bot.send_message(message.from_user.id, e.args)

                    elif (objs[0].lower() == "saturday" or objs[0].lower() == "суббота"):
                        with connection.cursor() as cursor:
                            try:
                                sql1 = "INSERT INTO `users` (`User`,`Name`,`timestart`,`timeend`,`teacher`,`classroom`, `odd`,`day`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(sql1, (
                                message.from_user.id, objs[1], objs[2], objs[3], objs[4], objs[5], objs[6], "5"))
                                connection.commit()
                                bot.send_message(message.from_user.id, "Успешно добавлена новая пара.")


                            except(BaseException) as e:
                                bot.send_message(message.from_user.id, e.args)

                    elif (objs[0].lower() == "sunday" or objs[0].lower() == "воскресенье"):
                        with connection.cursor() as cursor:
                            try:
                                tmp_time=objs[3].split(":")
                                sql1 = "INSERT INTO `users` (`User`,`Name`,`timestart`,`timeend`,`teacher`,`classroom`, `odd`,`day`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(sql1, (
                                message.from_user.id, objs[1], objs[2], objs[3], objs[4], objs[5], objs[6], "6"))
                                connection.commit()
                                bot.send_message(message.from_user.id, "Успешно добавлена новая пара.")

                            except(BaseException) as e:
                                bot.send_message(message.from_user.id, e.args)

                except:
                    pass
            except:
                bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        print(message.text.lower())


bot.polling(none_stop=True, interval=0)
