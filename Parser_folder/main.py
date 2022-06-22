import os
import sqlite3

dir = "/Volumes/ВИНТ 10/"
# for dirn in os.listdir(dir):
#     if dirn[0]!='.':
#         print(dirn)
# for dirnames in os.walk("./D/"):
#     for dirname in dirnames:
#         print(dirname)
# for dirpath, dirnames, filenames in os.walk("./D/"):
#     # перебрать каталоги
#     for dirname in dirnames:
#         print("Каталог:", os.path.join(dirpath, dirname))
connection = sqlite3.connect("database.db", check_same_thread=False)
cursor = connection.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS Dirs(
# project VARCHAR(255) NOT NULL,
# name VARCHAR(255) NOT NULL
# )"""
# )
# f = open('./project.txt', mode ='r')
# projects = f.readlines()
# for project in projects:
#     project = project[:-1]
#     for dirpath, dirnames, filenames in os.walk(dir + project):
#         for dirname in dirnames:
#             cat = dirname
#             print("Каталог:", cat)
#             cursor.execute(f"""INSERT INTO Dirs VALUES ('{project}', '{cat}')""")
#             connection.commit()

cursor.execute(