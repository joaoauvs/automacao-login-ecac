import logging
import time
from datetime import datetime
from functools import wraps
import json
import sys


@staticmethod
def get_message():
    """Recupera a mensagem do input."""
    return json.loads(sys.stdin.read())


def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logging.info(f"🕐 Execution started at: {start_time.strftime('%H:%M:%S')}")

        result = func(*args, **kwargs)

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        logging.info(f"🕑 Execution completed at: {end_time.strftime('%H:%M:%S')}")
        logging.info(
            f"🕞 Runtime: {int(hours):02} horas, {int(minutes):02} minutos e {int(seconds):02} segundos."
        )

        return result

    return wrapper


def attempts(max_attempts=3, waiting_time=1):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.info(
                        f"Attempt {attempt} of {max_attempts} failed. Error: {e}"
                    )
                    logging.info(f"Error: {type(e).__name__}, {e.args[0]}")
                    attempt += 1
                    time.sleep(waiting_time)
            raise Exception(f"Not possible to execute after {max_attempts} attempts.")

        return wrapper

    return decorador
