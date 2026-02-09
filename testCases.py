# test_runner.py
from engine.lexer import Lexer
from engine.parser import Parser
from engine.exceptions import SQLError

test_cases = [
    ("SELECT id FROM users;", "Simple Select"),
    ("SELECT * FRO users;", "Keyword Typo"),
    ("UPDATE users SET val = 1 WHERE id = (SELECT id FROM t2);", "Update with Subquery"),
    ("INSERT INTO t1 (id) VALUES (1", "Missing Paren in Insert"),
    ("SELECT 10.5.2 FROM table;", "Bad Decimal"),
    ("DELETE FROM users WHERE id = 'active';", "Delete with String")
]

def run_tests():
    passed = 0
    failed = 0
    
    print(f"{'TEST CASE':<50} | {'STATUS':<10}")
    print("-" * 65)
    
    for sql, description in test_cases:
        lexer = Lexer(sql)
        tokens = []
        token_err = False
        
        # Lexing phase
        while True:
            t = lexer.get_next_token()
            if isinstance(t, SQLError):
                token_err = True
                break
            tokens.append(t)
            if t.type.name == 'EOF': break
        
        if token_err:
            print(f"{description:<50} | ❌ LEX ERR")
            failed += 1
            continue

        # Parsing phase
        parser = Parser(tokens)
        result = parser.parse()
        
        if isinstance(result, SQLError):
            print(f"{description:<50} | ❌ PARSE ERR")
            failed += 1
        else:
            print(f"{description:<50} | ✅ PASS")
            passed += 1

    print("-" * 65)
    print(f"TOTAL: {len(test_cases)} | PASSED: {passed} | FAILED: {failed}")

if __name__ == "__main__":
    run_tests()