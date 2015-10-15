from datetime import datetime, timedelta
from dateutil import tz, parser as dt_parser
import json
import os.path

from . import output, api

from cliist.lib.config import Config


class Task(dict):
    def __init__(self, task_raw):
        for key, val in task_raw.items():
            self[key] = val

        self.due_date = None
        if task_raw.get('due_date'):
            dd = task_raw['due_date']
            self.due_date = dt_parser.parse(dd)
        sd = self.due_date or datetime(1500, 1, 1)
        self.sort_date = sd.replace(tzinfo=None)

        self.project = task_raw.get('project_id')
        self.priority = int(task_raw.get('priority', '1'))
        self.labels = task_raw.get('labels', [])
        self['project_name'] = projects_dict.get(self.project, '')
        lbls = ' '.join(map(lambda x: labels_dict.get(x), self.labels))
        self['label_names'] = lbls
        self.content = task_raw.get('content', '')
        self.raw = task_raw
        self.date_string = task_raw.get('date_string', '')
        self.is_recurring = any([
            'every ' in (self.date_string or ''),
            'ev ' in (self.date_string or ''),
        ])
        self.in_history = bool(task_raw.get('in_history', 0))
        self.checked = bool(task_raw.get('completed_date', None))

    def serialize(self):
        return json.dumps(self)

    def get_date(self):
        local_zone = tz.tzlocal()
        if self.due_date:
            if Config.get('time_offset'):
                dt = self.due_date.astimezone(local_zone) + timedelta(hours=Config.get('time_offset'))
                return dt.strftime(Config.get('output_date_format'))
            return self.due_date.astimezone(local_zone).strftime(Config.get('output_date_format'))
        return ''

    def get_key(self, order):
        key = getattr(self, order)
        if type(key) == str:
            return key.lower()
        return key

    def __hash__(self):
        return self.get('id')

    def pprint(self, output_engine=output.Plain):
        output_engine.task(self)


class TaskSet(list):
    FILTERS = {
        'gte': lambda v: (lambda i: i.sort_date.date() >= v),
        'lte': lambda v: (lambda i: i.sort_date.date() <= v),
        'gt': lambda v: (lambda i: i.sort_date.date() > v),
        'lt': lambda v: (lambda i: i.sort_date.date() < v),
        'eq': lambda v: (lambda i: i.sort_date.date() == v),
        'neq': lambda v: (lambda i: i.sort_date.date() != v),
        'search': lambda v: (lambda i: v.lower() in i['content'].lower()),
    }

    def __init__(self, result={}, set_type='unknown'):
        if 'project_id' in result:
            self.set_type = 'project'
        else:
            self.set_type = set_type

        for task in result.get('uncompleted', []):
            self.append(Task(task))
        self.raw = result

    def serialize(self):
        return json.dumps(self)

    def copy(self):
        copied = TaskSet(set_type=self.set_type)
        copied.set_type = self.set_type
        copied.extend(self)
        copied.raw = self.raw
        return copied

    def select(self, order=None, reverse=False, search=None, filters={}):
        if search:
            filters['search'] = search
        filtered = self.copy()
        for filtername, filterval in filters.items():
            filtered = filter(TaskSet.FILTERS[filtername](filterval), filtered)
        if order:
            filtered = sorted(filtered, key=lambda task: task.get_key(order))
        filtered = list(filtered)
        selected = TaskSet(set_type=self.set_type)
        selected.raw = self.raw
        for item in (reverse and filtered[::-1] or filtered):
            selected.append(item)
        return selected

    def pprint(self, output_engine=output.Plain):
        output_engine.task_set(self)

    def lookup(self, task_info):
        results = set()
        for task in self:
            if task_info.isdigit():
                task_id = int(task_info)
                if task_id and task_id == int(task.get('id', 0)):
                    results.add(task)
            elif task_info.lower() in task.get('content').lower():
                results.add(task)
        return results


class ResultSet:
    def __init__(self, result, name=None, no_save=False, **options):
        self.task_sets = []
        self.tasks = TaskSet()
        self.name = name
        self.raw = result
        for resultset in result or []:
            if resultset.get('content'):
                self.tasks.append(Task(resultset))
                continue
            for item in resultset['data']:
                if item.get('content'):
                    self.tasks.append(Task(item))
                else:
                    self.task_sets.append(TaskSet(item).select(**options))
        if options:
            self.tasks = self.tasks.select(**options)

        if not no_save:
            self.save()

    def pprint(self, output_engine=output.Plain):
        output_engine.result_set(self)

    def select(self, **options):
        return ResultSet(self.raw, name=self.name, **options)

    def serialize(self):
        dump = {'name': self.name, 'raw': self.raw}
        return json.dumps(dump)

    def save(self):
        if not Config.get('cache_enabled'):
            return None
        with open(Config.get('cache'), 'w') as fd:
            fd.write(self.serialize())

    def lookup(self, task_info):
        sets = [self.tasks] + self.task_sets
        tasks = set()
        for task_set in sets:
            for task_subset in map(lambda s: s.lookup(task_info), sets):
                for task in task_subset:
                    tasks.add(task)
        return list(filter(lambda task: task is not None, tasks))

    def lookup_one(self, task_info):
        tasks = self.lookup(task_info)
        if len(tasks) == 1:
            return tasks[0]
        return None

    @staticmethod
    def load():
        if not Config.get('cache_enabled'):
            return None
        if not os.path.exists(Config.get('cache')):
            return None
        with open(Config.get('cache'), 'r') as fd:
            return ResultSet.deserialize(fd.read())

    @staticmethod
    def deserialize(dumped_str):
        dump = json.loads(dumped_str)
        return ResultSet(dump['raw'],
                         name=dump['name'], no_save=True)


class LabelDict(dict):

    def __init__(self):
        for name, details in api.api_call('getLabels').items():
            self[details['id']] = '@' + details['name']


class ProjectDict(dict):

    def __init__(self):
        for project in api.api_call('getProjects'):
            self[project['id']] = '#' + project['name']

projects_dict = ProjectDict()
labels_dict = LabelDict()
