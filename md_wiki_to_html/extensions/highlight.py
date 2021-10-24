from typing import Any

from markdown import Markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.extensions import Extension


class HighlightExtension(Extension):
    """
    This will ==highlight some text==
    """

    def extendMarkdown(self, md: Markdown) -> None:
        md.inlinePatterns.register(
            SimpleTagInlineProcessor("()==(.*?)==", "mark"), "highlight", 175
        )
