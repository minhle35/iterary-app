"""
Simple trip parser - extracts city and duration using rule-based parsing.
Designed for use case: parse city + duration, then suggest activities via POI APIs.
"""

import re
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SimpleTripParser:
    """
    Simple trip parser that extracts:
    - City (destination)
    - Duration (in days)

    Uses rule-based pattern matching for both city and duration extraction.
    """

    def __init__(self):
        """Initialize the simple trip parser."""
        # Common city names (can be expanded)
        self.cities = [
            # Australia
            "Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide", "Darwin",
            "Canberra", "Gold Coast", "Cairns", "Hobart", "Newcastle", "Wollongong",
            # Asia
            "Tokyo", "Osaka", "Kyoto", "Seoul", "Bangkok", "Singapore",
            "Hong Kong", "Shanghai", "Beijing", "Taipei", "Manila", "Jakarta",
            # Europe
            "London", "Paris", "Berlin", "Rome", "Barcelona", "Amsterdam",
            "Madrid", "Vienna", "Prague", "Budapest", "Athens", "Lisbon",
            # Americas
            "New York", "Los Angeles", "San Francisco", "Chicago", "Miami", "Boston",
            "Toronto", "Vancouver", "Mexico City", "Buenos Aires", "Rio de Janeiro",
            # Others
            "Dubai", "Cairo", "Cape Town", "Auckland", "Wellington"
        ]

    def parse(self, query: str) -> Dict[str, Any]:
        """
        Parse a natural language trip query to extract city and duration.

        Args:
            query: Natural language query (e.g., "3 days in Melbourne" or "going to Sydney for 5 days")

        Returns:
            Dictionary with:
            - city: City name (empty string if not found)
            - duration_days: Number of days (None if not found)
        """
        result = {
            "city": "",
            "duration_days": None
        }

        # Extract city
        city = self._extract_city(query)
        if city:
            result["city"] = city

        # Extract duration
        duration = self._extract_duration(query)
        if duration:
            result["duration_days"] = duration

        return result

    def _extract_city(self, query: str) -> Optional[str]:
        """
        Extract city name from query.

        Patterns:
        - "in [City]"
        - "to [City]"
        - "going to [City]"
        - "visiting [City]"
        - "[City]" (standalone capitalized word)
        """
        query_lower = query.lower()

        # Check for known cities (case-insensitive)
        for city in self.cities:
            # Exact match (case-insensitive)
            if city.lower() in query_lower:
                # Check if it's a word boundary match
                pattern = r'\b' + re.escape(city.lower()) + r'\b'
                if re.search(pattern, query_lower):
                    return city

        # Pattern matching: "in [City]", "to [City]", etc.
        patterns = [
            r'\b(?:in|to|visiting|going to|traveling to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:for|from|starting)',
        ]

        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                potential_city = match.group(1)
                # Validate it's not a common word
                if potential_city.lower() not in ["nov", "dec", "jan", "feb", "mar", "apr",
                                                   "may", "jun", "jul", "aug", "sep", "oct",
                                                   "the", "and", "for", "with", "from"]:
                    return potential_city

        # Try to find capitalized words that might be cities
        words = query.split()
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word and clean_word[0].isupper() and len(clean_word) > 2:
                # Check if it matches a known city
                for city in self.cities:
                    if clean_word.lower() == city.lower():
                        return city
                # If no match but looks like a city name, return it
                if len(clean_word) > 3:  # Avoid short words like "The", "And"
                    return clean_word

        return None

    def _extract_duration(self, query: str) -> Optional[int]:
        """
        Extract duration in days from query.

        Patterns:
        - "for 3 days"
        - "3 days"
        - "3-day trip"
        - "weekend" (2 days)
        - "week" (7 days)
        """
        query_lower = query.lower()

        # Pattern: "for X days" or "X days"
        patterns = [
            r'for\s+(\d+)\s+days?',
            r'(\d+)\s+days?',
            r'(\d+)-day',
            r'(\d+)\s+day\s+trip',
        ]

        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                days = int(match.group(1))
                if 1 <= days <= 365:  # Reasonable range
                    return days

        # Special cases
        if "weekend" in query_lower:
            return 2
        if "week" in query_lower and "weekend" not in query_lower:
            # Check for "a week", "one week", "1 week"
            week_match = re.search(r'(?:a|one|1)\s+week', query_lower)
            if week_match:
                return 7
        if "month" in query_lower:
            month_match = re.search(r'(?:a|one|1)\s+month', query_lower)
            if month_match:
                return 30

        return None


# Global instance
_simple_trip_parser: Optional[SimpleTripParser] = None


def get_simple_trip_parser() -> SimpleTripParser:
    """Get or create the global simple trip parser instance."""
    global _simple_trip_parser
    if _simple_trip_parser is None:
        _simple_trip_parser = SimpleTripParser()
    return _simple_trip_parser
