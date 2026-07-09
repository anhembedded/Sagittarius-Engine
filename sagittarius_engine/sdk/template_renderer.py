import re


class TemplateRenderer:
    """
    @brief Responsible for rendering template files replacing brackets placeholders.
    """

    def render(self, content: str, placeholders: dict[str, str]) -> str:
        """
        @brief Replaces all occurrences of {{ placeholder }} in content with matching values.
        """
        rendered = content
        for key, value in placeholders.items():
            # Matches {{key}} and {{ key }}
            pattern = re.compile(r"\{\{\s*" + re.escape(key) + r"\s*\}\}")
            rendered = pattern.sub(str(value), rendered)
        return rendered
