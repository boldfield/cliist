cliist
======

Todoist commandline client is an asynchronous client for the Todoist todo-list web application.
It currently supports:
- adding/updating tasks
- marking tasks complete
- listing all tasks
- listing project tasks
- queryinig using Todoist query format
- listing all projects and labels

The client is currently tested only with Todoist Premium.

Every listed resultset is cached to the OS. This is helpful when you want to mark tasks completed. 

## After installation
Install via pip:
```bash
pip install -e git+git@github.com:boldfield/cliist.git#egg=master
```

Once installed you can configure cliist: `cliist --configure`

## Examples

### List all tasks for today and that are overdue
Input: `cliist`

Output:

```
Overdue and today
=================
- 12345677 05.07.2014 @ 21:59:59 task 1 that was overdue
- 12345678 06.07.2014 @ 21:59:59 task 2 for today
```

### List the tasks with a search string
Input: `cliist that`

Output:

```
Overdue and today
=================
- 12345677 05.07.2014 @ 21:59:59 task 1 that was overdue
```

### List all projects
Input: `cliist -P`

Output:

```
#Inbox
#Proj1
#Proj2
#Proj3
  #Proj3.1
  #Proj3.2
  #Proj3.3
#Proj4
```

### Add a task for project Proj 1 with due date today and label @happy and of first priority
Input: `cliist -a a very important task @happy #Proj1 %%4` (cliist uses %%4 instead of !!4 because ! is a special character in bash).

Alternetively, you could also input: `cliist -a 'a very important task @happy' --project Proj1 --priority 4`

### Query 
Input: `cliist -q @happy`

Output:

```
@happy
=================
- 12345677 !1 a very important task
- 12345678 12.07.2014 @ 21:59:59 another happy task
```

### Completing tasks

First we add three types of tasks. Input:


```
cliist -a -d today normal task
cliist -a -d 'ev day' recurring task
cliist -a something for the future 
```

List all tasks for today and tomorrow. Input: `cliist -q 'today, tomorrow'`

Output:

```
today, tomorrow
===============
  - 12345671 28.10.2014 @ 23:59:59   some task from before
  - 12345672 28.10.2014 @ 23:59:59   another some task from before
  - 12345673 28.10.2014 @ 23:59:59   normal task
  - 12345673 28.10.2014 @ 23:59:59   recurring task
```

Complete two tasks via ID. Input: `cliist -c 12345672 12345671`
You can also use a search string. Input: `cliist -c 'normal task'`
The complete command also works with recurring tasks but ***only if the task appeared in the last listing command***. If it didn't, the task will be marked completed and will not appear on the next recurring date.

Let's list the tasks again. Input: ``

Output:

```
today, tomorrow
===============
  - 12345673 29.10.2014 @ 23:59:59   recurring task
```

***Warning***: Search string can only be used if you used a listing command before and the task appeared in the list. In this example we used `cliist -q 'today, tomorrow'` before.



## All features
cliist features can be easily listed with `cliist -h`:
```
cliist -h                                                                                                                                                                [17:48:41]
Usage: cliist [options] task_content|search_string|task_id

Simple Todoist console client. If no options and arguments specified, all
uncompleted tasks for today and overdue are listed. Note: because ! is a
special bash character, you can write %% instead of !!

Options:
  -h, --help            show this help message and exit
  -d DATE, --date=DATE  Todoist due date formatted in Todoist date format.
                        Available when no other options specified and when
                        adding or editing tasks.
  -s ORDER, --sort=ORDER
                        Sort todoist tasks by content (c), priority (p) or due
                        date (d). Available every time a list of tasks is
                        listed.
  -r, --reverse         Reverse the list. Available every time tasks, projects
                        or labels are listed.
  -e EDIT_ID, --edit=EDIT_ID
                        Edit specified task content. Specify content with
                        arguments.
  -q QUERY, --query=QUERY
                        Query tasks using Todoist search queries as arguments.
  -c, --complete        Mark tasks completed (arguments are task ids or search
                        queries).
  -a, --add             Todoist add task where content as arguments.
  -L, --labels          List Todoist labels.
  -P, --projects        List Todoist projects.
  -p PROJECT_NAME, --project-tasks=PROJECT_NAME
                        List Todoist project tasks.
  -A, --all             List all uncompleted todoist tasks.
  --gte=GTE_DATE        List tasks with due date greater or equal than
                        GTE_DATE
  --lte=LTE_DATE        List tasks with due date less or equal to LTE_DATE
  --gt=GT_DATE          List tasks with due date greater than GT_DATE
  --lt=LT_DATE          List tasks with due date less than LT_DATE
  --eqaul=EQ_DATE       List tasks with due date equal to EQ_DATE
  --not-equal=NEQ_DATE  List tasks with due date not equal to NEQ_DATE
  --cached              List cached resultset.
  -o TASK_PROJECT, --project=TASK_PROJECT
                        New task project (available only when adding a task).
  -i TASK_PRIORITY, --priority=TASK_PRIORITY
                        New task priority (available only when adding a task).  
  --format=FORMAT       Select output format (default plain). Formats: plain,
                        org
  --configure           Configure cliist.
```
