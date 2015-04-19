class python {
# scope variables
$virtualenv_name = "project" # virtual environment name
$virtualenv_user = "vagrant" # vagrant user
$virtualenv_home_path = "/home/$virtualenv_user" # home path of the vagrant user
$virtualenv_path = "$virtualenv_home_path/.virtualenvs/$virtualenv_name" # path of the virtualenv.
$python = "python" # version of python: either python (python2) or python3
$python_path = "/usr/bin/$python"
$requirements_file = "/$virtualenv_user/requirements.txt"
$project_path ="/$virtualenv_user/$virtualenv_name"

$packages = [
"$python",
"$python-dev",
"$python-docutils",
"$python-pip",
"$python-setuptools",
"$python-software-properties",
"$python-tk",
"python-virtualenv",
"virtualenvwrapper"
]
# let's rock!
package { $packages: }

exec { "create-virtualenv-$virtualenv_name":
    command => "virtualenv $virtualenv_path --no-site-packages --distribute -p $python_path",
    require => Package[$packages],
}



}
