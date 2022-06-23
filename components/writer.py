import os
import re
import sys
from _thread import start_new_thread

from components.reader import Reader
from utils.terminal import cls

sys.path.append(os.path.dirname(os.path.abspath(__file__))[0:-11])

import pickle
import random
import socket
import time

from config import WRITER_TIMER, PORT_REPLICATOR_SENDER
from constants.codes import Code
from logger import Logger
from models.receiver_property import ReceiverProperty
from utils.connection import Connection


class Writer:
    data_sending_socket: socket.socket
    is_connected: bool = False
    is_running: bool = False
    writer_count: int = 0

    @staticmethod
    def start():  # pragma: no cover
        Writer.is_running = True
        Writer.connect()
        start_new_thread(Writer.automatic_data_generation, ())
        Writer.user_prompt()

    @staticmethod
    def connect():  # pragma: no cover
        Writer.data_sending_socket = Connection.connect(PORT_REPLICATOR_SENDER)
        Logger.log_action('[INFO]: Sending data to replicator sender')
        print('[INFO]: Sending data')
        Writer.is_connected = True

    @staticmethod
    def reconnect():  # pragma: no cover
        Logger.log_action('[INFO]: Writer reconnecting')
        print('[INFO]: Reconnecting')
        Writer.is_connected = False
        Writer.connect()

    @staticmethod
    def user_prompt():  # pragma: no cover
        while Writer.is_running:
            if Writer.is_connected:
                Writer.print_menu()

                choice = Writer.ask_for_input(5)
                if choice == 1:
                    Writer.writer_count += 1
                elif choice == 2:
                    Writer.writer_count -= 1
                elif choice == 3:
                    Writer.print_code_values()
                elif choice == 4:
                    Writer.print_interval_values()
                elif choice == 5:
                    cls()
                    Writer.is_running = False
                    exit()

    @staticmethod
    def print_menu():  # pragma: no cover
        cls()
        print('Writers:')
        for writer_id in range(Writer.writer_count):
            writer_id += 1
            print(f'{writer_id}. Worker {writer_id}')
        print('\nSelect option:')
        print('\t1. Create new writer')
        print('\t2. Delete existing writer')
        print('\t3. Get values by code')
        print('\t4. Get values by interval')
        print('\t5. Exit')

    # Tested
    @staticmethod
    def ask_for_input(max_number: int):
        while Writer.is_running:
            choice = input()
            try:
                choice = int(choice)
                if 1 <= choice <= max_number:
                    return choice
                else:
                    continue
            except:
                continue

    @staticmethod
    def automatic_data_generation():  # pragma: no cover
        while Writer.is_running:
            if Writer.is_connected:
                time.sleep(WRITER_TIMER)
                for writer in range(Writer.writer_count):
                    code = random.choice(list(Code))
                    value = random.randint(1000, 9999)
                    item = ReceiverProperty(code, value)
                    package = ('ITEM', item)
                    package = pickle.dumps(package)
                    try:
                        Writer.data_sending_socket.send(package)
                        Logger.log_action(f'[INFO]: Writer {writer + 1} sent item: {item}')
                    except socket.error:
                        Writer.reconnect()

    @staticmethod
    def print_interval_values():  # pragma: no cover
        code, start_date, start_time, end_date, end_time = Writer.get_interval_data()
        values = Reader.get_values_by_interval(code, start_date, start_time, end_date, end_time)

        cls()
        print(f'Values:')
        for value in values:
            print(f'\t{value}')
        input()

    @staticmethod
    def get_interval_data():  # pragma: no cover
        code = Writer.get_code()
        start_date = Writer.get_date('start')
        start_time = Writer.get_time('start')
        end_date = Writer.get_date('end')
        end_time = Writer.get_time('end')
        return code, start_date, start_time, end_date, end_time

    # TODO: Test
    @staticmethod
    def get_date(time_type: str):
        while Writer.is_running:
            cls()
            print(f'Enter {time_type} date in format YYYY-MM-DD')
            user_input = input()
            if not re.match('^[0-9]{4}-[0-1]?[0-9]-[0-3]?[0-9]$', user_input):
                continue
            return user_input

    # TODO: Test
    @staticmethod
    def get_time(time_type: str):
        while Writer.is_running:
            cls()
            print(f'Enter {time_type} time in HH:MM:SS')
            user_input = input()
            if not re.match('[0-9]{2}:[0-9]{2}:[0-9]{2}', user_input):
                continue
            return user_input

    @staticmethod
    def print_code_values():  # pragma: no cover
        code = Writer.get_code()
        values = Reader.get_values_by_code(code)

        cls()
        print(f'Code report:')
        for value in values:
            print(f'\t{value}')
        input()

    @staticmethod
    def get_code():  # pragma: no cover
        while Writer.is_running:
            cls()
            print('Select code (enter index of code)')
            codes = [code.name for code in Code]
            index = 0
            for code in codes:
                index += 1
                print(f'{index}. {code}')
            user_input = Writer.ask_for_input(len(codes))

            code_name = codes[user_input - 1]
            code = Code[code_name]
            return code


if __name__ == '__main__':
    Writer.start()
