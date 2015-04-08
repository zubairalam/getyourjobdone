class project {

  exec { "project-permissions":
     command => "chown -R www-data: /var/www && chown -R www-data: /var/www/www.firethoughts.mu",
     require => Class["nodejs"]
  }

  exec { "restart-web-servers":
    command => "service nginx restart",
    require => Exec["project-permissions"]
  }

}