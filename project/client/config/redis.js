var redis = require('redis'),
    redisClient = redis.createClient();
    redisClient.auth('xeontek123');

module.exports = redisClient;
