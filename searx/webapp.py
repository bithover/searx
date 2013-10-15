#!/usr/bin/env python

'''
searx is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

searx is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with searx. If not, see < http://www.gnu.org/licenses/ >.

(C) 2013- by Adam Tauber, <asciimoo@gmail.com>
'''

if __name__ == "__main__":
    from sys import path
    from os.path import realpath, dirname
    path.append(realpath(dirname(realpath(__file__))+'/../'))

from flask import Flask, request, flash, render_template
import ConfigParser
from os import getenv
from searx.engines import search, engines

cfg = ConfigParser.SafeConfigParser()
cfg.read('/etc/searx.conf')
cfg.read(getenv('HOME')+'/.searxrc')
cfg.read(getenv('HOME')+'/.config/searx/searx.conf')
cfg.read('searx.conf')


app = Flask(__name__)
app.secret_key = cfg.get('app', 'secret_key')

def render(template_name, **kwargs):
    kwargs['engines'] = engines.keys()
    return render_template(template_name, **kwargs)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        if not request.form.get('q'):
            flash('Wrong post data')
            return render('index.html')
        query = request.form['q']
        results = search(query, request)
        return render('results.html', results=results, q=query)
    return render('index.html')

if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()

    app.run(debug        = cfg.get('server', 'debug')
           ,use_debugger = cfg.get('server', 'debug')
           ,port         = int(cfg.get('server', 'port'))
           )
