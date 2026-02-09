import logging
from engine.tokens import TokenType, KEYWORDS
from engine.exceptions import SQLError

logger = logging.getLogger("SQLValidator")

class Token:
    """The Individual unit produced by the Lexer."""
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}' at {self.line} : {self.column})"
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if text else None

    def advance(self):
        """Move to the next char in the text."""
        if self.current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None            # text is finished

    def get_next_token(self):
        """"The 'Engine' which finds the next token!!"""
        while self.current_char is not None:

            start_col = self.column
            start_line = self.line

            # 1. Skip Whitespace
            if self.current_char.isspace():
                self.advance()
                continue
            
            # 2. Handle Keywords / Identifiers (Words)
            if self.current_char.isalpha() or self.current_char == '_':
                word_text = self._handle_word()
                t_type = KEYWORDS.get(word_text.upper(), TokenType.IDENTIFIER)
                return Token(t_type, word_text, start_line, start_col)
            
            # handle Numbers
            if self.current_char.isdigit():
                return self._handle_number()
            
            # handle Strings (single quotes)
            if self.current_char == "'":
                return self._handle_string()

            # 3. Handle Operator
            if self.current_char == "*":
                self.advance()
                return Token(TokenType.ASTERISK, '*', start_line, start_col)
            
            if self.current_char == ",":
                self.advance()
                return Token(TokenType.COMMA, ',', start_line, start_col)
            
            if self.current_char == "=":
                self.advance()
                return Token(TokenType.EQUALS, '=', start_line, start_col)
            
            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, '(', start_line, start_col)
            
            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ')', start_line, start_col)
            
            if self.current_char == ";":
                self.advance()
                return Token(TokenType.SEMICOLON, ';', start_line, start_col)
            
            logger.error(f"Unknown Character Found : {self.current_char}")
            return SQLError(
                message=f"Unknown Character '{self.current_char}' found!",
                line=self.line,
                column=self.column,
                detail="Unknown Character has been detected!")
        
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def _handle_word(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        return result
    
    def _handle_number(self):
        result = ""
        decimal_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                decimal_count += 1
                if decimal_count > 1:
                    logger.error("Invalid Number Format : multiple decimal points")
                    return SQLError(
                        message="Invalid Number Format",
                        line=self.line,
                        column=self.column,
                        detail="Decimal Number can't have more that one decimal point '.' ."
                    )
                
            result += self.current_char
            self.advance()
        
        return Token(TokenType.NUMBER, float(result) if decimal_count > 0 else int(result), self.line, self.column)
    
    def _handle_string(self):
        result = ""

        self.advance()

        while self.current_char is not None and self.current_char != "'":
            result += self.current_char
            self.advance()

        if self.current_char == "'":
            self.advance()
            return Token(TokenType.STRING, result, self.line, self.column)
        else:
            logger.error("Lexer Error : Unterminated string literal")
            return SQLError(
                message="Unterminated String Literal",
                line=self.line,
                column= self.column,
                detail="Make sure you closed your single quotes (')."
            )