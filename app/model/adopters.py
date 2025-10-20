#
# Copyright (C) 2019-2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
import glob
import typing
from .. import app


_ADOPTERS_DIRECTORY_PATH = os.path.join(app.root_path, "..", "adopters")


class Adopter:
    def __init__(self, name: str, logo_file_name: str, website: str):
        self.name = str(name)
        self.logo_file_name = str(logo_file_name)

        website = str(website)
        if "://" in website:
            self.website_url = website
        else:
            self.website_url = "http://" + website


def get_list() -> typing.Iterable[Adopter]:
    entries = list(
        sorted(map(os.path.basename, glob.glob(_ADOPTERS_DIRECTORY_PATH + "/*.png")))
    )
    for e in entries:
        name, website = e.rsplit(".", 1)[0].rsplit(" ", 1)
        yield Adopter(name, e, website)


def get_logo_file_path(logo_file_name: str) -> str:
    return os.path.join(_ADOPTERS_DIRECTORY_PATH, logo_file_name)
