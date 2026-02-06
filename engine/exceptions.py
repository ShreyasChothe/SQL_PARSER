class SQLError:
    """The object returned when validation fails."""

    def __init__(self, message, line=None, column=None, detail=None):
        self.msg = message
        self.line = line
        self.column = column
        self.detail = detail

    def to_json(self):
        """Perfect for when you want to export the error to a JSON file."""
        return {
            "status": "error",
            "error_info" : {
                "message" : self.msg,
                "location" : f"Line {self.line}, Col {self.column}",
                "hint" : self.detail
            }
        }
    
    def to_txt(self):
        return f"""
        Error Detected : {self.msg}
        \r\rMessage : {self.msg}
        \r\rLocation : Line {self.line}, Col {self.column}
        \r\rHint : {self.detail}"""

    def to_xml(self):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<error>
    <status>error</status>
    <message>{self.msg}</message>
    <location>
        <line>{self.line}</line>
        <column>{self.column}</column>
    </location>
    <hint>{self.detail}</hint>
</error>
"""    
    