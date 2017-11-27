"""general purpose utility functions"""


def conv_time(time_str):
    """converts HH:MM -> H:MM PM

    examples:
        "14:20" -> "2:20 PM"
        "12:20" -> "12:20 PM"
        "11:30" -> "11:30 AM"
    """
    hr = int(time_str[:2])
    mn = int(time_str[4:])
    suffix = "PM" if hr >= 12 else "AM"
    if hr > 12:
        hr = hr % 12
    return "{}:{:02d} {}".format(hr, mn, suffix)
