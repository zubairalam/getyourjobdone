class core {
	$timezone = 'Europe/London'

	exec { "set-swapon":
		command => "dd if=/dev/zero of=/swap bs=1M count=1024 && mkswap /swap && swapon /swap",
	}
	exec { "set-locale":
		command => "locale-gen en_GB.UTF-8",
		require => Exec["set-swapon"]
	}

	exec { "update-clock":
		command => "ntpdate ntp.ubuntu.com",
		require => Exec["set-locale"]
	}

	exec { "set-tzdata":
		command => "echo $timezone  > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata",
		require => Exec["update-clock"]
	}

}