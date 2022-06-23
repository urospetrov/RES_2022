import sqlite3
import threading

from constants.codes import Code
from constants.datasets import Dataset
from models.collection_description import CollectionDescription
from models.receiver_property import ReceiverProperty


class Reader:
    def __init__(self, dataset_to_process):  # pragma: no cover
        self.dataset_to_process = dataset_to_process

    def save_data(self, data: CollectionDescription):  # pragma: no cover
        for value in data.historical_collection.receiver_properties:
            if value.code == Code.CODE_DIGITAL:
                self.save_value(value)
            else:
                last_value = self.get_last_value_by_code(value.code)
                if last_value is None:
                    self.save_value(value)
                elif abs(value.receiver_value - last_value) > (last_value * 0.02):
                    self.save_value(value)

    # TODO: Test
    def get_last_value_by_code(self, code: Code):
        while True:
            try:
                lock = threading.Lock()
                lock.acquire()
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                dataset_id = Reader.map_code_to_dataset_id(code)
                query = f"""SELECT VALUE FROM DATASET_{dataset_id} WHERE TIME_CREATED = (SELECT MAX(TIME_CREATED) FROM DATASET_{dataset_id} WHERE CODE='{code.name}') AND CODE='{code.name}'"""
                cur.execute(query)
                result = cur.fetchone()
                con.close()
                lock.release()

                if result is None:
                    return None
                return result[0]
            except:
                self.create_tables()

    # TODO: Test
    def save_value(self, receiver_property: ReceiverProperty):
        try:
            lock = threading.Lock()
            lock.acquire()
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            dataset_id = self.map_code_to_dataset_id(receiver_property.code)
            query = f"""INSERT INTO DATASET_{dataset_id} (CODE, VALUE) VALUES ('{receiver_property.code.name}', {receiver_property.receiver_value})"""
            cur.execute(query)
            con.commit()
            con.close()
            lock.release()
        except:
            pass

    @staticmethod
    def get_values_by_code(code: Code):
        try:
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            dataset_id = Reader.map_code_to_dataset_id(code)
            query = f"""SELECT VALUE FROM DATASET_{dataset_id} WHERE CODE = '{code.name}'"""
            cur.execute(query)
            values = cur.fetchall()
            cur.close()
            con.close()

            if values is None:
                return []

            actual_values = []
            for value in values:
                actual_values.append(value[0])

            return actual_values
        except:
            pass

    # TODO: Test
    @staticmethod
    def get_values_by_interval(code: Code,
                               start_interval_date: str,
                               start_interval_time: str,
                               end_interval_date: str,
                               end_interval_time: str):
        try:
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            dataset = Reader.map_code_to_dataset_id(code)
            str1 = f'{start_interval_date} {start_interval_time}'
            str2 = f'{end_interval_date} {end_interval_time}'
            query = f"""SELECT VALUE FROM DATASET_{dataset} WHERE CODE = '{code.name}' AND TIME_CREATED > datetime('{str1}') AND TIME_CREATED < datetime('{str2}')"""
            cur.execute(query)
            values = cur.fetchall()
            con.close()
            if values is None:
                return []

            actual_values = []
            for value in values:
                actual_values.append(value[0])
            return actual_values
        except:
            pass

    # TODO: Test
    @staticmethod
    def map_code_to_dataset_id(code: Code):
        if code in Dataset.Dataset_1.value:
            return 1
        elif code in Dataset.Dataset_2.value:
            return 2
        elif code in Dataset.Dataset_3.value:
            return 3
        elif code in Dataset.Dataset_4.value:
            return 4

    @staticmethod
    def create_tables():  # pragma: no cover
        lock = threading.Lock()
        lock.acquire()
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        for dataset_id in range(1, 5):
            query = f"""CREATE TABLE DATASET_{dataset_id}
                        (
                            CODE         TEXT NOT NULL,
                            VALUE        INT  NOT NULL,
                            TIME_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            CONSTRAINT DATASET_{dataset_id}_CH CHECK (DATASET_{dataset_id}.VALUE >= 0)
                        )"""
            cur.execute(query)
        con.close()
        lock.release()

    def __str__(self):  # pragma: no cover
        return f'Reader {self.dataset_to_process}'
