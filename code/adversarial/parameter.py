
# coding: utf-8

# In[ ]:

#from __future__ import division
#from __future__ import print_function

import json
import collections

__author__ = 'David'

"""Generic classes and functions for creating configuration parameters."""

# Different parameter types
MULTI = 'multiple_params'
SINGLE = 'single_param'
OPTIONS = 'option_group'


class Parameter:

    def __init__(self, name=None, description=None, tuning_tip=None, values=None, default_value=None):
        self.name = name
        self.description = description
        self.tuning_tip = tuning_tip
        self.values = values
        self.default_value = default_value

        if self.values is None and self.default_value is not None:
            self._param_type = SINGLE
        elif self.values is not None and self.default_value is None:
            self._param_type = MULTI
        elif self.values is not None and self.default_value is not None:
            self._param_type = OPTIONS
        else:
            raise ValueError('At least one of "values" and "default_value" must be specified.')

        self._values = None if values is None else {val.name: val for val in values}
        self._default_value = default_value
        self._value = default_value

    def to_dict(self):
        """Convert parameter tree to nested dictionaries."""
        d = {}
        d['name'] = '' if self.name is None else self.name
        d['description'] = '' if self.description is None else self.description
        d['tuning_tip'] = '' if self.tuning_tip is None else self.tuning_tip
        d['default_value'] = '' if self._default_value is None else self._default_value
        d['value'] = '' if self._value is None else self._value
        if self._values is None:
            d['values'] = ''
        else:
            d['values'] = []
            for child_param in self._values.values():
                d['values'].append(child_param.to_dict())
        return d

    def to_json(self):
        """Convert parameter tree to JSON."""
        return json.dumps(self.to_dict())

    def get_values(self):
        return self._values

    def get_value(self, name=None):
        """Return specified child parameter, current child parameter option, or value depending on param type."""
        if self._param_type == OPTIONS:
            return self._values[self._value]
        elif self._param_type == MULTI:
            return self._values[name]
        else:
            return self._value

    def set_value(self, value):
        if self._param_type != MULTI:
            self._value = value
        return self

    def get_options(self):
        if self._param_type == OPTIONS:
            return self._values.keys()
        else:
            return None

    def print_values(self):
        """Print tree of active parameters."""
        self._traverse(action='print')

    def restore_defaults(self):
        """Restore all values to default."""
        self._traverse(action='restore_default')

    def _print_value(self, depth):
        if self._param_type == SINGLE:
            print('{}{}: {}'.format(''.join(['|\t']*depth), self.name, self._value))
        else:
            print('{}{}'.format(''.join(['|\t']*depth), self.name))

    def _restore_default(self):
        self._value = self._default_value

    def _traverse(self, depth=0, action=None):
        if action == 'print':
            self._print_value(depth)
        elif action == 'restore_default':
            self._restore_default()

        if self._param_type == OPTIONS:
            self._values[self._value]._traverse(depth=depth+1, action=action)
        elif self._param_type == MULTI:
            for value in self._values.values():
                value._traverse(depth=depth+1, action=action)


def params_from_dict(param_dict):
    name = None if param_dict['name'] == '' else param_dict['name']
    description = None if param_dict['description'] == '' else param_dict['description']
    tuning_tip = None if param_dict['tuning_tip'] == '' else param_dict['tuning_tip']
    default_value = None if param_dict['default_value'] == '' else param_dict['default_value']
    value = None if param_dict['value'] == '' else param_dict['value']
    if param_dict['values'] == '':
        values = None
    else:
        values = []
        for child_param in param_dict['values']:
            values.append(params_from_dict(child_param))
    param = Parameter(name, description, tuning_tip, values, default_value).set_value(value)
    return param


def params_from_json(json_string):
    param_dict = json.loads(json_string)
    return params_from_dict(param_dict)

