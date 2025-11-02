from symtable import Class

import pytest


@pytest.fixture()
def clear_books_database():
    print("[FIXTURE] Удаляем все данные из базы данных")

@pytest.fixture()
def fill_books_database():
    print("[FIXTURE] Создаем новые данные  в БД")

@pytest.mark.usefixtures('fill_books_database')
def test_read_all_books_in_library():
    print("Reading all books")


@pytest.mark.usefixtures(
    'fill_books_database',
    'clear_books_database'
)
class TestLibrary(object):
    def test_read_all_books_in_library(self):
        print("Reading all books")

    def test_delete_all_books_in_library(self):
        print("Deleting all books")