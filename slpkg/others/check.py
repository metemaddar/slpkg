#!/usr/bin/python
# -*- coding: utf-8 -*-

# check.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from sizes import units
from repositories import Repo
from messages import template
from blacklist import BlackList
from init import Initialization
from splitting import split_package
from colors import YELLOW, GREY, ENDC
from __metadata__ import slpkg_tmp, pkg_path, lib_path


from pkg.manager import PackageManager

from slack.remove import delete
from slack.slack_version import slack_ver

from greps import repo_data
from download import packages_dwn


class OthersUpgrade(object):

    def __init__(self, repo, version):
        self.repo = repo
        self.version = version
        self.tmp_path = slpkg_tmp + "packages/"
        self.repo_init()
        repos = Repo()
        sys.stdout.write("{0}Reading package lists ...{1}".format(GREY, ENDC))
        sys.stdout.flush()
        self.step = 700
        repos = Repo()
        if self.repo == "rlw":
            lib = lib_path + "rlw_repo/PACKAGES.TXT"
            self.mirror = "{0}{1}/".format(repos.rlw(), slack_ver())
        elif self.repo == "alien":
            lib = lib_path + "alien_repo/PACKAGES.TXT"
            self.mirror = repos.alien()
            self.step = self.step * 2
        elif self.repo == "slacky":
            lib = lib_path + "slacky_repo/PACKAGES.TXT"
            arch = ""
            if os.uname()[4] == "x86_64":
                arch = "64"
            self.mirror = "{0}slackware{1}-{2}/".format(repos.slacky(), arch,
                                                        slack_ver())
            self.step = self.step * 2
        f = open(lib, "r")
        self.PACKAGES_TXT = f.read()
        f.close()

    def repo_init(self):
        '''
        Initialization repository if only use
        '''
        if not os.path.exists(slpkg_tmp):
            os.mkdir(slpkg_tmp)
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        repository = {
            'rlw': Initialization().rlw,
            'alien': Initialization().alien,
            'slacky': Initialization().slacky
        }
        repository[self.repo]()

    def start(self):
        '''
        Install packages from official Slackware distribution
        '''
        try:
            dwn_links, upgrade_all, comp_sum, uncomp_sum = self.store()
            sys.stdout.write("{0}Done{1}\n".format(GREY, ENDC))
            print   # new line at start
            if upgrade_all:
                template(78)
                print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
                    "| Package", " " * 17,
                    "Version", " " * 12,
                    "Arch", " " * 4,
                    "Build", " " * 2,
                    "Repos", " " * 10,
                    "Size"))
                template(78)
                print("Upgrading:")
                views(upgrade_all, comp_sum, self.repo)
                unit, size = units(comp_sum, uncomp_sum)
                msg = msgs(upgrade_all)
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total {1} {2} will be upgraded.".format(
                    GREY, len(upgrade_all), msg))
                print("Need to get {0} {1} of archives.".format(size[0],
                                                                unit[0]))
                print("After this process, {0} {1} of additional disk "
                      "space will be used.{2}".format(size[1], unit[1], ENDC))
                read = raw_input("\nWould you like to upgrade [Y/n]? ")
                if read in ['Y', 'y']:
                    upgrade_all.reverse()
                    packages_dwn(self.tmp_path, dwn_links)
                    upgrade(upgrade_all)
                    delete(self.tmp_path, upgrade_all)
            else:
                print("There are no packages for upgrade\n")
        except KeyboardInterrupt:
            print   # new line at exit
            sys.exit()

    def store(self):
        '''
        Store and return packages for install
        '''
        dwn, install, comp_sum, uncomp_sum = ([] for i in range(4))
        black = BlackList().packages()
        # name = data[0]
        # location = data[1]
        # size = data[2]
        # unsize = data[3]
        installed = self.installed()
        data = repo_data(self.PACKAGES_TXT, self.step, self.repo, self.version)
        for pkg in installed:
            for name, loc, comp, uncomp in zip(data[0], data[1], data[2],
                                               data[3]):
                inst_pkg = split_package(pkg)
                repo_pkg = split_package(name[:-4])
                if repo_pkg[0] == inst_pkg[0] and name[:-4] > pkg \
                        and inst_pkg[0] not in black:
                    # store downloads packages by repo
                    dwn.append("{0}{1}/{2}".format(self.mirror, loc, name))
                    install.append(name)
                    comp_sum.append(comp)
                    uncomp_sum.append(uncomp)
        return [dwn, install, comp_sum, uncomp_sum]

    def installed(self):
        '''
        Return all installed packages by repository
        '''
        packages = []
        repository = {
            'rlw': '_rlw',
            'alien': 'alien',
            'slacky': 'sl'
        }
        repo = repository[self.repo]
        for pkg in os.listdir(pkg_path):
            if pkg.endswith(repo):
                packages.append(pkg)
        return packages


def views(upgrade_all, comp_sum, repository):
    '''
    Views packages
    '''
    upg_sum = 0
    # fix repositories align
    align = {
        'rlw': ' ' * 3,
        'alien': ' ',
        'slacky': ''
    }
    repository += align[repository]
    for pkg, comp in zip(upgrade_all, comp_sum):
        pkg_split = split_package(pkg[:-4])
        upg_sum += 1
        print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11:>11}{12}".format(
            YELLOW, pkg_split[0], ENDC,
            " " * (25-len(pkg_split[0])), pkg_split[1],
            " " * (19-len(pkg_split[1])), pkg_split[2],
            " " * (8-len(pkg_split[2])), pkg_split[3],
            " " * (7-len(pkg_split[3])), repository,
            comp, " K"))
    return upg_sum


def msgs(upgrade_all):
    '''
    Print singular plural
    '''
    msg_pkg = "package"
    if len(upgrade_all) > 1:
        msg_pkg = msg_pkg + "s"
    return msg_pkg


def upgrade(upgrade_all):
    '''
    Install or upgrade packages
    '''
    for pkg in upgrade_all:
        print("[ {0}upgrading{1} ] --> {2}".format(YELLOW, ENDC, pkg[:-4]))
        PackageManager(pkg).upgrade()