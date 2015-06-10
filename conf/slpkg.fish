complete --command slpkg --long-option help --short-option h --description 'Print this help message and exit.'
complete --command slpkg --long-option version --short-option v --description 'Print program version and exit.'
complete --command slpkg --long-option autobuild --short-option a  --description 'Auto build SBo packages. If you already have downloaded the script and the source code you can build a new package with this command.'
complete --command slpkg --long-option blacklist --short-option b --description 'Manage packages in the blacklist. Add or remove packages and print the list. Each package is added here will not be accessible by the program.'
complete --command slpkg --long-option queue --short-option q --description 'Manage SBo packages in the queue. Add or remove and print the list build-install of packages. Build and then install the packages from the queue.'
complete --command slpkg --long-option config --short-option g --description 'Configuration file management. Print the configuration file or edit.'
complete --command slpkg --long-option list --short-option l --description 'Print a list of all available packages repository index or print only packages installed on the system.'
complete --command slpkg --long-option check --short-option c --description 'Check view and install updated packages from repositories.'
complete --command slpkg --long-option sync --short-option s --description 'Sync packages. Install packages directly from remote repositories with all dependencies.'
complete --command slpkg --long-option tracking --short-option t --description 'Tracking package dependencies and print package dependenies tree with highlight if packages is installed.'
complete --command slpkg --long-option print --short-option p --description 'Print description of a package directly from the repository and change color text.'
complete --command slpkg --long-option network --short-option n --description 'View a standard of SBo page in terminal and manage multiple options like reading downloading building installation etc.'
complete --command slpkg --long-option find --short-option f --description 'Find and print installed packages reporting the size and the sum.'
complete --command slpkg --long-option FIND --short-option F --description 'Find packages from repositories and search at each enabled repository and prints results.'
complete --command slpkg --long-option install --short-option i --description 'Installs single or multiple Slackware binary packages.'
complete --command slpkg --long-option install-new --short-option u --description 'Upgrade single or multiple Slackware binary packages from a older to a newer one.'
complete --command slpkg --long-option reinstall --short-option o --description 'Reinstall signle or multiple Slackware binary packages with the same packages if the exact.'
complete --command slpkg --long-option remove --short-option r --description 'Removes a previously installed Slackware binary packages.'
complete --command slpkg --long-option display --short-option d --description 'Display the installed packages contents and file list.'
