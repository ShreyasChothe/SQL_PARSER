from engine.lexer import Lexer
from engine.parser import Parser
from engine.exceptions import SQLError

class ValidatorEngine:
    @staticmethod
    def validate_query(sql_text):
        """Validates a single SQL string and returns (result, tokens)."""
        lexer = Lexer(sql_text)
        tokens = []
        
        while True:
            token = lexer.get_next_token()
            if isinstance(token, SQLError):
                return token, None  # Return error object
            
            tokens.append(token)
            if token.type.name == 'EOF':
                break
        
        # Now pass tokens to Parser
        parser = Parser(tokens)
        parse_result = parser.parse()
        
        if isinstance(parse_result, SQLError):
            return parse_result, tokens
            
        return "SUCCESS", tokens

    @staticmethod
    def batch_validate(queries):
        """Processes a list of queries and categorizes them into successes and errors."""
        results = []
        errors = []
        
        for idx, query in enumerate(queries, start=1):
            status, tokens = ValidatorEngine.validate_query(query)
            
            if isinstance(status, SQLError):
                errors.append({
                    "query_index": idx,
                    "query": query,
                    "message": status.msg,
                    "line": status.line,
                    "column": status.column,
                    "hint": status.detail
                })
            else:
                results.append({
                    "query_index": idx,
                    "query": query,
                    "tokens": [{"type": t.type.name, "value": str(t.value)} for t in tokens]
                })
        
        return results, errors