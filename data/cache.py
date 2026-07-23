import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MarketDataCache:
    """
    In-memory L1/L2 cache with TTL support and manual invalidation.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached object if not expired.
        """
        entry = self._cache.get(key)
        if not entry:
            return None

        if time.time() > entry["expires_at"]:
            logger.debug("Cache key expired: %s", key)
            del self._cache[key]
            return None

        return entry["value"]

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """
        Set cache value with TTL.
        """
        self._cache[key] = {
            "value": value,
            "created_at": time.time(),
            "expires_at": time.time() + ttl_seconds
        }

    def invalidate(self, prefix: Optional[str] = None) -> None:
        """
        Invalidate cache entries. If prefix is None, clear all cache entries.
        """
        if prefix is None:
            self._cache.clear()
            logger.info("Entire cache invalidated.")
        else:
            keys_to_del = [k for k in self._cache.keys() if k.startswith(prefix)]
            for k in keys_to_del:
                del self._cache[k]
            logger.info("Invalidated %d cache keys matching prefix '%s'.", len(keys_to_del), prefix)

# Global singleton cache instance
global_cache = MarketDataCache()
