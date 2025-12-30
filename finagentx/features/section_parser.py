import re
from typing import Dict


class SectionParser:
    SECTION_PATTERN = re.compile(r"(ITEM\s+\d+[A-Z]?\.)", re.IGNORECASE)

    def parse(self, text: str) -> Dict[str, str]:
        sections = {}
        splits = self.SECTION_PATTERN.split(text)

        for i in range(1, len(splits), 2):
            title = splits[i].strip().upper()
            body = splits[i + 1].strip()

            # ignore noise
            if len(body) < 200:
                continue

            sections[title] = body

        return sections
