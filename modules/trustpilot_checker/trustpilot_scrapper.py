import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, Dict


class TrustPilotScraper:

    REVIEW_URL: str = 'https://trustpilot.com/review/'
    
    @staticmethod
    def scrape_trustpilot(url: str) -> Optional[Dict[str, Optional[int]]]:

        headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        
        try:
            response: requests.Response = requests.get(TrustPilotScraper.REVIEW_URL + url, headers=headers)
            response.raise_for_status()  # Lève une exception pour les codes d'état HTTP 4xx/5xx
        except requests.RequestException as e:
            print(f"Error fetching data from Trustpilot: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        return TrustPilotScraper._extract_rating_info(soup)

    @staticmethod
    def _extract_rating_info(soup: BeautifulSoup) -> Dict[str, Optional[int]]:
        
        ret: Dict[str, Optional[int]] = {'note': None, 'ratings': None}

        rating = soup.select_one('#business-unit-title > div > div > p')
        number_of_ratings = soup.select_one('#business-unit-title > span.styles_clickable__zQWyh > span')

        if rating and rating.get_text(strip=True):
            
            ret['note'] = round((float(rating.get_text(strip=True)) / 5) * 100, 2)

        if number_of_ratings:
            match = re.search(r'(\d{1,3}(?:,\d{3})*)', number_of_ratings.get_text(strip=True))
            if match:
                number = match.group(1).replace(',', '')
                ret['ratings'] = int(number)

        return ret

