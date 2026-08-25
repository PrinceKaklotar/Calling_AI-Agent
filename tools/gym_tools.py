# NOTE:
# The VS Code "Run Python File" button may not work correctly here
# because this file uses package imports such as:
# from database.database import ...
#
# Run this file from the project root instead:
#
# python -m tools.gym_tools
#
# Example:
# PS C:\Users\Dell\Desktop\Calling AI Agent> python -m tools.gym_tools



from langchain_core.tools import tool
from database.database import (
    check_availability as db_check_availability,
    add_booking as db_add_booking,
    cansel_booking as db_cansel_booking)


@tool
def check_availability(booking_date: str, booking_time: str):
  """
        Check whether a PR Gym trial booking slot is available for a specific date and time.

        Use this tool whenever the customer:
        - asks whether a trial slot is available
        - asks if they can book a trial at a specific date and time
        - asks whether a particular time slot is free or already booked
        - wants to check available booking times before making a reservation

        The tool requires:
        - booking_date: The requested booking date.
        - booking_time: The requested booking time.

        Do NOT use this tool for:
        - general questions about PR Gym
        - membership or pricing questions
        - gym timings or facilities
        - actually creating a booking
        - cancelling a booking

        This tool only CHECKS availability. It does not create or cancel a booking.
"""
# now we call our function 
  return db_check_availability(booking_date,booking_time)


@tool
def add_booking(customer_name:str, phone_number:str, booking_date:str, booking_time:str):
    """
    Book a PR Gym trial slot for a customer.

    Use this tool when the customer has provided the required
    customer name, phone number, date, and time and wants to
    create a trial booking.

    This tool creates the booking in the PR Gym booking system.
    Do not use it only to check availability.
    """
    
    return db_add_booking(customer_name, phone_number, booking_date, booking_time)

@tool

def cansel_booking(booking_id : int):
    """
    Cancel an existing PR Gym trial booking.

    Use this tool when the customer explicitly wants to cancel
    an existing booking and provides the booking ID.

    This tool permanently removes the booking from the booking
    system.
    """
    
    # call the function which is written in databse.py
    return db_cansel_booking(booking_id)



# result = check_availability.invoke({
#     "booking_date": "2026-09-02",
#     "booking_time": "5:00 PM"
# })

# print(result)

# add_booking.invoke({
#     "customer_name": "Raju",
#     "phone_number": "9876543210",
#     "booking_date": "2026-09-03",
#     "booking_time": "6:00 PM"
# })

cansel_booking.invoke({
    "booking_id" : 5
})


