JobPlus Project
===============

Authors     :   [firethoughts Ltd] (http://www.firethoughts.com/)

Version     :   0.0.1

Description :   Job Portal built MEANly!

License     :   MIT

------------------------------------------------------------------------

Hardware Requirements
---------------------

-   Your PC/laptop has a processor which is **64-bit capable (Intel Core 2 Duo+)**.
-   Your PC/laptop has a minimum of **1GB RAM memory**.
-   Your PC/laptop has broadband/internet access of at least **2Mbps+**.

Software Requirements
---------------------

-   Your PC/laptop has a copy of **Windows, Linux or Mac OSX** operating system installed.
-   Install the latest version of [Git] (http://git-scm.com/).
-   Install the latest version of [Git Flow] (https://github.com/nvie/gitflow)
-   Install the latest version of [VirtualBox] (http://www.virtualbox.org/wiki/Downloads). Recommended version:: 4.3.18
-   Install the latest version of [VirtualBox Extensions Pack] (http://www.virtualbox.org/wiki/Downloads). Recommended version:: 4.3.18
-   Install the latest version of [Vagrant] (http://www.vagrantup.com/downloads.html). Recommended version:: 1.6.5
-   Install the latest version of [Vagrant Cachier Plugin] (https://github.com/fgrehm/vagrant-cachier).
-   Grab a code editor like [Vim] (http://www.vim.org/download.php).


Cloning the Project Repository
------------------------------

You can get the code in two ways via the [Code Repo] (http://code.firethoughts.com/).

> -  **(SSH Mode) git clone git@code.firethoughts.com:devs/jobplus.git**
> -  **(HTTP Mode) git clone http://code.firethoughts.com/devs/jobplus.git**

Running the Project
-------------------

After successfully cloning the repository, launch “Terminal or Console" and
run the following commands in order:

> 1.  **vagrant up** (Approx. 5-30 minutes based on internet connectivity)
> 2.  **vagrant ssh** (SSH connection into the guest machine)

NB: Windows users only.
The performance for accesses to shared folders from a Windows guest might be decreased due to delays during the resolution of the VirtualBox shared folders name service.
To fix these delays, add the following entries to the file \windows\system32\drivers\etc\lmhosts of the Windows guest:

- 255.255.255.255        VBOXSVR #PRE
- 255.255.255.255        VBOXSRV #PRE

After doing this change, a reboot of the guest machine is required.

Using a terminal window, Navigate to project/server folder
> -  **npm install --no-bin-links** (Install dependencies on API server -- may require sudo)
> -  **npm start** (Runs the API Server)

Using a terminal window, Navigate to project/admin folder
> -  **npm install --no-bin-links** (Install dependencies on Admin app -- may require sudo)
> -  **npm start** (Runs the project)

Using a terminal window, Navigate to project/client folder
> -  **npm install --no-bin-links** (Install dependencies on Client app -- may require sudo)
> -  **npm start** (Runs the project)

Viewing the Project
-------------------

On the host machine, open your favourite internet browser and navigate
to:

> -   **<http://localhost:5000>** (for api client)
> -   **<http://localhost:3000>** (for web client)
> -   **<http://localhost:4000>** (for admin client)


Installing NPM Requirements
---------------------------

This is used mainly for Javascript side dependencies.

On the guest virtual machine, if you need to install npm libs:

> -  Make sure you're in the project/client or project/server folder.
> -  **npm install \<package\>@\<version\> --save --no-bin-links** (e.g npm install express@4.8.5 --save --no-bin-links) (NB:may require sudo)



