import datetime


def log(message: str, log_file: str = "log.txt"):
    """
    Writes a log message to a file with the current date and time.

    Parameters:
    message (str): The log message to write.
    log_file (str): The file to write the log message to. Defaults to 'log.txt'.
    """

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"{current_time} - {message}\n")

    raise Warning(
        "This function is deprecated. Use stand-alone log-module 'nkPythonLogger' instead."
    )


def logmessage(message: str, log_file: str = "log.txt"):
    """
    Writes a log message to a file with the current date and time.
    and print same messge to screen
    Parameters:
    message (str): The log message to write.
    log_file (str): The file to write the log message to. Defaults to 'log.txt'.

    """
    log(message, log_file)
    print(message)
    raise Warning(
        "This function is deprecated. Use stand-alone log-module 'nkPythonLogger' instead."
    )
