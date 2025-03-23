import requests
from bs4 import BeautifulSoup

def scrape_reviews(product_url, review_selector, score_selector, headers=None):
    try:
        if not headers:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            }
        
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract reviews
        review_elements = soup.select(review_selector)
        reviews = [review.get_text().strip() for review in review_elements]

        # Extract scores
        score_elements = soup.select(score_selector)
        scores = []
        for score in score_elements:
            score_text = score.get_text().strip()
            # Convert score to float/int (e.g., "4.5 out of 5 stars" → 4.5)
            try:
                # Extract numeric part (assumes format like "4.5" or "4")
                numeric_score = float(''.join(filter(str.isdigit or str.isdecimal, score_text))[:2]) / 10 if '.' in score_text else int(score_text[0])
                scores.append(numeric_score)
            except (ValueError, IndexError):
                scores.append(None)  # Handle cases where score can’t be parsed

        if not reviews:
            print("No reviews found. Please check the review selector.")
            return {"error": "No reviews found"}
        
        if not scores or len(scores) != len(reviews):
            print("Warning: Score count doesn’t match review count or no scores found. Check the score selector.")
            scores = [None] * len(reviews)  # Fallback to None if scores are missing/inconsistent

        print(f"Successfully scraped {len(reviews)} reviews and {sum(1 for s in scores if s is not None)} scores.")
        return {
            "reviews": reviews,
            "scores": scores
        }

    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Amazon example
    url = "https://www.amazon.in/Lenovo-Athlon-Laptop-Windows-Warranty/dp/B0872G2MPV"
    review_sel = 'span[data-hook="review-body"]'  # Amazon review text
    score_sel = 'span[data-hook="review-star-rating"]'  # Amazon star rating
    
    result = scrape_reviews(url, review_sel, score_sel)
    if "reviews" in result:
        for review, score in zip(result["reviews"], result["scores"]):
            print(f"Review: {review[:50]}... | Score: {score}")

# print(scrape_reviews("https://www.amazon.in/Lenovo-Athlon-Laptop-Windows-Warranty/dp/B0872G2MPV/ref=sr_1_3?crid=1PWU0ROGKS0S6&dib=eyJ2IjoiMSJ9.05vnYa8Y1eYR8nvDhW0pdc1t5T7Eu8TebpJx75vIMbqzU5HAZ8QxOKcIyRRqubkhrmEUMldFlOCrtZUJNlIZEPimGTx8rD2zRHtBrXJvmUvEaV4-TSbkwA_omO_iCdHzGkWajGaq1VcD8aO-LKy-7Sy4gkfTVxXISrjL7Jwbu1qzs1pVepthPKgPuN_HFkB1zqRODpFRlFXUEylb9fLbsW6M-skntYRV8BfTrX6rP10.TXyx8_GOhjFud2sl-r00wz1VP6kqoRLo82WkDuemUEc&dib_tag=se&keywords=laptops+under+25000&qid=1742723224&sprefix=laptops%2Caps%2C228&sr=8-3",'span[data-hook="review-body"]','i[data-hook="review-star-rating"]'))