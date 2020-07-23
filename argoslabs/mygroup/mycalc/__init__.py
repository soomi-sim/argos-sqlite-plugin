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
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2019/03/08]
#     - add icon
#  * [2018/11/28]
#     - starting

################################################################################
import os
import sys
import sqlite3
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from simpleeval import simple_eval


################################################################################
class SQLManager:
    def __init__(self, db_filepath):
        self.db_filepath = db_filepath
        self.cur, self.con = self.get_cursor()

    def get_cursor(self):
        con = sqlite3.connect(self.db_filepath)
        cur = con.cursor()
        return cur, con

    def sql_str_values(self, values):
        x = ''
        for val in values:
            for v in val:
                x += (v + ' ')
            self.sql_str(x)

    def sql_str(self, value):
        self.cur.execute(value)
        self.con.commit()
        return True

    def sql_file(self, value_file):
        f = open(value_file)
        data = f.read()
        self.cur.execute(data)
        self.con.commit()
        f.close()

    def csv_input_values(self, db_name, values):
        x = ''
        for i in values:
            x += (i + ' ')
        self.csv_input(db_name, x)

    def csv_input(self, db_name, value):
        self.cur.execute("INSERT INTO {table} VALUES ({val})"
                         .format(table=db_name, val=value))
        self.con.commit()

    # def insert_values(self, db_name, values):
    #     for val in values:
    #         self.insert(db_name, *val)
    #
    # def insert(self, db_name, *args):
    #     self.cur.execute("INSERT INTO {table} VALUES {val}"
    #                      .format(table=db_name, val=args))
    #     self.con.commit()
    #     return True
    #
    # def update_values(self, db_name, values):
    #     for val in values:
    #         self.update(db_name, *val)
    #
    # def update(self, db_name, target2, value2, target, value):
    #     self.cur.execute("UPDATE {table} SET {column} = ? WHERE {column2} = ?"
    #                      .format(table=db_name, column=target, column2=target2),
    #                      (value, value2))
    #     self.con.commit()
    #
    # def delete_values(self, db_name, values):
    #     for val in values:
    #         self.delete(db_name, *val)
    #
    # def delete(self, db_name, target, value):
    #     self.cur.execute("DELETE FROM {table} WHERE {column} = ?"
    #                      .format(table=db_name, column=target), (value, ))
    #     self.con.commit()
    #
    # def create_values(self, db_name, values):
    #     for val in values:
    #         self.delete(db_name, *val)
    #
    # def create(self, db_name, value):
    #     self.cur.execute("CREATE TABLE IF NOT EXISTS  {table} ({column})"
    #                      .format(table=db_name, column=value))
    #     self.con.commit()
    def get_all_data(self, db_name):
        self.cur.execute('select * from {table}'.format(table=db_name))
        rows = self.cur.fetchall()
        return rows

    def show(self, db_name):
        self.cur.execute("SELECT * from {table}".format(table=db_name))
        data = self.cur.fetchall()
        for d in data:
            for i in d:
                print(i, end=' ')
            print(end='\n')
        return True


################################################################################
@func_log
def do_eval(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """

    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.name:
            raise ValueError('Invalid Name')
        if not argspec.filepath:
            raise ValueError('Invalid Filepath')

        manager = SQLManager(db_filepath=argspec.filepath)

        # if argspec.add:
        #     manager.insert_values(argspec.name[0], argspec.add)

        # elif argspec.update:
        #     manager.update_values(argspec.name[0], argspec.update)
        #
        # elif argspec.delete:
        #     manager.delete_values(argspec.name[0], argspec.delete)
        #
        # elif argspec.create:
        #     manager.create_values(argspec.name[0], argspec.create)

        if argspec.sql:
            manager.sql_str_values(argspec.sql)

        elif argspec.csv:
            manager.csv_input_values(argspec.name[0], argspec.csv)

        elif argspec.sqlfile:
            manager.sql_file(argspec.sqlfile)

        manager.show(argspec.name[0])

        mcxt.logger.info('>>>end...')
        return 0

    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1

    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS-DEMO',
        group='mygroup',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='My Calc',
        icon_path=get_icon_path(__file__),
        description='My Calculator',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('-n', '--name', nargs='+', help='DB name to use',
                          display_name='DB Name')
        mcxt.add_argument('-f', '--filepath', display_name='DB file',
                          help='DB file path [[C:/Users/Desktop/Book.db]]')

        # ######################################## for app dependent options
        # mcxt.add_argument('-a', '--add', display_name='insert', nargs='*',
        #                   action='append', help='jkhkj [[jkhkjh]]')
        # mcxt.add_argument('-u', '--update', display_name='update', nargs='*',
        #                   action='append')
        # mcxt.add_argument('-d', '--delete', display_name='delete', nargs='*',
        #                   action='append')
        # mcxt.add_argument('-c', '--create', display_name='new DB', nargs='*',
        #                   action='append')
        mcxt.add_argument('-s', '--sql', display_name='SQL string', nargs='*',
                          action='append', help='SQL String to execute'
                                                '[[INSERT INTO Book VALUES '
                                                '(abc, 123, def, 1000)]]')
        mcxt.add_argument('-sf', '--sqlfile', display_name='SQL file',
                          help='SQL file to execute'
                               ' [[C:/Users/Desltop/test.txt]]')
        mcxt.add_argument('-c', '--csv', display_name='CSV input',
                          help='input data write [[1, \'abc\', 123, \'def\']]',
                          action='append')

        argspec = mcxt.parse_args(args)
        return do_eval(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass

