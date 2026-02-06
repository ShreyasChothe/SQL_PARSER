from enum import Enum, auto

class TokenType(Enum):
    """Enumeration of all possible SQL token types."""
    # --- Keywords ---
    # Data Manipulation (DML)
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    INSERT = auto()
    INTO = auto()
    VALUES = auto()
    UPDATE = auto()
    SET = auto()
    DELETE = auto()
    
    # Data Definition (DDL)
    CREATE = auto()
    TABLE = auto()
    DROP = auto()
    ALTER = auto()
    ADD = auto()
    
    # Clauses & Logic
    JOIN = auto()
    ON = auto()
    GROUP = auto()
    BY = auto()
    ORDER = auto()
    HAVING = auto()
    LIMIT = auto()
    AS = auto()
    DISTINCT = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IN = auto()
    IS = auto()
    NULL = auto()

    # Data Types
    INT = auto()
    INTEGER = auto()
    VARCHAR = auto()
    TEXT = auto()
    BOOLEAN = auto()
    DATE = auto()

    # --- Literals & Identifiers ---
    IDENTIFIER = auto()  # Table names, column names
    NUMBER = auto()      # 10, 3.14
    STRING = auto()      # 'Hello' or "World"

    # --- Operators & Punctuation ---
    ASTERISK = auto()    # *
    COMMA = auto()       # ,
    SEMICOLON = auto()   # ;
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    EQUALS = auto()      # =
    NOT_EQUALS = auto()  # != or <>
    LESS = auto()        # <
    LESS_EQUALS = auto() # <=
    GREATER = auto()     # >
    GREATER_EQUALS = auto() # >=
    PLUS = auto()        # +
    MINUS = auto()       # -
    SLASH = auto()       # /

    # --- Special ---
    EOF = auto()         # End Of File (Signal that we are done)

# This dictionary maps the SQL string to our TokenType
# We use this in the Lexer to distinguish Keywords from Identifiers
KEYWORDS = {
    'SELECT': TokenType.SELECT,
    'FROM': TokenType.FROM,
    'WHERE': TokenType.WHERE,
    'INSERT': TokenType.INSERT,
    'INTO': TokenType.INTO,
    'VALUES': TokenType.VALUES,
    'UPDATE': TokenType.UPDATE,
    'SET': TokenType.SET,
    'DELETE': TokenType.DELETE,
    'CREATE': TokenType.CREATE,
    'TABLE': TokenType.TABLE,
    'DROP': TokenType.DROP,
    'ALTER': TokenType.ALTER,
    'ADD': TokenType.ADD,
    'JOIN': TokenType.JOIN,
    'ON': TokenType.ON,
    'GROUP': TokenType.GROUP,
    'BY': TokenType.BY,
    'ORDER': TokenType.ORDER,
    'HAVING': TokenType.HAVING,
    'LIMIT': TokenType.LIMIT,
    'AS': TokenType.AS,
    'DISTINCT': TokenType.DISTINCT,
    'AND': TokenType.AND,
    'OR': TokenType.OR,
    'NOT': TokenType.NOT,
    'IN': TokenType.IN,
    'IS': TokenType.IS,
    'NULL': TokenType.NULL,
    'INT': TokenType.INT,
    'INTEGER': TokenType.INTEGER,
    'VARCHAR': TokenType.VARCHAR,
    'TEXT': TokenType.TEXT,
    'BOOLEAN': TokenType.BOOLEAN,
    'DATE': TokenType.DATE,
}