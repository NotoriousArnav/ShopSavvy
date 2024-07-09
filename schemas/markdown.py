from pydantic import BaseModel
import markdown

class MarkdownModel(BaseModel):
        content: str

        class Config:
                schema_extra = {
                        "example": {
                            "content": "Hello **bold** and [link](https://www.example.com)"
                    }
                }

        def to_markdown(self):
            return markdown.markdown(self.content)
