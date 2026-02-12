from dataclasses import dataclass

@dataclass(frozen=True)
class DetectConfig:
    min_occurrences: int = 3
    monthly_interval_min_days: int = 20
    monthly_interval_max_days: int = 40
    annual_interval_min_days: int = 330
    annual_interval_max_days: int = 395

    price_spike_pct: float = 0.25
    dup_similarity_threshold: float = 0.86
