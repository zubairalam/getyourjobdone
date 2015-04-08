class elasticsearch {
  $package_version = "elasticsearch-1.4.2.deb"
  $package_url = "https://download.elasticsearch.org/elasticsearch/elasticsearch/$package_version"

  $plugins = [
    "elasticsearch/marvel/latest",
    "mobz/elasticsearch-head"
  ]

   exec { "install-elasticsearch":
      command => "curl -LOSs $package_url && sudo dpkg -i $package_version && rm -rf $package_version",
      require => Class["system"],
  }


  define install_elasticsearch_plugins {
    exec { "installing plugin $name":
        command => "sudo /usr/share/elasticsearch/bin/plugin -install $name ",
        require => Exec["install-elasticsearch"],
    }
  }

  install_elasticsearch_plugins { $plugins: }
  service { "elasticsearch": require => INSTALL_ELASTICSEARCH_PLUGINS[$plugins] }

}