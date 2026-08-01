"""Tests for Pack 03 memory cache infrastructure."""

from __future__ import annotations

import time

import pytest

from engines.interpretation_engine.cache import (
    CacheManager,
    CacheStats,
    ContextCache,
    InterpretationCache,
    InterpretationCacheInterface,
    MemoryCache,
    PlaceholderCache,
    RegistryCache,
    SentenceCache,
    TemplateCache,
)


def test_domain_caches_exist_and_are_memory_only() -> None:
    """All five domain caches are distinct MemoryCache instances."""
    manager = CacheManager()
    assert isinstance(manager.context, ContextCache)
    assert isinstance(manager.sentence, SentenceCache)
    assert isinstance(manager.template, TemplateCache)
    assert isinstance(manager.placeholder, PlaceholderCache)
    assert isinstance(manager.registry, RegistryCache)
    assert set(manager.caches()) == {
        "context_cache",
        "sentence_cache",
        "template_cache",
        "placeholder_cache",
        "registry_cache",
    }
    assert manager.validate() is True
    assert issubclass(ContextCache, InterpretationCacheInterface)


def test_memory_cache_crud_and_stats() -> None:
    """MemoryCache supports get/set/delete/has/clear with stats."""
    cache: MemoryCache[str] = MemoryCache(cache_id="unit", max_size=10)
    assert cache.get("missing") is None
    assert cache.has("missing") is False

    cache.set("a", "alpha")
    assert cache.get("a") == "alpha"
    assert cache.has("a") is True
    assert cache.keys() == ("a",)
    assert cache.delete("a") is True
    assert cache.delete("a") is False
    assert cache.get("a") is None

    cache.set("b", "beta")
    cache.clear()
    assert cache.size() == 0

    stats = cache.stats()
    assert isinstance(stats, CacheStats)
    assert stats.validate() is True
    assert stats.sets >= 1
    assert stats.hit_ratio >= 0.0


def test_lru_eviction_and_ttl() -> None:
    """LRU eviction and TTL expiry work without Redis."""
    cache: MemoryCache[int] = MemoryCache(cache_id="lru", max_size=2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.get("a")  # make a most-recent
    cache.set("c", 3)  # evict b
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    assert cache.stats().evictions >= 1

    ttl_cache: MemoryCache[str] = MemoryCache(
        cache_id="ttl",
        max_size=10,
        default_ttl_seconds=0.01,
    )
    ttl_cache.set("x", "value")
    time.sleep(0.02)
    assert ttl_cache.get("x") is None
    assert ttl_cache.has("y") is False
    ttl_cache.set("z", "keep", ttl_seconds=60)
    assert ttl_cache.purge_expired() == 0
    assert ttl_cache.get("z") == "keep"


def test_cache_manager_aggregate_operations() -> None:
    """CacheManager clear/purge/stats aggregate across domains."""
    manager = CacheManager()
    manager.context.set("ctx_1", {"id": "ctx_1"})
    manager.sentence.set("s_1", {"ref": "s_1"})
    manager.template.set("t_1", {"ref": "t_1"})
    manager.placeholder.set("p_1", {"ref": "p_1"})
    manager.registry.set("r_1", {"ref": "r_1"})
    assert manager.total_size() == 5

    stats = manager.stats()
    assert stats["context_cache"].sets == 1
    assert stats["sentence_cache"].size == 1

    purged = manager.purge_expired()
    assert purged == 0
    manager.clear_all()
    assert manager.total_size() == 0


def test_validation_and_errors() -> None:
    """Invalid cache ids/keys/ttls raise clearly."""
    with pytest.raises(ValueError, match="cache_id_required"):
        MemoryCache(cache_id="")
    cache = MemoryCache[str](cache_id="err")
    with pytest.raises(ValueError, match="cache_key_required"):
        cache.set("", "x")
    with pytest.raises(ValueError, match="cache_ttl_invalid"):
        cache.set("k", "v", ttl_seconds=-1)
    assert cache.get("") is None
    assert cache.has("") is False
    assert CacheStats().hit_ratio == 0.0


def test_legacy_interpretation_cache_still_available() -> None:
    """Legacy InterpretationCache remains re-exported."""
    legacy = InterpretationCache()
    legacy.set("k", 1)
    assert legacy.get("k") == 1
    assert legacy.has("k") is True


def test_unbounded_cache_and_explicit_ttl_override() -> None:
    """max_size<=0 disables eviction; per-set TTL overrides default."""
    cache = MemoryCache[int](cache_id="unbounded", max_size=0, default_ttl_seconds=100)
    for index in range(5):
        cache.set(str(index), index)
    assert cache.size() == 5
    cache.set("temp", 99, ttl_seconds=0.01)
    time.sleep(0.02)
    assert cache.purge_expired() >= 1
    assert cache.get("temp") is None
