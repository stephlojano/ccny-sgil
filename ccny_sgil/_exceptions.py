class CredentialsError(Exception):
    '''Exception raised when credentials are invalid'''
    def __init__(self):
        self.message = 'Credentials are invalid'
        super().__init__(self.message)
    
class CredentialsFileError(Exception):
    '''Exceptioni raised when credentials file is not found'''
    def __init__(self, path_to_file):
        self.message = f'{path_to_file} was not found. Does it exist?'
        super().__init__(self.message)

class CredentialsMissing(Exception):
    '''Exception raised when credentials are not passed into here_APi object'''
    def __init__(self):
        self.message = 'Missing Credentials or Credentials File'
        super().__init__(self.message)

class EnergyModelError(Exception):
    '''Exception raised when missing arguments in building energy consumption model'''
    def __init__(self, speed, energy_consumption, model):
        if speed is None and energy_consumption is None and model is None:
            self.message = 'Missing speed and energy_consumption or energy consumption model (model)'
        elif speed is not None and energy_consumption is None:
            self.message = 'Missing energy_consumption to build energy consumption model'
        elif speed is None and energy_consumption:
            self.message = 'Missing speed to build energy consumption model'
        elif len(speed) != len(energy_consumption):
            self.message = 'speed and energy_consumption must be of the same length'
        else: 
            self.message = 'Missing argument'
        super().__init__(self.message)

class ResponseError(Exception):
    '''Exception raised when there are no results to return'''
    def __init__(self):
        self.message = 'There was no response from here API - did you make a request?'
        super().__init__(self.message)

def warning_format(message, category, filename, lineno, line=''):
    return '\n' + str(filename) + ': line' + str(lineno) + ': ' + category.__name__ + ': ' +str(message) + '\n'