from engine.lexer import Lexer
from engine.parser import Parser
from engine.exceptions import SQLError

class ValidatorEngine:
    @staticmethod
    def validate_query(sql_text):
   
    
        lexer = Lexer(sql_text)
        tokens = []

        # ---------- LEXING ----------
        while True:
            token = lexer.get_next_token()
            
            # Lexer error
            if isinstance(token, SQLError):
                return {
                    "status": "INVALID",
                    "phase": "LEXING",
                    "error": {
                        "message": token.msg,
                        "line": token.line,
                        "column": token.column,
                        "hint": token.detail
                    },
                    "tokens": None
                }

            tokens.append(token)
            if token.type.name == 'EOF':
                break

        # ---------- PARSING ----------
        parser = Parser(tokens)
        parse_result = parser.parse()

        if isinstance(parse_result, SQLError):
            return {
                "status": "INVALID",
                "phase": "PARSING",
                "error": {
                    "message": parse_result.msg,
                    "line": parse_result.line,
                    "column": parse_result.column,
                    "hint": parse_result.detail
                },
                "tokens": tokens
            }

        # ---------- SUCCESS ----------
        return {
            "status": "VALID",
            "phase": "COMPLETE",
            "error": None,
            "tokens": tokens
        }


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
    @staticmethod
    def build_text_report(result, query):
        """Creates formatted text output for files."""
        
        report = []
        report.append("SQL QUERY VALIDATION REPORT")
        report.append("=" * 40)
        report.append(f"Query : {query}\n")

        # STATUS HEADER ⭐
        report.append(f"QUERY STATUS : {result['status']}")
        report.append("-" * 40)

        # If INVALID → show error only
        if result["status"] == "INVALID":
            err = result["error"]
            report.append(f"Phase   : {result['phase']}")
            report.append(f"Message : {err['message']}")
            report.append(f"Line    : {err['line']}")
            report.append(f"Column  : {err['column']}")
            report.append(f"Hint    : {err['hint']}")
            return "\n".join(report)

        # If VALID → show tokens ⭐
        report.append("\nLEXING OUTPUT (TOKENS)")
        report.append("-" * 40)

        for t in result["tokens"]:
            report.append(f"{t.type.name:<15} -> {t.value}")

        report.append("\nPARSING RESULT : SUCCESS")

        return "\n".join(report)

        