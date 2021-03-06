#!/usr/bin/env python3

from optparse import OptionParser

from cliist.lib import process
from cliist.lib.utils import CliistException
from cliist.lib import output

USAGE = "usage: %prog [options] task_content|search_string|task_id"
DESC = """Simple Todoist console client.
If no options and arguments specified, all uncompleted tasks for today and \
overdue are listed.  Note: because ! is a special bash character, you can \
write %% instead of !!
"""


def main():
    parser = OptionParser(usage=USAGE, description=DESC)

    parser.add_option('-d', '--date',
                      dest='date',
                      default=None,
                      help='Todoist due date formatted in Todoist date '
                           'format. Available when no other options specified '
                           'and when adding or editing tasks. If using with '
                           '--archive, date can only be a full iso formatted '
                           'date. Example: 2014-12-1T10:11')

    parser.add_option('-s', '--sort',
                      dest='order',
                      default=None,
                      help='Sort todoist tasks by content (c), priority (p) '
                           'or due date (d). Available every time a list of '
                           'tasks is listed.')

    parser.add_option('-r', '--reverse',
                      dest='reverse',
                      action='store_true',
                      default=False,
                      help='Reverse the list. Available every time tasks, '
                           'projects or labels are listed.')

    parser.add_option('-e', '--edit',
                      dest='edit_id',
                      default=None,
                      help='Edit specified task content. Specify content with '
                           'arguments.')

    parser.add_option('-q', '--query',
                      dest='query',
                      default=None,
                      help='Query tasks using Todoist search queries as '
                           'arguments.')

    parser.add_option('-c', '--complete',
                      dest='complete',
                      action='store_true',
                      default=None,
                      help='Mark tasks completed (arguments are task ids or '
                           'search queries).')

    parser.add_option('-a', '--add',
                      dest='add_task',
                      action='store_true',
                      default=False,
                      help='Todoist add task where content as arguments.')

    parser.add_option('-L', '--labels',
                      dest='labels',
                      action='store_true',
                      default=False,
                      help='List Todoist labels.')

    parser.add_option('--info',
                      dest='info',
                      action='store_true',
                      default=False,
                      help='Add aditional info.')

    parser.add_option('-P', '--projects',
                      dest='projects',
                      action='store_true',
                      default=False,
                      help='List Todoist projects.')

    parser.add_option('-p', '--project-tasks',
                      dest='project_name',
                      default=False,
                      help='List Todoist project tasks.')

    parser.add_option('-A', '--all',
                      dest='all',
                      action='store_true',
                      default=False,
                      help='List all uncompleted todoist tasks.')

    parser.add_option('--archive',
                      dest='archive',
                      action='store_true',
                      help='If -p PROJECT is specified, show only completed '
                           'tasks of that project. Date (-d) will be set as '
                           'from date but it has to be in ISO format.')

    parser.add_option('--limit',
                      dest='limit',
                      default=30,
                      help='Limit returned archive size.')

    parser.add_option('--gte',
                      dest='gte_date',
                      default=None,
                      help='List tasks with due date greater or equal than '
                           'GTE_DATE.')

    parser.add_option('--lte',
                      dest='lte_date',
                      default=None,
                      help='List tasks with due date less or equal to '
                           'LTE_DATE.')

    parser.add_option('--gt',
                      dest='gt_date',
                      default=None,
                      help='List tasks with due date greater than GT_DATE.')

    parser.add_option('--lt',
                      dest='lt_date',
                      default=None,
                      help='List tasks with due date less than LT_DATE.')

    parser.add_option('--eqaul',
                      dest='eq_date',
                      default=None,
                      help='List tasks with due date equal to EQ_DATE.')

    parser.add_option('--not-equal',
                      dest='neq_date',
                      default=None,
                      help='List tasks with due date not equal to NEQ_DATE.')

    parser.add_option('--cached',
                      dest='cached',
                      action='store_true',
                      default=False,
                      help='List cached resultset.')

    parser.add_option('-o', '--project',
                      dest='task_project',
                      default=None,
                      help='New task project (available only when adding a '
                           'task).')

    parser.add_option('-i', '--priority',
                      dest='task_priority',
                      default=False,
                      help='New task priority (available only when adding a '
                           'task).')

    fmts = ', '.join(output.formaters.keys())
    parser.add_option('--format',
                      dest='format',
                      default='plain',
                      help='Select output format (default plain). Formats: '
                           '{}.'.format(fmts))

    parser.add_option('--configure',
                      dest='configure',
                      action='store_true',
                      default=False,
                      help='Configure cliist.')

    options, args = parser.parse_args()
    try:
        process.command(args, options)
    except CliistException as msg:
        print(msg)
