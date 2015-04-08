class nginx {
  package { "nginx": require => Class["redis"] }

  service { "nginx": require => Package["nginx"] }

  group { "www-data":
    require => Package["nginx"]
  }

  exec { "add-nginx-user":
    command => "usermod -a -G www-data firethoughts",
    require => Group["www-data"]
  }

  file { "/etc/nginx/sites-enabled/default":
    ensure  => "absent",
    require => Exec["add-nginx-user"]
  }

  file { "/etc/nginx/sites-available/default":
    ensure  => "absent",
    require => Exec["add-nginx-user"]
  }

  file { "/etc/nginx/nginx.conf":
    source  => "puppet:///modules/nginx/nginx.conf",
    replace => true,
    require => File["/etc/nginx/sites-enabled/default"]
  }

  file { "/etc/nginx/sites-available/web.conf":
    source  => "puppet:///modules/nginx/web.conf",
    require => File["/etc/nginx/nginx.conf"]
  }

  file { "/etc/nginx/sites-enabled/web.conf":
    ensure  => "link",
    source  => "/etc/nginx/sites-available/web.conf",
    require => File["/etc/nginx/sites-available/web.conf"]
  }

}

