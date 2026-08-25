import sqlite3

#Database connection 

DB_NAME = "gym.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

#Create Table
def create_table():
    
    connection = get_connection()
    cursor = connection.cursor()
    
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS trial_bookings(
                
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                customer_name TEXT NOT NULL,
                
                phone_number TEXT NOT NULL,
                
                booking_date TEXT NOT NULL,
                
                booking_time TEXT NOT NULL,
                
                status TEXT NOT NULL DEFAULT 'BOOKED',
                
                UNIQUE(booking_date,booking_time)
                
            )           
    """)
    
    connection.commit()
    connection.close()
    
def check_availability(booking_date,booking_time):
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
                   SELECT booking_id FROM trial_bookings
                   WHERE booking_date = ? 
                   AND booking_time = ?
                   AND status = 'BOOKED'
                   """,(
                       booking_date,
                       booking_time
                   ))
    
    booking = cursor.fetchone()
    connection.close()
    
    if booking:
        print("Sorry ! this time-slot not available, already assign to someone Else")
        return False
    
    print("Yes this slot is available.")
    return True
    
def add_booking(customer_name, phone_number, booking_date, booking_time):
    
    check = check_availability(booking_date,booking_time)
    
    if check == False:
        return
        
        
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO trial_bookings
        (customer_name, phone_number, booking_date, booking_time)
        VALUES (?, ?, ?, ?)
    """, (
        customer_name,
        phone_number,
        booking_date,
        booking_time
    ))
    
   
    
    # cursor.execute("""
    #                SELECT customer_name,booking_id,booking_date,booking_time
    #                FROM trial_bookings
    #                WHERE booking_date = ? AND booking_time = ? 
    #                """,(
    #                    booking_date,
    #                    booking_time
    #                ))

    # result = cursor.fetchall()
    # print("=====" *20)
    # print(f"Hello dear, {result[0][0]} your booking is confirmed on the date : {result[0][2]} and time : {result[0][3]} \nPlease remember your booking id : {result[0][1]}")
    # print("=====" *20)
    
    
    booking_id = cursor.lastrowid
    
    connection.commit()
    connection.close()

    # print("Booking added successfully!")
    print (
        f"Booking confirmed! "
        f"Booking ID: {booking_id}, "
        f"Name: {customer_name}, "
        f"Date: {booking_date}, "
        f"Time: {booking_time}"
    )
    
def show_bookings():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM trial_bookings
    """)

    bookings = cursor.fetchall()

    connection.close()

    print("\n========== ALL BOOKINGS ==========")

    for booking in bookings:
        print(booking)
    
def cansel_booking(booking_id):
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        DELETE FROM trial_bookings
        WHERE booking_id = ?
    """, (booking_id,))

    
    connection.commit()
    
    if cursor.rowcount == 0 : 
        print(f"Booking not found with id : {booking_id}")
        connection.close()
        return
        
    connection.close()
    
    print(f"Booking canselled successfully for the booking id {booking_id}")
    
    
if __name__ == "__main__":
    
    # create_table()

    # add_booking(
    #     "mitul",
    #     "9876543270",
    #     "2026-08-26",
    #     "6:00 PM"
    # )

    # add_booking(
    #     "Amit",
    #     "9123456789",
    #     "2026-08-25",
    #     "7:00 PM"
    # )
    #   add_booking(
    #             "prince",
    #             "9876543000",
    #             "2026-08-26",
    #             "8:00 PM"
    #         )
    # add_booking(
    #     "jadav bhabha",
    #     "8123417900",
    #     "2026-09-01",
    #     "7:00 PM"
    # )
    # show_bookings()
    
    # cansel_booking(40)

    show_bookings()
    
   
