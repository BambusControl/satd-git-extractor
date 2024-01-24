from typing import Optional


def print_progress(total: int, current: Optional[int] = None):
    value = total if current is None else current
    progress = 100.0 * float(total - value) / total
    print(f"\r{progress:.4f}%", end='', flush=True)
