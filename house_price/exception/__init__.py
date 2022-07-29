import sys

class HousePricePredictionException(Exception):

    def __init__(self, exception: Exception, error_details: sys) -> None:
        self.exception = exception
        self.error_details = error_details
        self.error_message = self.format_error(self)
        super().__init__(self.exception)

    @staticmethod
    def format_error(self) -> str:
        e, p, t = self.error_details.exc_info()
        exception_name = e.__name__
        error_line_numb = t.tb_lineno
        error_file_path = t.tb_frame.f_code.co_filename

        error_message = f'{exception_name} - {p}, at line number {error_line_numb}, in the file {error_file_path}.'

        return error_message

    def __str__(self) -> str:
        return self.error_message
    
    def __repr__(self) -> str:
        return HousePricePredictionException.__name__.__str__()
