class nodejs {
  $packages = [
    "npm@latest",
    "bower",
    "grunt-cli",
    "nodemon",
    "karma",
    "phantomjs",
    "yo"
  ]

  exec { "add-node-repo":
    command => "curl -sL https://deb.nodesource.com/setup | sudo bash -",
    require => Class["mongo"]
  }

  package { "nodejs": require => Exec["add-node-repo"] }


  define install_npm_packages {
    exec { "installing node package $name":
      command => "npm install -g $name",
      require => Package["nodejs"]
    }
  }
  install_npm_packages { $packages:  }
}