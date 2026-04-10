# socialscope

Phase 1 — Skeleton (week 1)
Validator → platform detect → Reddit fetch → store raw post → JSON output. At the end of this phase you can submit a Reddit link and get structured metadata back.

Phase 2 — Media pipeline (week 2)
Download video → extract keyframes with OpenCV → strip audio with ffmpeg → run Whisper. Store transcript and frame paths. Test on a few Reddit video posts.

Phase 3 — AI analysis (week 3)
Feed combined signals into the LLM prompt. Design the output schema. Store structured result. Test quality on 10–15 posts. Tune the prompt.

Phase 4 — Storage and search (week 4)
Wire up SQLite tables. Generate embeddings. Basic vector search working. User can query their library with a natural language prompt and get ranked results.

Phase 5 — Personalisation (week 5)
Add the user profile table. Build Engine 1 filter. Let user edit tags post-ingestion and save corrections. Add thumbs down capture. Build Engine 2 re-ranker (start simple — just a score penalty on rejected posts for similar queries).

Phase 6 — Progress and polish (week 6)
Background job queue with progress log. Non-blocking CLI. Purpose field with AI suggestion + user override. Basic analytics queries (top categories, most used tags).
