import csv
import typing
from _csv import QUOTE_ALL
from abc import abstractmethod, ABCMeta
from pathlib import Path


class IOWriteHandler(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def write(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def setup(cls, **kwargs) -> typing.Union[None, Exception]:
        raise NotImplementedError


class IOReadHandler(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def read(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def setup(cls, **kwargs) -> typing.Union[None, Exception]:
        raise NotImplementedError


class FileHandler:
    path_object = None

    @classmethod
    def set(cls, file_path: str = "", extension: str = "") -> typing.Union[None, Exception]:
        _file = Path(file_path)
        try:
            if cls.validate_file(_file, extension):
                cls.path_object = _file
                return None
            else:
                raise Exception("Invalid file extension")
        except Exception as e:
            return e

    @staticmethod
    def validate_file(path_object: Path, extension: str) -> bool:
        if not (path_object.exists() and path_object.is_file() and path_object.suffix == extension):
            return False
        return True

    @classmethod
    def get_path(cls) -> Path:
        return cls.path_object


class CSVWriteHandler(FileHandler, IOWriteHandler):
    @classmethod
    def write(cls, columns: typing.List[str], rows: typing.List[typing.Dict]):
        with cls.get_path().open("w") as csv_file:
            csv_writer = csv.DictWriter(csv_file, quoting=QUOTE_ALL, escapechar="\\", fieldnames=columns)
            csv_writer.writeheader()
            for row in rows:
                csv_writer.writerow(row)

    @classmethod
    def append(cls, columns: typing.List[str], rows: typing.List[typing.Dict]):
        with cls.get_path().open("a+") as csv_file:
            csv_writer = csv.DictWriter(csv_file, quoting=QUOTE_ALL, escapechar="\\", fieldnames=columns)
            for row in rows:
                csv_writer.writerow(row)

    @classmethod
    def setup(cls, file_path: str = "") -> typing.Optional[Exception]:
        open(file_path, 'w').close()
        return super().set(file_path=file_path, extension=".csv")
