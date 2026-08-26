import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_script_type = None
        self.current_cell = None
        self.current_heading = None
        self.current_heading_class = None
        self.scripts = []
        self.cells = []
        self.headings = []
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "script":
            self.current_script_type = attributes.get("type")
            self._buffer = []
        elif tag in {"th", "td"}:
            self.current_cell = tag
            self._buffer = []
        elif tag in {"h1", "h2", "h3"}:
            self.current_heading = tag
            self.current_heading_class = attributes.get("class")
            self._buffer = []

    def handle_data(self, data):
        if self.current_script_type or self.current_cell or self.current_heading:
            self._buffer.append(data)

    def handle_endtag(self, tag):
        text = " ".join("".join(self._buffer).split())
        if tag == "script" and self.current_script_type:
            if self.current_script_type == "application/ld+json":
                self.scripts.append(json.loads("".join(self._buffer)))
            self.current_script_type = None
            self._buffer = []
        elif tag == self.current_cell:
            self.cells.append((tag, text))
            self.current_cell = None
            self._buffer = []
        elif tag == self.current_heading:
            self.headings.append((tag, self.current_heading_class, text))
            self.current_heading = None
            self.current_heading_class = None
            self._buffer = []


def parse_page(name):
    parser = PageParser()
    parser.feed((ROOT / name).read_text())
    return parser


class FallReopeningTests(unittest.TestCase):
    def test_hours_page_presents_effective_date_and_weekday_schedule(self):
        page = parse_page("lab-hours.html")
        text = (ROOT / "lab-hours.html").read_text()

        self.assertIn("Effective Monday, August 31, 2026", text)
        self.assertIn(("th", "Day"), page.cells)
        self.assertIn(("th", "Open Hours"), page.cells)
        self.assertEqual(
            [cell for tag, cell in page.cells if tag == "td"],
            [
                "Monday", "1:00–7:00 PM",
                "Tuesday", "1:00–7:00 PM",
                "Wednesday", "4:00–7:00 PM",
                "Thursday", "1:00–7:00 PM",
                "Friday", "1:00–7:00 PM",
            ],
        )

    def test_schema_exposes_real_fall_weekday_hours(self):
        page = parse_page("lab-hours.html")
        business = next(item for item in page.scripts if item.get("@type") == "LocalBusiness")

        self.assertEqual(
            business["openingHoursSpecification"],
            [
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Thursday", "Friday"],
                    "opens": "13:00",
                    "closes": "19:00",
                    "validFrom": "2026-08-31",
                },
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": "Wednesday",
                    "opens": "16:00",
                    "closes": "19:00",
                    "validFrom": "2026-08-31",
                },
            ],
        )

    def test_public_status_files_no_longer_report_summer_closure(self):
        public_files = [
            "lab-hours.html",
            "online-ordering.html",
            "free-print-wednesday.html",
            "api/site-info.json",
            "llms.txt",
        ]
        stale = re.compile(r"closed (?:for summer break|between semesters)|reopens? the week of", re.I)

        for name in public_files:
            with self.subTest(name=name):
                self.assertIsNone(stale.search((ROOT / name).read_text()))

    def test_guru_roster_lists_the_three_confirmed_fall_staff(self):
        page = parse_page("lab-staff.html")
        guru_names = [
            text
            for level, class_name, text in page.headings
            if level == "h3" and class_name == "staff-card-name"
            and text not in {"Dr. Aric Rindfleisch", "Dr. Vishal Sachdev"}
        ]

        self.assertEqual(
            guru_names,
            ["Bayu Febriansyah", "Aldo Villanueva", "Sahib Bedi"],
        )


if __name__ == "__main__":
    unittest.main()
