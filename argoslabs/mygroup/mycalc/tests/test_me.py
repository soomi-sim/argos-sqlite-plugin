#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.mygroup.mycalc`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import unittest
import sqlite3
from argoslabs.mygroup.mycalc import SQLManager
from argoslabs.mygroup.mycalc import _main


################################################################################
TEST_DATA_1 = 'CREATE TABLE Book2' \
              '(book_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,'\
              'title text, isbn int, author text, price int);'
TEST_DATA_2 = "INSERT INTO Book2 (title, isbn, author, price)" \
              " VALUES ('abc', 123, 'def', 1000);"
TEST_DATA_3 = "INSERT INTO Book2 (title, isbn, author, price)" \
              " VALUES ('abc', 123, 'def', 5000);"
TEST_DATA_4 = "INSERT INTO Book2 (title, isbn, author, price)" \
              " VALUES ('abc', 123, 'def', 5000);"
TEST_DATA_5 = 'UPDATE Book2 SET price = 10000 WHERE book_id = 3'
TEST_DATA_6 = '4,\'ccc\',123,\'ccc\',5000'


class TestSQL(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = SQLManager(":memory:")

    def test_010_sql_str(self):
        result = self.manager.sql_str(TEST_DATA_1)
        result = self.manager.sql_str(TEST_DATA_2)
        result = self.manager.sql_str(TEST_DATA_3)
        result = self.manager.sql_str(TEST_DATA_4)
        result = self.manager.sql_str(TEST_DATA_5)
        result = self.manager.show('Book2')
        self.assertTrue(result)

    def test_020_csv_input(self):
        result = self.manager.sql_str(TEST_DATA_1)
        result = self.manager.sql_str(TEST_DATA_2)
        result = self.manager.sql_str(TEST_DATA_3)
        result = self.manager.sql_str(TEST_DATA_4)
        result = self.manager.sql_str(TEST_DATA_5)
        result = self.manager.csv_input('Book2', TEST_DATA_6)
        result = self.manager.get_all_data('Book2')
        self.assertEqual(4, len(result))

    def test_030_sql_file(self):
        result = self.manager.sql_file('C:/Users/jose_com/Desktop/test/create.txt')
        result = self.manager.sql_file('C:/Users/jose_com/Desktop/test/insert.txt')
        result = self.manager.get_all_data('book3')
        self.assertEqual(3, len(result))
