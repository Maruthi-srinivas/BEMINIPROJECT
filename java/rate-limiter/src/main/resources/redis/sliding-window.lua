local now, window, limit, cost = tonumber(ARGV[1]), tonumber(ARGV[2]), tonumber(ARGV[3]), tonumber(ARGV[4])
local minimum = now - window
redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, minimum)
local count = redis.call('ZCARD', KEYS[1])
local allowed = count + cost <= limit
if allowed then
  for i = 1, cost do redis.call('ZADD', KEYS[1], now, now .. '-' .. i .. '-' .. math.random()) end
end
redis.call('EXPIRE', KEYS[1], math.ceil(window))
return {allowed and 1 or 0, limit - count - (allowed and cost or 0), minimum + window}
