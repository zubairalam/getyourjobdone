node "firethoughts" {

  user { root:
    ensure   => present,
    password => '$6$fWQDITDg$z9WEORldKxF2oSRyFoFzVVUDPp2zDPs/2QRyHgIwziwQg.5dY8Lf/Y7XYjizPjt9agC2ZQ5n7s.d.Ar3/SDo30',
  }

  Exec {
    path      => [ "/bin", "/sbin", "/usr/bin", "/usr/sbin", "/usr/local/bin", "/usr/local/sbin"],
    timeout   => 3600,
    user      => root,
    tries     => 10,
    logoutput => true
  }

  exec { "apt-update":
    command => "apt-get update",
    user    => root
  }

  Exec["apt-update"] -> Package <| |>

  Group {
    ensure => present,
  }

  Package {
    ensure => "present"
  }

  Service {
    ensure  => "running",
    enable  => "true",
  }

  Cron {
    user     => root,
    hour     => "*",
    minute   => "*",
    month    => "*",
    monthday => "*",
    weekday  => "*",
  }

  include core
  include system
  include elasticsearch
  include redis
  include nginx
  include mongo
  include nodejs
  include project
}






