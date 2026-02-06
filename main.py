#---------------------------------------------------------
# Testing Logger : 

#from utils.logger import setup_logger

# #Initialize the logger
# logger = setup_logger()

# logger.info("Project Initialized Succesfully!!")
# logger.debug("This is a debug message for the dev!!")
# logger.error("This is what an error looks like!")
#---------------------------------------------------------

#---------------------------------------------------------
# Testing FileHandler, Lexer :
from utils.logger import setup_logger
from utils.file_handler import FileHandler
from engine.lexer import Lexer
from engine.exceptions import SQLError

# initialize the logging system
logger = setup_logger()

def run_test(source_input):
    print(f"\n---Testinng : {source_input}---")

    # 1. Test File Handler
    raw_sql = FileHandler.read(source_input)
    if not raw_sql :
        logger.error("Could not retrieve SQL content.")
        return
    
    # 2. Test Lexer
    lexer = Lexer(raw_sql)
    tokens = []

    while True:
        token = lexer.get_next_token()

        if isinstance(token, SQLError):
            print(f"Validation Error : {token.to_txt()}")
            break

        tokens.append(token)

        if token.type.name == "EOF":
            print("LEXING SUCCESSFUL")
            for t in tokens:
                print(t)
            break

if __name__ == "__main__":
    #run_test("SELECT id, name FROM table;")
   # str=input("enter the string:")
   # run_test(str)
    #run_test("test/test.txt")

   # run_test("test/test.json")
   run_test("test/test.sql")


    #run_test("test/bad.txt")