from datetime import datetime

from dateutil.relativedelta import relativedelta


def calculate_number_periods(start_date, end_date):
    """
    Calculates the number of periods between two dates based on the specified payout period.

    Args:
        payout_period (str): The payout period, e.g., 'Days', 'Weeks', 'Months', 'Years', '30 Seconds', '2 Minutes'.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        int: The number of periods between the start and end dates.

    Raises:
        ValueError: If an invalid payout period is specified.
    """

    start_date = datetime.strptime(
        start_date, "%Y-%m-%d"
    )  # Include seconds in the format
    end_date = datetime.strptime(end_date, "%Y-%m-%d")  # Include seconds in the format

    diff = relativedelta(end_date, start_date)
    no_periods = diff.years * 12 + diff.months  # Total months

    return no_periods
