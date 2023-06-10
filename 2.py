import mysql.connector
import threading
import time

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'xxx',
  'raise_on_warnings': True
}

# Funkcja, która zwiększa wartość rekordu
def increment_value(user):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    try:
        # Start transakcji
        cursor.execute("START TRANSACTION")

        # Pobranie aktualnej wartości z blokadą rekordu
        query = ("SELECT value FROM counter WHERE id = 1 FOR UPDATE")
        cursor.execute(query)
        row = cursor.fetchone()
        current_value = row[0]

        # sleep
        time.sleep(3)

        # Zwiększenie wartości o 1
        new_value = current_value + 1

        # Aktualizacja wartości w bazie danych
        update_query = ("UPDATE counter SET value = %s WHERE id = 1")
        cursor.execute(update_query, (new_value,))

        # Zatwierdzenie transakcji
        cnx.commit()

        print(f'User {user} update value to {new_value}')

    except mysql.connector.Error as err:
        # Jeśli coś poszło nie tak, cofnij transakcję
        print(f"Something went wrong: {err}")
        cnx.rollback()

    finally:
        cursor.close()
        cnx.close()

# Symulacja dwóch użytkowników próbujących jednocześnie zaktualizować dane
thread1 = threading.Thread(target=increment_value, args=(1,))
thread2 = threading.Thread(target=increment_value, args=(2,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()