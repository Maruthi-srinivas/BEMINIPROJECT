# D17-T009 — Social media news feed

Topic ID: `D17-T009`

## A. Topic Overview

Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case.

## B. Requirements, capacity, API, data

**FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table.

## D. Architecture

```mermaid
flowchart TD
  user[User]
  feed[FeedService]
  post[PostService]
  graph[SocialGraph]
  cache[(FeedCache)]
  user --> feed --> cache
  feed --> graph
  post --> graph
```

## J. Bottlenecks / failures

Hot celebrity fan-out; ranker CPU; stale feed after unfollow; like counter drift.

## K. Interview Preparation

### Beginner

#### Q1. Fan-out on read vs write?

**Answer:** Write fan-out precomputes feeds for followers at post time—fast read, slow post for celebrities. Read fan-out merges on request—slow read for users with many follows. Hybrid uses write for normal users and pull for celebrities. Pick based on read:write ratio and follower distribution.

#### Q2. What is the feed?

**Answer:** Ordered list of post ids for a viewer. Materialized list or computed merge. Pagination via cursor on stable ordering key.

#### Q3. Pagination cursor?

**Answer:** Opaque cursor encodes last seen rank/score/id. Avoid offset pagination on large feeds. Stable under new posts inserting at top.

#### Q4. Hot user problem?

**Answer:** User with millions of followers cannot fan-out on write synchronously. Async fan-out, sampling, or read-time merge required.

#### Q5. Chronological vs ranked?

**Answer:** Chronological is simpler and predictable. Ranked needs ML features and online scoring budget. Many apps offer toggle.

### Intermediate

#### Q1. Hybrid fan-out?

**Answer:** Threshold follower count switches strategy. Monitor post latency for users near threshold.

#### Q2. Precompute scores?

**Answer:** Offline batch features; online lightweight model. Cache ranked feeds with TTL.

#### Q3. Comment threading?

**Answer:** Separate tree storage; feed shows top-level posts primarily.

#### Q4. Counter denormalization?

**Answer:** `like_count` on post row; reconcile from event log periodically.

#### Q5. Ads insertion?

**Answer:** Insert slots in ranker with frequency caps; separate ad service.

### Advanced

#### Q1. ML ranker serving?

**Answer:** Feature store low latency; model server GPU pool; fallback to chronological on timeout.

#### Q2. Global consistency?

**Answer:** Eventual feed freshness acceptable; strong consistency for post creation in DB.

#### Q3. Sharding graph?

**Answer:** Shard follows by follower id; celebrity edges may be side table.

#### Q4. Real-time trending?

**Answer:** Stream aggregations separate from home feed.

#### Q5. Cold start users?

**Answer:** Popular/topic bootstrap until graph exists.

### Scenarios

#### Q1. Celebrity 10M followers.

**Answer:** Async partial fan-out + read merge for online followers; CDN not applicable to personalized feed.

#### Q2. Unfollow still sees posts.

**Answer:** Remove from feed cache on unfollow event; stale cache TTL bug.

#### Q3. Empty new user feed.

**Answer:** Onboarding suggestions; follow recommendations.

#### Q4. Ranking latency spike.

**Answer:** Degrade to chronological; scale ranker; cache features.

#### Q5. Wrong like count.

**Answer:** Reconcile counters from Kafka log.

### Follow-ups

#### Q1. Autocomplete?

**Answer:** `D17-T013` for query suggest.

#### Q2. Media storage?

**Answer:** `D17-T010`/`D17-T011` for photos/video.

#### Q3. Notifications?

**Answer:** `D17-T004` on likes/comments.

## L. Exercises

Solutions: `EXERCISES/solutions/D17-T009.md`. Hybrid fan-out; cache invalidation; like counters.

## C, E–I, M–O

Post service writes graph; feed service reads cache. Trade-offs: materialized vs computed feed. Completion: draw hybrid fan-out threshold.

## Supplement for missing section letters

## C. Internal Working and Architecture

Social media news feed continues the design already written in this file. Topic ID: `D17-T009` Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case. **FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table. ```mermaid flowchart TD user[User] feed[FeedService] post[PostServi

For section C, keep the same capacity numbers and API as the requirements above. Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck.

## E. Examples and Analogies

Social media news feed continues the design already written in this file. Topic ID: `D17-T009` Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case. **FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table. ```mermaid flowchart TD user[User] feed[FeedService] post[PostServi

For section E, keep the same capacity numbers and API as the requirements above. Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck.

## F. Code Examples

```python
# unexecuted illustration for D17-T009
def explain():
    return 'Social media news feed'
```

## G. Practical Backend Application

Social media news feed continues the design already written in this file. Topic ID: `D17-T009` Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case. **FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table. ```mermaid flowchart TD user[User] feed[FeedService] post[PostServi

For section G, keep the same capacity numbers and API as the requirements above. Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Social media news feed | Matches the requirements in this note | More components | The bottleneck in section J is real | A single node still meets the SLO |

## I. Common Mistakes and Misconceptions

Social media news feed continues the design already written in this file. Topic ID: `D17-T009` Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case. **FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table. ```mermaid flowchart TD user[User] feed[FeedService] post[PostServi

For section I, keep the same capacity numbers and API as the requirements above. Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck.

## M. Revision Notes

Social media news feed continues the design already written in this file. Topic ID: `D17-T009` Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case. **FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table. ```mermaid flowchart TD user[User] feed[FeedService] post[PostServi

For section M, keep the same capacity numbers and API as the requirements above. Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck.

## N. Related Topics

Social media news feed continues the design already written in this file. Topic ID: `D17-T009` Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case. **FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table. ```mermaid flowchart TD user[User] feed[FeedService] post[PostServi

For section N, keep the same capacity numbers and API as the requirements above. Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck.

## O. Completion Criteria

Social media news feed continues the design already written in this file. Topic ID: `D17-T009` Home feed of posts from follows; ranked or chronological; celebrity fan-out is the classic hard case. **FR:** Post, like, comment; `GET /v1/feed?cursor=`. **NFR:** Feed p99 < 200 ms; freshness tens of seconds. **Capacity:** 300M DAU; **10k posts/s**; reads dominate—fan-out on write vs read hybrid. **API:** `POST /v1/posts`, `GET /v1/feed`. **Data:** `posts`, `follows`, `feed_cache(user_id)` or fan-out table. ```mermaid flowchart TD user[User] feed[FeedService] post[PostServi

For section O, keep the same capacity numbers and API as the requirements above. Do not invent a second architecture. The completion check is whether you can still draw the original diagram and name its bottleneck.
