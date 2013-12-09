"""
An IPython extension that provides a magic command that displays
a table with information about versions of dependency modules.
"""
import cgi
import json
import os
import sys
import time

import IPython
from IPython.core.magic import magics_class, line_magic, Magics


@magics_class
class VersionInformation(Magics):

    @line_magic
    def version_information(self, line=''):
        """Show information about versions of modules.

        Usage:

            %version_information [optional list of modules]

        """
        self.packages = [("Python", sys.version.replace("\n", "")),
                         ("IPython", IPython.__version__),
                         ("OS", "%s [%s]" % (os.name, sys.platform))]

        modules = line.replace(' ', '').split(",")

        for module in modules:
            if len(module) > 0:
                try:
                    code = "import %s; version=%s.__version__" % (module, module)
                    ns_g = ns_l = {}
                    exec(compile(code, "<string>", "exec"), ns_g, ns_l)
                    self.packages.append((module, ns_l["version"]))
                except Exception as e:
                    self.packages.append((module, str(e)))

        return self


    def _repr_json_(self):
        obj = {
            'Software versions': [
                {'module': name, 'version': version} for
                (name, version) in self.packages]}
        return json.dumps(obj)


    def _repr_html_(self):

        html = "<table>"
        html += "<tr><th>Software</th><th>Version</th></tr>"
        for name, version in self.packages:
            _version = cgi.escape(version)
            html += "<tr><td>%s</td><td>%s</td></tr>" % (name, _version)

        html += "<tr><td colspan='2'>%s</td></tr>" % \
                    time.strftime('%a %b %d %H:%M:%S %Y %Z')
        html += "</table>"

        return html


    @staticmethod
    def _latex_escape(str_):
        CHARS = {
            '&':  r'\&',
            '%':  r'\%',
            '$':  r'\$',
            '#':  r'\#',
            '_':  r'\letterunderscore{}',
            '{':  r'\letteropenbrace{}',
            '}':  r'\letterclosebrace{}',
            '~':  r'\lettertilde{}',
            '^':  r'\letterhat{}',
            '\\': r'\letterbackslash{}',
            '>':  r'\textgreater',
            '<':  r'\textless',
        }
        return u"".join([CHARS.get(c, c) for c in str_])


    def _repr_latex_(self):

        latex = r"\begin{tabular}{|l|l|}\hline" + "\n"
        latex += r"{\bf Software} & {\bf Version} \\ \hline\hline" + "\n"
        for name, version in self.packages:
            _version = self._latex_escape(version)
            latex += r"%s & %s \\ \hline" % (name, _version) + "\n"

        latex += r"\hline \multicolumn{2}{|l|}{%s} \\ \hline" % \
                    time.strftime('%a %b %d %H:%M:%S %Y %Z') + "\n"
        latex += r"\end{tabular}" + "\n"

        return latex


    def _repr_pretty_(self, pp, cycle):

        text = "Software versions\n"
        for name, version in self.packages:
            text += "%s %s\n" % (name, version)

        text += "\n%s" % time.strftime('%a %b %d %H:%M:%S %Y %Z')

        pp.text(text)


def load_ipython_extension(ipython):
    ipython.register_magics(VersionInformation)
