class postgresql {
# scope variables
$db_name = "project" # database name
$db_user = "vagrant" # user to run db as
$db_pass = "vagrant" # password for the postgresql db
$packages = ["libpq-dev", "postgresql", "postgresql-contrib"]

# let's rock!
package { $packages:
    require => Class["core"]
}

service { "postgresql":
    enable  => "true",
    ensure => "running",
    require => Package[$packages],
}

exec {"update-postgresql-utf8-1":
    command =>"sudo -u postgres psql -c \"UPDATE pg_database SET datistemplate=FALSE WHERE datname='template1';\"",
    require => Service["postgresql"],
}

exec {"update-postgresql-utf8-2":
    command =>"sudo -u postgres psql -c \"DROP DATABASE template1;\"",
    require => Exec["update-postgresql-utf8-1"],
}

exec {"update-postgresql-utf8-3":
    command =>"sudo -u postgres psql -c \"CREATE DATABASE template1 WITH owner=postgres template=template0 encoding='UTF8';\"",
    require => Exec["update-postgresql-utf8-2"],
}

exec {"update-postgresql-utf8-4":
    command =>"sudo -u postgres psql -c \"UPDATE pg_database SET datistemplate=TRUE WHERE datname='template1';\"",
    require => Exec["update-postgresql-utf8-3"],
}

exec {"create-psql-database":
    command => "sudo -u postgres createdb $db_name",
    require => Exec["update-postgresql-utf8-4"],
}

exec {"create-psql-superuser":
    command => "sudo -u postgres createuser $db_user -s",
    require => Exec["update-postgresql-utf8-4"],
}

exec {"update-psql-user":
    command => "sudo -u postgres psql -c \"alter user $db_user with encrypted password '$db_pass';\"",
    require => [Exec["create-psql-superuser"], Exec["create-psql-database"]],
}

exec {"associate-psql-user":
    command => "sudo -u postgres psql -c \"grant all privileges on database $db_name to $db_user;\"",
    require => Exec["update-psql-user"],
}

}