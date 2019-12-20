import logging
from random import choice, random
from subprocess import run, PIPE
from pwnagotchi.plugins import Plugin

'''
This needs the fortune program installed along with a database of fortunes.
To install with just a minimal database of fortunes:
> apt-get install fortune-mod
To install with a larger database of fortunes:
> apt-get install fortune-mod fortunes
To install with a database of fortunes for some language other than English,
> apt-get install fortune-mod fortunes-XX
where XX is one of: bg, br, cs, de, eo, es, fr, ga, it, pl, ru, zh.

The fortune command may be completely replaced by setting alt_cmd in the
configuration file.
'''


class Fortune(Plugin):
    __author__ = '@Feneric'
    __version__ = '0.1.0'
    __license__ = 'GPL3'
    __description__ = 'Alleviate a little boredom by quoting random fortunes.'

    def __init__(self):
        # The fortune program only supports a dozen languages at the moment.
        self.langs = ('bg', 'br', 'cs', 'de', 'eo', 'es', 'fr', 'ga', 'it', 'pl', 'ru', 'zh')
        self.fortune = ""

    def set_fortune(self, agent):
        display = agent.view()
        config = agent.config()
        try:
            lang = config['main']['lang'][:2]
            if lang not in self.langs:
                lang = ''
        except KeyError:
            lang = ''
        try:
            alt_cmd = config['plugins']['fortune']['alt_cmd']
        except KeyError:
            alt_cmd = ''
        cmd = alt_cmd.split() or ['/usr/games/fortune', '-s', '-n', '120', lang]
        proc = run(cmd, stdout=PIPE)
        self.fortune = proc.stdout.decode('utf-8')
        logging.info("[fortune] {}".format(self.fortune))
        display.update(force=True)

    def on_loaded(self):
        logging.info("Fortune plugin loaded")

    def on_bored(self, agent):
        if random() > .5:
            self.set_fortune(agent)

    def on_lonely(self, agent):
        if random() > .8:
            self.set_fortune(agent)

    def on_sad(self, agent):
        if random() > .9:
            self.set_fortune(agent)

    def on_ui_update(self, ui):
        if self.fortune:
            ui.set('face', choice(['(☉‗☉ )', '( ☉‗☉)']))
            ui.set('status', self.fortune)
            self.fortune = ""
