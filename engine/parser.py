import logging
from engine.tokens import TokenType
from engine.exceptions import SQLError

logger = logging.getLogger("SQLValidator")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if tokens else None
        self.error = None

    def advance(self):
        """Move to the next token in the list."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        return self.current_token
    
    def eat(self, token_type):
        """
        Compare the current token type with expected type.
        If they match, 'eat' it and move to next one.
        If not, raise error
        """
        if self.current_token.type == token_type:
            logger.info(f"Matched {token_type}")
            self.advance()
            return None

        else:
            # This is where SQLError obj comes in
            error_msg = f"Expected {token_type}, but got {self.current_token.type}"
            logger.error(error_msg)
            self.error = SQLError(
                message=f"Syntax Error : Expected {token_type.name}",
                line=self.current_token.line,
                column=self.current_token.column,
                detail=f"Found '{self.current_token.value}' instead of the required keyword/symbol."
            )
            return self.error

    def parse(self):
            """The main entry point that decides which statement to parse."""
            if self.current_token.type == TokenType.SELECT:
                return self.parse_select()
            elif self.current_token.type == TokenType.INSERT:
                return self.parse_insert()
            elif self.current_token.type == TokenType.UPDATE:
                return self.parse_update()
            elif self.current_token.type == TokenType.DELETE:
                return self.parse_delete()
            else:
                return SQLError(message=f"Unsupported statement start: {self.current_token.type.name}")

    def parse_select(self):
        
        if self.eat(TokenType.SELECT): return self.error
        
        # Handle columns
        if self.current_token.type == TokenType.ASTERISK:
            self.eat(TokenType.ASTERISK)
        elif self.current_token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                if self.current_token.type != TokenType.IDENTIFIER:
                    return SQLError("Expected column name after ','", self.current_token.line, self.current_token.column)
                self.eat(TokenType.IDENTIFIER)
        else:
            return SQLError(message="Expected column name or '*' after SELECT", line=self.current_token.line, column=self.current_token.column)

        if self.eat(TokenType.FROM): return self.error
        
        if self.eat(TokenType.IDENTIFIER): return self.error

        if self.current_token.type == TokenType.WHERE:
            err = self._handle_where_clause()
            if err: return err
        
        # Optional Semicolon
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
            
        return "SUCCESS"
    
    def parse_insert(self):
        # Rule: INSERT INTO <table> (col1, col2) VALUES (val1, val2);
        
        if self.eat(TokenType.INSERT): return self.error
        if self.eat(TokenType.INTO): return self.error
        if self.eat(TokenType.IDENTIFIER): return self.error # Table name
        
        # Column List: (id, name)
        if self.eat(TokenType.LPAREN): return self.error
        if self.eat(TokenType.IDENTIFIER): return self.error
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            if self.eat(TokenType.IDENTIFIER): return self.error
        if self.eat(TokenType.RPAREN): return self.error
        
        if self.eat(TokenType.VALUES): return self.error
        
        # Values List: ('1', 'John')
        if self.eat(TokenType.LPAREN): return self.error
        # Here we allow STRING or NUMBER
        if self.current_token.type in [TokenType.STRING, TokenType.NUMBER]:
            self.advance()
        else:
            return SQLError("Expected value in VALUES clause", self.current_token.line, self.current_token.column)
            
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            if self.current_token.type in [TokenType.STRING, TokenType.NUMBER]:
                self.advance()
            else: return self.error
            
        if self.eat(TokenType.RPAREN): return self.error
        return "SUCCESS"
    
    def parse_delete(self):
        if self.eat(TokenType.DELETE): return self.error
        if self.eat(TokenType.FROM): return self.error
        if self.eat(TokenType.IDENTIFIER): return self.error
        
        # Optional WHERE clause
        if self.current_token.type == TokenType.WHERE:
            err = self._handle_where_clause()
            if err: return err
            
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return "SUCCESS"    

    def parse_update(self):
        if self.eat(TokenType.UPDATE): return self.error
        if self.eat(TokenType.IDENTIFIER): return self.error
        if self.eat(TokenType.SET): return self.error
        
        # Handle col = val
        if self.eat(TokenType.IDENTIFIER): return self.error
        if self.eat(TokenType.EQUALS): return self.error
        if self.current_token.type in [TokenType.STRING, TokenType.NUMBER]:
            self.advance()
        else:
            return SQLError("Expected value after '='", self.current_token.line, self.current_token.column)

        # Optional WHERE clause
        if self.current_token.type == TokenType.WHERE:
            err = self._handle_where_clause()
            if err: return err

        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return "SUCCESS"

# Inside core/parser.py

    def _handle_value_or_subquery(self):
        """Handles a literal value OR a nested (SELECT ...) query."""
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            
            # RECURSION: Start parsing as a SELECT statement again!
            # This allows SELECT * FROM (SELECT * FROM ...)
            result = self.parse_select() 
            if isinstance(result, SQLError): return result
            
            if self.eat(TokenType.RPAREN): return self.error
            return None
        
        # Otherwise, it's just a normal value
        if self.current_token.type in [TokenType.STRING, TokenType.NUMBER, TokenType.IDENTIFIER]:
            self.advance()
            return None
            
        return SQLError("Expected value or subquery", self.current_token.line, self.current_token.column)

    def _handle_where_clause(self):
        """Updated WHERE to support 'IN' or subqueries."""
        self.eat(TokenType.WHERE)
        if self.eat(TokenType.IDENTIFIER): return self.error
        
        # Support for '=' or 'IN'
        if self.current_token.type in [TokenType.EQUALS, TokenType.IN]:
            self.advance()
            return self._handle_value_or_subquery()
            
        return SQLError("Expected operator (=, IN) in WHERE clause", self.current_token.line, self.current_token.column)