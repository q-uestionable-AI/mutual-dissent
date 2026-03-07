## 2024-05-24 - N+1 in Stats Computation
**Learning:** `_compute_stats` in the debate orchestrator was fetching model pricing (`await pricing_cache.get_pricing(r.model_id)`) inside a loop over every response. Even with a pricing cache, this means many sequential `await` calls if there are multiple rounds and models.
**Action:** When computing stats across a large number of model responses, always pre-fetch unique model IDs first and store their pricing/data in a local dictionary before entering the main loop.
