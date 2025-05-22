
from datetime import datetime
import locale

from NKDatabase.NKPostgres.PostgreSQL import connect, load_config, select_with_conditions

class Parameter:
    '''
    Purpose:
    Class for holding paremeter
    Contains:
    parameter -> (str) name of parameter
    value -> (any) value of parameter
    '''
    def __init__(self, name:str, value:any):
        self.parameter = name
        self.value = value

def get_initial_values(appname: str='', debugging: bool=False):
    '''
    Purpose:
    Get constants for application

    Argument:
    appname -->  name of application (id in table row)

    returns a list of class values containing name and value of contsnats/parameters
    '''

    if appname is not None and len(appname) > 0:
        config = load_config()
        connection = connect(config)
        if connection:
            parameters = []
            #   Select the values from the database
            where_conditions = {'id': appname, 'debugmode': debugging}
            results = select_with_conditions(connection, 'public', 'nkinitvalues', where_conditions)
            for result in results:
                parameter = get_parameter(result)
                if parameter:
                    parameters.append(parameter)
            return parameters
    return None

def get_parameter(row):
    '''
    Purpose extract class Parameter from database row
    Parameter:
    row -> db record
    Return a list of Parameter
    '''
    if row:
        match row['type_id']:
            case 1:
                value = str(row['value'])
            case 2:
                value = int(row['value'])
            case 3:
                value = locale.atof(row['value'])
            case 4:
                val = row['value'].lower()
                if val in ('y', 'yes', 't', 'true', 'on', '1', 'ja'):
                    value = True
                else:
                    value = False
            case 5:
                value = row['value'].split(',')
            case 6:
                vals = row['value'].split(',')
                value=[]
                for val in vals:
                    value.append(int(val))
            case 7:
                vals = row['value'].split(',')
                value=[]
                for val in vals:
                    value.append(locale.atof(val))
            case 8:
                value = parse_date(row['value'])
            case _:
                return None

        parameter = Parameter(name=row['name'], value=value)
        return parameter
    return None


def parse_date(date_str):
    """
    parse_date(date_str)
    Parses a string to datetime

    Parameters:
    date_str:   text to convert or parse to datetime

    returns: datetime object
    if None parse failed
    """

    date_formats = ["%d-%m-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y"]  # List of possible date formats
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized for date: {date_str}")


def get_config(appname: str='', debugging: bool=False):
    '''
    Purpose:
    Get constants for application

    Argument:
    appname -->  name of application (id in table row)
    debugging --> indicates whether values fetched are for production or debugging.   Default is False

    returns a list of class values containing name and value of contsnats/parameters
    '''

    if appname is not None and len(appname) > 0:
        # print(f'looking up valujes for {appname}')
        constants = {}
        config = load_config()
        connection = connect(config)
        if connection:
            # print(f'connection established')
            #   Select the values from the database
            where_conditions = {'id': appname, 'debugmode': debugging}
            rows = select_with_conditions(connection, 'public', 'nkinitvalues', where_conditions)
            for row in rows:

                constants[row['name']] = get_parameter_value(row)
            return constants
    return None

def get_parameter_value(row):
    '''
    Purpose extract class Parameter from database row
    Parameter:
    row -> db record
    Return a list of Parameter
    '''
    if row:
        match row['type_id']:
            case 1:
                value = str(row['value'])
            case 2:
                value = int(row['value'])
            case 3:
                value = locale.atof(row['value'])
            case 4:
                val = row['value'].lower()
                if val in ('y', 'yes', 't', 'true', 'on', '1', 'ja'):
                    value = True
                else:
                    value = False
            case 5:
                value = row['value'].split(',')
            case 6:
                vals = row['value'].split(',')
                value=[]
                for val in vals:
                    value.append(int(val))
            case 7:
                vals = row['value'].split(',')
                value=[]
                for val in vals:
                    value.append(locale.atof(val))
            case 8:
                value = parse_date(row['value'])
            case _:
                return None

        return value
    return None


class Configuration:
    """
    Singleton class to encapsulate the configuration settings for the entire application.
    """
    def __init__(self, appname: str='', debugging: bool=False,
                 named_attributes: bool = False):
        self.named_attributes = named_attributes
        self.initialized = True
        self.configs:dict = get_config(appname=appname, debugging=debugging)
        self.set_constants()
    def set_constants(self):
        """
        Class method to set the constants dynamically.

        Purpose:
            Pass the key-value pairs to the Configuration instance, and the class will update the values.
        """
        if self.configs:
            if not self.named_attributes:
                for key, value in self.configs.items():
                    setattr(self, key, value)
            else:
                for key, value in self.configs.items():
                    if hasattr(self, key):
                        setattr(self, key, value)