local capacity, refill_rate, cost = tonumber(ARGV[1]), tonumber(ARGV[2]), tonumber(ARGV[3])
local current = redis.call('HMGET', KEYS[1], 'tokens', 'updated_at')
local tokens, updated = tonumber(current[1]), tonumber(current[2])
local now = tonumber(redis.call('TIME')[1])
if not tokens then tokens = capacity end
if not updated then updated = now end
tokens = math.min(capacity, tokens + (now - updated) * refill_rate)
local allowed = tokens >= cost
if allowed then tokens = tokens - cost end
redis.call('HMSET', KEYS[1], 'tokens', tokens, 'updated_at', now)
redis.call('EXPIRE', KEYS[1], math.max(1, math.ceil(capacity / refill_rate) * 2))
return {allowed and 1 or 0, math.floor(tokens), now}
