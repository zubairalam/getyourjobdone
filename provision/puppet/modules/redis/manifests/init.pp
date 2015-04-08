class redis{
  $password = "firethoughts123"

  package { "redis-server": require => Class["elasticsearch"] }

  service { "redis-server": require => Package["redis-server"] }

  exec { "auth-redis":
    command => 'sed -i "s/bind 127.0.0.1/#bind 127.0.0.1/g" /etc/redis/redis.conf', # sed not allowing password here!
    require => Package["redis-server"]
  }

   exec { "redis-bind":
    command => 'sed -i "s/^# requirepass foobared/requirepass firethoughts123/g" /etc/redis/redis.conf',
    require => Exec["auth-redis"],
    notify  => Service["redis-server"],
  }
}