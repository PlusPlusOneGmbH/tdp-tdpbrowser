__minimum_td_version__ = "2025.32460"

from . import Browser

from td import COMP, root, baseCOMP


_ToxFiles  = {
    "Browser" : Browser.ToxFile
}

def Setup(home_op:COMP = None):
    browser = (home_op or root.op("utils") or root.create(baseCOMP, "utils")).loadTox( Browser.ToxFile )
    browser.par.externaltox.expr = f"mod.tdptdpbrowser.Browser.ToxFile"
    browser.par.enableexternaltox.val = True
    browser.par.enableexternaltoxpulse.pulse()
