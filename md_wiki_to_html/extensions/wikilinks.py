from markdown import Markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.extensions import Extension
from markdown.extensions.wikilinks import (
    WikiLinkExtension as BaseWikiLinkExtension,
    WikiLinksInlineProcessor,
)


WIKILINK_RE = r"\[\[([\w0-9_ -\/]+)\]\]"


class WikiLinkExtension(BaseWikiLinkExtension):
    """
    Extends the WikiLinkExtension in python-markdown with one that supports "/" in links
    """

    def extendMarkdown(self, md: Markdown) -> None:
        pattern = WikiLinksInlineProcessor(WIKILINK_RE, self.getConfigs())
        pattern.md = md
        md.inlinePatterns.register(pattern, "wikilink", 70)
