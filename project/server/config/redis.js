var redis = require('redis'),
    redisClient = redis.createClient();
    redisClient.auth('firethoughts123');

module.exports = redisClient;
