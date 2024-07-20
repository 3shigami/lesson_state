import sqlite3

class User:
  """
  Класс для работы с таблицей пользователей в локальной базе данных SQLite.
  """

  def __init__(self):
    
    self.db_path = "database/database.db"  # Путь к локальной базе данных SQLite по умолчанию

  def connect_to_db(self):
    
    connection = sqlite3.connect(self.db_path)
    return connection

  def check_user_exists(self, user_id):
    
    connection = self.connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

  def is_user_registered(self, user_id):
    
    if not self.check_user_exists(user_id):
      return False

    connection = self.connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT registration FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] == 1

  def register_user(self, user_id):
   
    if not self.check_user_exists(user_id):
      raise ValueError(f"Пользователь с ID {user_id} не существует")

    connection = self.connect_to_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET registration = 1 WHERE id = ?", (user_id,))
    connection.commit()
    connection.close()

  def add_user(self, user_id):

    connection = self.connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (id, registration) VALUES (?, 0)", (user_id,))
    connection.commit()
    connection.close()