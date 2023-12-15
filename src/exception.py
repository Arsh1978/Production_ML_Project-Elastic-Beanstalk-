import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    #the sys.exc_info() has three values in tuple: 1) error type 2) error value 3) traceback object and we are using only the traceback object.
    #the traceback object has three values in tuple: 1) traceback object 2) line number 3) file name 4) function name
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):  #here :sys is used as type hint for error_detail
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message

# #Testing
# if __name__ == "__main__":
#    try:
#        a=1/0
#    except Exception as e:
#        logging.info("Divide by zero error")
#        raise CustomException("this is a custom exception",sys)