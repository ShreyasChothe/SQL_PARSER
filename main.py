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
from engine.parser import Parser
from engine.exceptions import SQLError
from engine.tokens import TokenType

# initialize the logging system
logger = setup_logger()

def validate_sql(source_input):
    print(f"\n{"=" * 50}")
    print(f"Validating : {source_input}")
    print(f"\n{"=" * 50}")

    # 1 fetch sql
    raw_sql = FileHandler.read(source_input)
    if not raw_sql:
        print("Error : Could not read input")
        return
    
    # 2 lexical analysis
    lexer = Lexer(raw_sql)
    tokens = []

    while True:
        token = lexer.get_next_token()
        if isinstance(token, SQLError):
            print(f"Lexer Error : {token.to_txt()}")
            return
        
        tokens.append(token)
        if token.type.name == 'EOF':
            break

    # 3 syntax analysis (parsing)
    parser = Parser(tokens)
    result = parser.parse()

    if result == "SUCCESS" and parser.current_token.type != TokenType.EOF:
        if parser.current_token.type != TokenType.SEMICOLON:
            print(f"Error : Unparsed tokens left over : {parser.current_token.value}")
            return 

    if isinstance(result, SQLError):
        print(f"PARSER ERROR : {result.to_txt()}")
        logger.error(f"Validation Failed : {result.msg} at {result.line} : {result.column}")

    else:
        print("SUCCESS : SQL Grammer is Valid")
        logger.info("Validation Successfull!")


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
    # #run_test("SELECT id, name FROM table;")

    # run_test("test/test.txt")

    # #run_test("test/test.json")

    # #run_test("test/bad.txt")
    # validate_sql("SELECT * FRO users;")

    # validate_sql("SELECT id, FROM users;")

    # validate_sql("SELECT id, name FROM employee WHERE id = 10;")

    validate_sql("SELECT name FROM users WHERE id IN (SELECT user_id FROM orders);")

    # Test 2: Double Nested (Deep recursion!)
    validate_sql("SELECT * FROM t1 WHERE id = (SELECT id FROM t2 WHERE x = (SELECT y FROM t3));")
    
    # Test 3: Broken Nested (Missing closing paren)
    validate_sql("SELECT * FROM users WHERE id = (SELECT id FROM staff;")
