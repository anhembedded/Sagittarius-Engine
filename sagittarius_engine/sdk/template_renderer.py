import re


class TemplateRenderer:
    """
    @brief Responsible for rendering template files replacing brackets placeholders.
    """

    # Compile the pattern once for all instances
    # Matches {{key}} and {{ key }} and extracts the key
    _pattern = re.compile(r"\{\{\s*(.*?)\s*\}\}")

    def render(self, content: str, placeholders: dict[str, str]) -> str:
        """
        @brief Replaces all occurrences of {{ placeholder }} in content with matching values.
        """
        def replacer(match):
            key = match.group(1)
            if key in placeholders:
                return str(placeholders[key])
            return match.group(0)

        return self._pattern.sub(replacer, content)
