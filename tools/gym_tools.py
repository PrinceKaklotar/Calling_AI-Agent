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
            Check whether a PR Gym free-trial slot is available.

            AVAILABILITY INTENT:
            Use this tool when the user wants to CHECK whether a specific
            trial date and time is available.

            Examples:
            - "Is September 5 at 6 PM available?"
            - "Is tomorrow at 7 PM free?"
            - "Can I take a trial at 5 PM tomorrow?"
            - "Is that slot available?"

            REQUIRED INFORMATION:
            - booking_date
            - booking_time

            IMPORTANT:
            - If the user wants to check availability but the date or time
            is missing, DO NOT call this tool.
            - Ask the user for the missing date and/or time.
            - This tool ONLY checks availability.
            - This tool does NOT create a booking.
            - This tool does NOT cancel a booking.
            - Do not use this tool for general PR Gym questions.
        """
        # now we call our function 

        return db_check_availability(booking_date,booking_time)

@tool
def add_booking(customer_name:str, phone_number:str, booking_date:str, booking_time:str):
    """
            Create a PR Gym free-trial booking.
    
            BOOKING INTENT:
            If the user says they want to book, reserve, schedule, or take
            a free trial, treat this as a BOOKING REQUEST even if they have
            not provided all required information.
    
            Examples:
            - "I want to book a free trial."
            - "I want a free trial."
            - "Can I book a trial?"
            - "I want to reserve a trial slot."
            - "I would like to book a gym trial."
            - similer kind of question releted to trial, free trial , book the trial
    
            REQUIRED INFORMATION:
            - customer_name
            - phone_number
            - booking_date
            - booking_time
    
            IMPORTANT:
            - If the user has booking intent but one or more required
            details are missing, DO NOT call this tool.
            - Instead, ask the user for the missing required information.
            - NEVER send an incomplete booking request to the RAG/knowledge
            answering process.
            - Call this tool only when all required booking information
            is available.
            - This tool CREATES the actual booking.
            - Do not use this tool for availability checks,
            cancellation, or general PR Gym questions.
    """
    return db_add_booking(customer_name, phone_number, booking_date, booking_time)

@tool
def cansel_booking(booking_id : int):
    """
            Cancel an existing PR Gym free-trial booking.

            CANCELLATION INTENT:
            If the user says they want to cancel, remove, or delete an
            existing trial booking, treat it as a CANCELLATION REQUEST.

            Examples:
            - "I want to cancel my booking."
            - "Cancel my trial."
            - "I want to cancel my slot."
            - "Please cancel my booking."
            - "Cancel booking 14."

            REQUIRED INFORMATION:
            - booking_id

            IMPORTANT:
            - If the user wants to cancel but has NOT provided the booking ID,
            DO NOT call this tool.
            - Ask the user to provide the booking ID.
            - If the user already provided the booking ID, do not ask for it again.
            - Call this tool only when the user explicitly wants to cancel
            AND a booking_id is available.
            - If the user only asks what is required to cancel a booking,
            answer that the booking ID is required and DO NOT call this tool.
            - This tool ONLY cancels an existing booking.
            - This tool does NOT create a booking.
            - This tool does NOT check availability.
            - Do not use this tool for general PR Gym questions.
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

# cansel_booking.invoke({
#     "booking_id" : 5
# })


