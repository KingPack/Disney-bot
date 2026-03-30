import random
import time


class HumanBehavior:
    @staticmethod
    def random_delay(min_seconds: float = 0.5, max_seconds: float = 2.5) -> None:
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    @staticmethod
    def scroll(driver, depth: int = 3) -> None:
        for _ in range(depth):
            driver.execute_script("window.scrollBy(0, window.innerHeight * 0.7);")
            HumanBehavior.random_delay(0.4, 1.4)
