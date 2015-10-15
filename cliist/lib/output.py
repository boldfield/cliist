import datetime
import sys

from cliist.lib.config import Config


class Plain:
    COLORS = {
        'project': Config.color('project'),
        'unknown': Config.color('endc'),
        'set': Config.color('endc')
    }
    FORMAT = {
        'task': '{c0}{indent}{c5}{priority:>3.3} {c1}{content}{c0}\n        {c3}{project_name:26.26}{c4} {label_names:26.26} {c2}Due: {due:12.12}\n{c0}',  # nopep8
        'project': '\n{color}#{project_name}\n',
        'unknown': '',
    }

    @staticmethod
    def task(obj):
        indent = '  ' * (int(obj.get('indent', '1')) - 1)
        prio = '  '
        if obj.priority and obj.priority != 1:
            prio = '!' * (obj.priority - 1)
        due = obj.get_date()
        if due:
            due += ' '

        line = Plain.FORMAT['task'].format(c0=Config.color('endc'),
                                           c1=Config.color('content'),
                                           c2=Config.color('date'),
                                           c3=Config.color('project'),
                                           c4=Config.color('label'),
                                           c5=Config.color('priority'),
                                           indent=indent,
                                           priority=prio,
                                           content=obj.get('content'),
                                           project_name=obj.get('project_name'),  # nopep8
                                           label_names=obj.get('label_names'),
                                           due=due,
                                           taskid=obj.get('id'))
        sys.stdout.write(line)

    @staticmethod
    def task_set(obj):
        color = Plain.COLORS[obj.set_type]
        line = Plain.FORMAT[obj.set_type].format(color=color, **obj.raw)
        sys.stdout.write(line)
        for task in obj:
            Plain.task(task)

    @staticmethod
    def result_set(obj):
        if obj.name:
            print('{}{}\n{}{}'.format(Config.color('filter'), obj.name,
                                      ''.join('=' for _ in obj.name or ''),
                                      Config.color('endc')))
        for task_set in obj.task_sets:
            Plain.task_set(task_set)
        if obj.tasks:
            Plain.task_set(obj.tasks)


class Org:
    PRIORITY = {1: '', 2: 'C', 3: 'B', 4: 'A'}
    DATE = 'DEADLINE: <{} {}>'
    NAMES = {
        'project': '{project_name}',
        'unknown': '',
    }

    @staticmethod
    def task(obj, level=2):
        stars = ('*' * (level - 1)) + ('*' * (int(obj.get('indent', '1'))))
        indent = ' ' * (len(stars) + 1)
        prio = Org.PRIORITY[obj.priority or 1]
        due = obj.due_date and Org.DATE.format(obj.due_date.date().isoformat(),
                                               obj.due_date.strftime("%A")[:3])
        props = {
            'TaskID': obj.get('id'),
            'Recurring': obj.is_recurring and 'yes' or 'no',
        }
        if obj.labels:
            props['Labels'] = ', '.join(map(str, obj.labels))
        if obj.project:
            props['Project'] = obj.project
        if obj.date_string:
            props['DateString'] = obj.date_string

        print('{} {} {}{}'.format(stars,
                                  'DONE' if obj.checked else 'TODO',
                                  '[#{}] '.format(prio) if prio else '',
                                  obj.content))
        if due:
            print(indent + due)
        print(indent + ':PROPERTIES:')
        prop_len = max(len(val) for val in props.keys()) + 3
        for prop, value in props.items():
            prop_value = ('{:<' + str(prop_len) + '}{}').format(':{}:'.format(prop), value)  # nopep8
            print(indent + prop_value)
        print(indent + ':END:')

    @staticmethod
    def task_set(obj, level=1):
        name = Org.NAMES[obj.set_type].format(**obj.raw)
        if name:
            print('{} {}'.format('*' * level, name))
        for task in obj:
            Org.task(task, level=(level+1) if name else level)

    @staticmethod
    def result_set(obj):
        level = 1
        if obj.name:
            level = 2
            print('* ' + obj.name)
        for task_set in obj.task_sets:
            Org.task_set(task_set, level=level)
        for task in obj.tasks:
            Org.task(task, level=level)


formaters = {
    'plain': Plain,
    'org': Org
}
