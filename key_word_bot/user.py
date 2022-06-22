from datetime import date, datetime, timedelta

class User:
    
    date = ''
    name_event = ''
    mode = None
    date_format = "%Y.%m.%d"

    def __init__(self, id, mode, cursor, connection):
        self.id = id
        self.mode = mode
        self.cursor = cursor
        self.connection = connection
    
    def get_file(self, data):
        print(f'Mode: {self.mode}')
        if self.mode is None:
            if data == '/start':
                return None, '/add_event - добавить мероприятие\n/search - поиск по ключевому слову'
            if data == '/add_event':
                self.mode = 'In_project'
                return None, 'Введите название проекта'
            elif data == '/search':
                self.mode = 'Search_keyword'
                return None, 'Введите слово для поиска'

        if self.mode == 'Search_keyword':
            self.cursor.execute(f"""SELECT name FROM Event JOIN WHERE keyword LIKE '%{data}%'""")
            results = self.cursor.fetchall()
            print(results)
            answer = ''
            if len(results)>0:
                for result in results:
                    answer += result[0] + '\n'
                self.mode = None
                return None, answer
            else:
                self.mode = None
                return None, 'Ничего не найдено'

        if self.mode == 'In_project':
            self.project = data
            self.mode = 'In_date'
            return None, 'Введите дату в формате **ГГГГ.ММ.ДД**, "Сегодня" или "Вчера"'

        if self.mode == 'In_date':
            now = datetime.now()
            if data == 'Сегодня':
                self.date = now.strftime(self.date_format)
            elif data == 'Вчера':
                now = now - timedelta(days=1)
                self.date = now.strftime(self.date_format)
            else:
                self.date = data
            self.mode = 'In_name'
            return None, 'Введите название мероприятия'

        elif self.mode == 'In_name':
            self.name_event = data
            self.mode = 'In_keyword'
            return None, 'Введите ключевые слова через запятую (не меньше 5 слов)'

        elif self.mode == 'In_keyword':
            keywords = data.split(',')
            if len(data.split(','))<5:
                return None, 'Введите больше 4 ключевых слов!'
            name_file = self.date + ' ' + self.name_event
            f = open(f'./txt/{name_file}.txt', mode = 'w')
            f.write(data)
            f.close()
            self.cursor.execute(f"""INSERT INTO Event VALUES ('{self.date}', '{self.project.strip().lower()}', '{self.name_event.strip()}')""")
            id_rowid = self.cursor.lastrowid
            self.connection.commit()
            for keyword in keywords:
                self.cursor.execute(f"""INSERT INTO KeyWord VALUES ('{id_rowid}', '{keyword.strip().lower()}')""")
            self.connection.commit()
            self.mode = None
            return f'./txt/{name_file}.txt', f'Назовите папку:\n**{name_file}**\nи переместите в него файл'