/*
 * Copyright (C) 2021 desklab gUG
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

{% load l10n %}
'use strict';

let mapboxgl = gcampus.mapboxgl;

mapboxgl.accessToken = '{{ mapbox_access_token }}'
const map = new mapboxgl.Map({
    container: '{{ container }}',
    style: '{{ mapbox_style }}',
    center: [{{ center_lng|unlocalize }}, {{ center_lat }}],
    zoom: {{ zoom }},
    attributionControl: false
});
map.addControl(
    new mapboxgl.AttributionControl({ compact: true})
);
var nav = new mapboxgl.NavigationControl();
map.addControl(nav, 'top-left');

{% if onload %}
map.on('load', {{ onload }});
{% endif %}

if (window._maps === undefined) {
    window._maps = {};
}
window._maps['{{ name }}'] = map;
