"""
    Plugin for ResolveURL
    Copyright (C) 2016 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import re
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError


class VoyeurhitResolver(ResolveUrl):
    name = 'voyeurhit'
    domains = ['voyeurhit.com']
    pattern = r'(?://|\.)(voyeurhit\.com)/(?:videos|embed)/([\w\-]+)'

    def get_media_url(self, host, media_id):
        if not media_id.isdigit():
            web_url = self.get_url(host, media_id)
            headers = {'User-Agent': common.RAND_UA}
            html = self.net.http_GET(web_url, headers=headers).content
            embed = re.search(r"""<iframe.+?src=['"](http://voyeurhit.com/embed/\d+)""", html, re.I)
            if embed:
                return helpers.get_media_url(embed.group(1), patterns=[r"""video_url:\s*['"](?P<url>.+?)(?:/\?[^"']+)?["']"""]).replace(' ', '%20')

            raise ResolverError('File not found')

        else:
            return helpers.get_media_url(self.get_url(host, media_id), patterns=[r"""video_url:\s*['"](?P<url>.+?)(?:/\?[^"']+)?["']"""]).replace(' ', '%20')

    def get_url(self, host, media_id):
        if not media_id.isdigit():
            return self._default_get_url(host, media_id, template='http://{host}/videos/{media_id}/')
        else:
            return self._default_get_url(host, media_id, template='http://{host}/embed/{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True
