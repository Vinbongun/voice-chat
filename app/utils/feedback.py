from typing import Optional


def normalize_rating(rating: int, min_val: int = 1, max_val: int = 5) -> int:
    """Clamp rating to valid range."""
    return max(min_val, min(max_val, rating))


def rating_to_label(rating: int) -> str:
    """Convert numeric rating to human-readable label."""
    labels = {1: "very_bad", 2: "bad", 3: "neutral", 4: "good", 5: "very_good"}
    return labels.get(rating, "unknown")


def is_positive_feedback(rating: int, threshold: int = 4) -> bool:
    """Return True if rating is considered positive."""
    return rating >= threshold
