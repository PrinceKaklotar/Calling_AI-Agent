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
            Check whether a PR Gym trial booking slot is available
            for the specified date and time.

            USE THIS TOOL when the customer wants to:
            - check if a trial slot is available
            - know whether a specific date and time is free
            - ask if they can come for a trial at a particular date and time
            - check a slot before making a booking

            REQUIRED INFORMATION:
            - booking_date: The requested trial date.
            - booking_time: The requested trial time.

            IMPORTANT:
            - This tool ONLY checks slot availability.
            - It does NOT create a booking.
            - It does NOT cancel a booking.
            - Do NOT use this tool for general PR Gym questions,
            membership information, pricing, facilities, or timings.

            EXAMPLES:
            "Is tomorrow at 6 PM available?"
            "Is September 5 at 7 PM free?"
            "Can I take a trial at 5 PM tomorrow?"

            For these requests, use this tool to check the requested slot.
        """
# now we call our function 
        return db_check_availability(booking_date,booking_time)


@tool
def add_booking(customer_name:str, phone_number:str, booking_date:str, booking_time:str):
    """
    Create a new PR Gym trial booking for the customer.

    USE THIS TOOL when the customer explicitly wants to:
    - book a trial
    - reserve a trial slot
    - make an appointment for a trial
    - confirm a trial booking

    REQUIRED INFORMATION:
    - customer_name: Customer's name.
    - phone_number: Customer's phone number.
    - booking_date: Date of the trial.
    - booking_time: Time of the trial.

    IMPORTANT:
    - This tool CREATES a booking in the PR Gym booking system.
    - It should only be used when the customer wants to actually
      make a booking.
    - It is NOT a tool for checking general PR Gym information.
    - It is NOT a tool for cancelling a booking.
    - The requested date and time must be provided before creating
      the booking.
    - The booking system will determine whether the requested slot
      can be booked.

    EXAMPLES:
    "Book me a trial tomorrow at 6 PM."
    "I want to reserve September 5 at 7 PM."
    "Please book my trial for 5 PM tomorrow."

    For these requests, use this tool to create the booking.
    """
    
    return db_add_booking(customer_name, phone_number, booking_date, booking_time)

@tool

def cansel_booking(booking_id : int):
    """
    Cancel an existing PR Gym trial booking using its booking ID.

    USE THIS TOOL when the customer explicitly wants to:
    - cancel an existing trial booking
    - remove a previously made booking
    - cancel an appointment and provides the booking ID

    REQUIRED INFORMATION:
    - booking_id: The unique booking ID of the booking
      that the customer wants to cancel.

    IMPORTANT:
    - This tool ONLY cancels an existing booking.
    - It does NOT create a new booking.
    - It does NOT check general slot availability.
    - Do NOT use this tool when the customer only wants to
      know whether a slot is available.
    - Do NOT use this tool without a valid booking ID.

    EXAMPLES:
    "Cancel my booking 12."
    "I want to cancel booking ID 25."
    "Please cancel my trial booking, ID 7."

    For these requests, use this tool to cancel the specified booking.
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


