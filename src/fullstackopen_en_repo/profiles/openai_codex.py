import logging
import re
from pathlib import Path
from urllib.parse import urlparse

from .base import SiteProfile

log = logging.getLogger(__name__)

class OpenAICodexProfile(SiteProfile):
    """
    Profile for crawling developers.openai.com/codex.
    """
    name = "openai-codex"
    domains = ["developers.openai.com"]
    start_urls = ["https://developers.openai.com/docs/codex"]
    max_depth = 10  # Adjust as needed

    def in_scope(self, url: str) -> bool:
        """
        Check if a URL is within the scope of the codex documentation.
        """
        parsed = urlparse(url)
        return (
            parsed.hostname in self.domains
            and (parsed.path == "/docs/codex" or parsed.path.startswith("/docs/codex/"))
        )

    def derive_output_path(self, url: str) -> Path:
        """
        Derive the output path from the URL.
        Example:
        https://developers.openai.com/docs/codex -> <output_root>/openai-codex/index.md
        https://developers.openai.com/docs/codex/introduction -> <output_root>/openai-codex/introduction.md
        """
        parsed = urlparse(self.normalize_url(url))
        path_str = parsed.path.rstrip("/")

        # Remove the base path prefix
        prefix = "/docs/codex"
        if path_str.startswith(prefix):
            path_str = path_str[len(prefix):]

        # If the path is empty, it's the root
        if not path_str:
            return self.output_root / self.name / "index.md"

        # Handle sub-paths
        relative_path = Path(path_str.lstrip("/"))
        
        # If it has a file extension, use it as is
        if relative_path.suffix:
             return self.output_root / self.name / f"{relative_path}.md"

        # Otherwise, treat it as a directory with an index file or a direct .md file
        # Let's check the last part of the segment to decide
        parts = path_str.strip("/").split("/")
        if len(parts) > 0:
            # e.g., /docs/codex/introduction -> openai-codex/introduction.md
            return self.output_root / self.name / f"{'/'.join(parts)}.md"
        else:
             # This case should be covered by the root index.md case above
            return self.output_root / self.name / "index.md"


    def rewrite_link(self, href: str, from_url: str) -> str:
        """
        Rewrite an internal link to be a relative path.
        """
        if not self.is_internal_link(href):
            return href

        # Resolve the href to an absolute URL
        from .link_rewriter import resolve_href_to_absolute_url
        target_url = resolve_href_to_absolute_url(href, from_url)

        # Get paths for source and target
        source_path = self.derive_output_path(from_url)
        target_path = self.derive_output_path(target_url)

        # Calculate relative path
        from .link_rewriter import calculate_relative_path
        relative_path = calculate_relative_path(source_path, target_path)

        log.debug(
            f"Rewriting link: href='{href}', from='{from_url}' -> '{relative_path}'"
        )
        return relative_path
