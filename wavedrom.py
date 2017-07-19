import IPython.core.display
import IPython.display
import json
import os
import subprocess

def _draw_wavedrom_javascript(data, width):
    style = ""
    if width != None:
        style = ' style="width: ' + str(int(width)) + 'px"'
    htmldata = '<div' + style + '><script type="WaveDrom">' + json.dumps(data) + '</script></div>'
    IPython.core.display.display_html(IPython.core.display.HTML(htmldata))
    jsdata = 'WaveDrom.ProcessAll();'
    IPython.core.display.display_javascript(IPython.core.display.Javascript(
        data=jsdata, lib=['files/js/wavedrom.min.js', 'files/js/wavedromskin.js']))

def _draw_wavedrom_phantomjs(data, phantomjs):
    prog = subprocess.Popen([phantomjs, 'js/wavedrom-cli.js', '-i', '-', '-s', '-'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = prog.communicate(json.dumps(data).encode('utf-8'))
    return IPython.display.SVG(stdout)

def _is_exe(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def _find_phantomjs(program='phantomjs'):
    fpath, _ = os.path.split(program)
    if fpath:
        if _is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if _is_exe(exe_file):
                return exe_file
    return False

def draw_wavedrom(data, width=None, phantomjs=None):
    """
    A function to provide digital waveform drawing in ipython notebook.
    It utilises the wavedrom java script library, documentation for which can
    be found here: wavedrom.com.

    Example usage:
        import wavedrom
        a = {
        'signal': [
          {'name': 'clk', 'wave': 'p.....|...'},
          {'name': 'dat', 'wave': 'x.345x|=.x', 'data': ['head', 'body', 'tail', 'data']},
          {'name': 'req', 'wave': '0.1..0|1.0'},
          {},
          {'name': 'ack', 'wave': '1.....|01.'}
        ]}
        wavedrom.draw_wavedrom(a)

    Note, there are two wavedrom rendering engines built in. The default is to use the
    wavedrom-cli (https://github.com/wavedrom/cli). This requires phantomjs. This is the
    best option as it embeds the SVG into the notebook. If phantomjs is not found then a
    browser based render will be used, this means that the notebook can't be converted to
    PDF or displayed on github.

    The following arguments are used:
    * data - the wavedrom configuration (see wavedrom.com)
    * width - forces max width of the output when using browser rendering
    * phantomjs - set to the path to phantomjs if it is not in your PATH
    """
    if phantomjs != False:
        if phantomjs is None or phantomjs is True:
            phantomjs = _find_phantomjs() # Search it in path
        else:
            phantomjs = _find_phantomjs(phantomjs) # Search it with user path
    if phantomjs is False:
        _draw_wavedrom_javascript(data, width)
    else:
        return _draw_wavedrom_phantomjs(data, phantomjs)
