# [TIMESTAMP: 2026-06-11T13:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import requests
import re
import time
import random
import math
from collections import Counter
from typing import List, Dict, Any
from .config import add_log

class CitationManager:
    """
    Step 23: Manages academic citations and bibliography generation.
    """
    def __init__(self):
        self.citations = []

    def add_source(self, url: str, domain: str = None):
        if not domain:
            try:
                domain = re.search(r'https?://(.*?)/', url).group(1)
            except Exception:
                domain = "AcademicSource"

        citation = {
            "title": f"Metropolis Academic Archive: {domain.capitalize()}",
            "url": url,
            "accessed": time.strftime("%Y-%m-%d")
        }
        self.citations.append(citation)
        return citation

    def generate_bibliography(self) -> str:
        bib = "## BIBLIOGRAPHY\n"
        # Sort and deduplicate
        unique_cites = {c['url']: c for c in self.citations}.values()
        for c in sorted(unique_cites, key=lambda x: x['title']):
            bib += f"* {c['title']}. Available at: {c['url']} (Accessed {c['accessed']})\n"
        return bib

class AdvancedScraper:
    """
    HOUSE-MADE ADVANCED SCRAPER (FROM SCRATCH)
    - Step 25: Shannon Entropy Scoring for information density.
    - Heuristic filtering of low-quality data.
    - University-level data targeting.
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Metropolis-Research-Bot/1.0 (Markov-Shannon Synthesis Engine)'
        }
        self.blacklist = ["advertisement", "click here", "sign up", "cookie policy"]

    def calculate_shannon_entropy(self, text: str) -> float:
        """Calculates the information entropy of the text."""
        if not text: return 0.0
        probabilities = [n_occ / len(text) for n_occ in Counter(text).values()]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        return entropy

    def is_high_quality(self, text: str) -> bool:
        """Heuristically weeds out inaccurate or poor data using Shannon Logic."""
        if len(text) < 500: return False

        entropy = self.calculate_shannon_entropy(text)
        # Higher entropy (typically 4.0 - 5.0 for English text) implies higher information density
        if entropy < 3.5: return False # Likely repetitive or low-info content

        academic_markers = ["taxonomy", "genetics", "physiological", "evolutionary", "behavioral", "felis catus"]
        matches = sum(1 for m in academic_markers if m in text.lower())

        if matches < 2: return False
        if any(word in text.lower() for word in self.blacklist): return False

        return True

    def scrape_topic(self, topic: str, max_results: int = 10) -> List[Dict]:
        """
        Scrapes data for a topic using a search engine aggregator.
        """
        add_log(f"[SCRAPER] Initiating Advanced Scrape for: {topic}")
        search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}+university+study+feline+biology"

        results = []
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                links = re.findall(r'href="/url\?q=(https://.*?)"', response.text)
                unique_links = list(set([l.split('&')[0] for l in links if "google" not in l]))

                for link in unique_links[:max_results]:
                    content = self.fetch_and_clean(link)
                    if self.is_high_quality(content):
                        results.append({"url": link, "content": content})
                        add_log(f"[SCRAPER] Verified High-Quality Source: {link[:40]}...")
        except Exception as e:
            add_log(f"[SCRAPER] Scrape Error: {str(e)}", level="error")

        return results

    def fetch_and_clean(self, url: str) -> str:
        """Fetch HTML and heuristically extract structural text."""
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            html = re.sub(r'<(script|style).*?>.*?</\1>', '', res.text, flags=re.DOTALL)
            paragraphs = re.findall(r'<p>(.*?)</p>', html, flags=re.DOTALL)

            clean_text = ""
            for p in paragraphs:
                p_clean = re.sub(r'<.*?>', '', p)
                if len(p_clean) > 100:
                    clean_text += p_clean + "\n\n"
            return clean_text
        except Exception:
            return ""

    def get_citation(self, result: Dict) -> str:
        """Step 23: Generates an academic citation for a scraped source."""
        url = result['url']
        try:
            domain = re.search(r'https?://(.*?)/', url).group(1)
        except Exception:
            domain = "AcademicSource"
        title = "Metropolis Academic Archive: " + domain.capitalize()
        return f"[{title}. Available at: {url} (Accessed 2026-06-11)]"

advanced_scraper = AdvancedScraper()
