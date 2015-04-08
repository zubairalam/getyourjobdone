class system {
  $packages = [
    "apt-transport-https",
    "build-essential",
    "curl",
    "fabric",
    "fail2ban",
    "g++",
    "gcc",
    "git-core",
    "graphicsmagick",
    "imagemagick",
    "make",
    "openjdk-7-jre-headless",
    "openssh-server",
    "tar",
    "vim",
    "wget",
    "zsh"
  ]

  $libs = [
    "liblcms2-dev",
    "libffi-dev",
    "libfontconfig",
    "libfreetype6-dev",
    "libjpeg8-dev",
    "libopenjpeg-dev",
    "libssl-dev",
    "libtiff4-dev",
    "libwebp-dev",
    "libxml2-dev",
    "libxslt1-dev",
    "libyaml-dev",
    "tcl8.5-dev",
    "tk8.5-dev",
    "zlib1g-dev"
  ]

  package { $packages: require => Class["core"] }

  package { $libs: require => Package[$packages] }

  package { "bash":
    ensure  => latest,
    require => Package[$libs]
  }

  user { "firethoughts":
    ensure     => 'present',
    comment    => 'firethoughts',
    groups     => ['adm', 'sudo', 'users'],
    home       => '/home/firethoughts',
    managehome => true,
    shell      => '/bin/zsh',
    password   => '$6$fWQDITDg$z9WEORldKxF2oSRyFoFzVVUDPp2zDPs/2QRyHgIwziwQg.5dY8Lf/Y7XYjizPjt9agC2ZQ5n7s.d.Ar3/SDo30',
    require    => Package["bash"]
  }

  file { "/home/firethoughts":
    ensure  => "directory",
    mode    => 755,
    require => User["firethoughts"]
  }

  file { "/var/www/":
    ensure  => "directory",
    require => File["/home/firethoughts"]
  }

  file { "/var/www/www.firethoughts.mu":
    ensure  => "directory",
    require => File["/var/www/"]
  }

  file { "/home/firethoughts/website.git":
    ensure  => "directory",
    owner   => "firethoughts",
    group   => "firethoughts",
    mode    => 755,
    require => File["/var/www/www.firethoughts.mu"]
  }

  exec { "initialize-website-git":
    command => "git init --bare",
    cwd     => "/home/firethoughts/website.git",
    require => File["/home/firethoughts/website.git"]
  }

  file { "/home/firethoughts/website.git/hooks/post-receive":
    source  => "puppet:///modules/system/post-receive",
    require => Exec["initialize-website-git"]
  }

  exec { "post-receive-hook-executable":
    command => "chmod +x post-receive",
    cwd     => "/home/firethoughts/website.git/hooks",
    require => File["/home/firethoughts/website.git/hooks/post-receive"]
  }

  file { "/home/firethoughts/fabfile.py":
    source  => "puppet:///modules/system/fabfile.py",
    owner   => "firethoughts",
    group   => "firethoughts",
    require => Exec["post-receive-hook-executable"]
  }

  exec { "set-etc-shells":
    command => "echo '/usr/sbin/nologin' >> /etc/shells && echo '/bin/zsh' >> /etc/shells",
    require => File["/home/firethoughts"]
  }

exec { "set-vim-environment":
    command => "curl -LSso .vimrc https://raw.githubusercontent.com/firethoughts/vimrc/master/.vimrc &&
      mkdir -p .vim/autoload .vim/bundle &&
      curl -LSso .vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim &&
      git clone https://github.com/scrooloose/nerdtree .vim/bundle/nerdtree &&
      git clone https://github.com/jistr/vim-nerdtree-tabs.git .vim/bundle/vim-nerdtree-tabs &&
      git clone https://github.com/ervandew/supertab .vim/bundle/supertab &&
      git clone https://github.com/bling/vim-airline .vim/bundle/vim-airline &&
      git clone https://github.com/bling/vim-bufferline .vim/bundle/vim-bufferline &&
      git clone https://github.com/tpope/vim-fugitive .vim/bundle/vim-fugitive &&
      git clone https://github.com/airblade/vim-gitgutter .vim/bundle/vim-gitgutter &&
      git clone https://github.com/edkolev/tmuxline.vim .vim/bundle/tmuxline.vim &&
      git clone https://github.com/tpope/vim-repeat .vim/bundle/vim-repeat &&
      git clone https://github.com/kien/ctrlp.vim .vim/bundle/ctrlp.vim &&
      git clone https://github.com/sjl/gundo.vim .vim/bundle/gundo.vim &&
      git clone https://github.com/rodjek/vim-puppet .vim/bundle/vim-puppet &&
      git clone https://github.com/mattn/emmet-vim .vim/bundle/emmet-vim &&
      git clone https://github.com/scrooloose/syntastic .vim/bundle/syntastic &&
      chown -R firethoughts:firethoughts .vimrc &&
      chown -R firethoughts:firethoughts .vim",
    cwd     => "/home/firethoughts",
    require => Exec["set-etc-shells"]
  }

  exec { "set-zsh-environment":
    command => "git clone git://github.com/robbyrussell/oh-my-zsh.git .oh-my-zsh &&
      cp .oh-my-zsh/templates/zshrc.zsh-template .zshrc &&
      chown -R firethoughts:firethoughts .oh-my-zsh &&
      chown -R firethoughts:firethoughts .zshrc",
    cwd     => "/home/firethoughts",
    require => Exec["set-vim-environment"]
  }


}