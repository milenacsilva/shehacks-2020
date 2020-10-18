import psycopg2 as psql

# class DatabaseManager:
#     ''' Instance of a Database Manager '''
#     def __init__(self, DATABASE_URL):
#         self.conn = psql.connect(DATABASE_URL, sslmode='require')
#         self.cur = self.conn.cursor()
    
#     def is_user_registered(self, username, user_id):
#         self.cur.execute("SELECT username FROM Users WHERE id = (%s)", (user_id,))
         
#         if not self.cur.fetchall():
#             return False
    
#         print(f"Usuário encontrado: {username}")
#         return True
    
#     def register_new_user(self, username, user_id):
#         self.cur.execute("INSERT INTO Users(id, username) VALUES     (%s, %s)", (user_id, username))
#         print(f"Usuário novo adicionado: {username}")
#         self.conn.commit()

