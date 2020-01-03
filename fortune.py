import logging
from random import choice, random
from subprocess import run, PIPE
import pwnagotchi.plugins as plugins

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


class Fortune(plugins.Plugin):
    __author__ = '@Feneric'
    __version__ = '0.2.0'
    __license__ = 'GPL3'
    __description__ = 'Alleviate a little boredom by quoting random fortunes.'

    # The fortune program only supports a dozen languages at the moment.
    __langs = ('bg', 'br', 'cs', 'de', 'eo', 'es', 'fr', 'ga', 'it', 'pl', 'ru', 'zh')

    def set_fortune(self, agent):
        display = agent.view()
        config = agent.config()
        try:
            lang = config['main']['lang'][:2]
        except KeyError:
            lang = 'en'
        if lang not in Fortune.__langs:
            lang = ''
        try:
            alt_cmd = config['main']['plugins']['fortune']['alt_cmd']
        except KeyError:
            alt_cmd = ''
        try:
            fortune_length = config['main']['plugins']['fortune']['length']
        except KeyError:
            fortune_length = 120
        cmd = alt_cmd.split() or ['/usr/games/fortune', '-s', '-n', str(fortune_length), lang]
        proc = run(cmd, stdout=PIPE)
        fortune = proc.stdout.decode('utf-8')
        logging.info("[fortune] {}".format(fortune))
        face = choice(['(☉‗☉ )', '( ☉‗☉)'])
        display.update(force=True, new_data={'face': face, 'status': fortune})

    def on_loaded(self):
        logging.info("Fortune plugin loaded")

    def on_bored(self, agent):
        if random() > .5:
            self.set_fortune(agent)

    def on_lonely(self, agent):
        if random() > .7:
            self.set_fortune(agent)

    def on_sad(self, agent):
        if random() > .8:
            self.set_fortune(agent)
