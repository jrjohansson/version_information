"""
An IPython extension that provides a magic command that displays
a table with information about versions of dependency modules.
"""
import sys
import os
import time
import IPython

from IPython.display import HTML


def version_information(line=''):

    html = "<table>"
    html += "<tr><th>Software</th><th>Version</th></tr>"

    packages = [("Python", sys.version),
                ("IPython", IPython.__version__),
                ("OS", "%s [%s]" % (os.name, sys.platform))]
    
    modules = line.replace(' ', '').split(",")
    
    for module in modules:
        if len(module) > 0:
            try:
                code = "import %s; version=%s.__version__" % (module, module)
                ns_g = ns_l = {}
                exec(compile(code, "<string>", "exec"), ns_g, ns_l)
                packages.append((module, ns_l["version"]))
            except Exception as e:
                packages.append((module, str(e)))
                
    for name, version in packages:
        html += "<tr><td>%s</td><td>%s</td></tr>" % (name, version)

    html += "<tr><td colspan='2'>%s</td></tr>" % time.strftime('%a %b %d %H:%M:%S %Y %Z')
    html += "</table>"

    return HTML(html)        


def load_ipython_extension(ipython):
    ipython.register_magic_function(version_information)