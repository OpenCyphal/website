#
# Copyright (C) 2019-2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
import glob
import typing
from .. import app


_ADOPTERS_DIRECTORY_PATH = os.path.join(app.root_path, '..', 'adopters')


class Adopter:
    def __init__(self, name: str, logo_file_name: str, website: str):
        self.name = str(name)
        self.logo_file_name = str(logo_file_name)

        website = str(website)
        if '://' in website:
            self.website_url = website
        else:
            self.website_url = 'http://' + website


def get_adopters() -> list:
    tiered_adopters=[[] for i in range(10)]
    entries = list(map(os.path.basename, glob.glob(_ADOPTERS_DIRECTORY_PATH + '/*.png')))

    for e in entries:
        name, website = e[2:].rsplit('.', 1)[0].rsplit(' ', 1)
        tiered_adopters[int(e[0:1])].append(Adopter(name, e, website))

    return tiered_adopters


def get_logo_file_path(logo_file_name: str) -> str:
    return os.path.join(_ADOPTERS_DIRECTORY_PATH, logo_file_name)
