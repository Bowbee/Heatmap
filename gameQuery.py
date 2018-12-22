import logging
import logging.handlers

from gevent.pool import Pool
from valve.source.master_server import MasterServerQuerier
from valve.source.a2s import ServerQuerier, NoResponseError
from valve.source.messages import BrokenMessageError

MASTER_HOST = 'hl2master.steampowered.com'
MASTER_TIMEOUT = 60
SERVER_TIMEOUT = 5


pool = Pool(size=50)


def get_server_stats(address):
    server = ServerQuerier(address, timeout=SERVER_TIMEOUT)
    try:
        info = server.info()

        logging.info(u'{player_count},{max_players},{server_name}'.format(**info))
        return True
    except (NotImplementedError, NoResponseError, BrokenMessageError):
        pass


def find_servers():
    count = 0
    greenlets = []
    master = MasterServerQuerier(
        address=(MASTER_HOST, 27011), timeout=MASTER_TIMEOUT
    )
    try:
        for address in master.find(region='rest',
                                gamedir=u"atlas"):
            greenlets.append(pool.spawn(get_server_stats, address))
            count += 1
    except NoResponseError as e:
        # Protocol is UDP so there's no "end"
        if u'Timed out' not in e.message:
            logging.warning('Error querying master server: {0}'.format(e))
    finally:
        logging.info('Found {0} addresses'.format(count))
        return greenlets


if __name__ == '__main__':
    while(True):
        handler = logging.handlers.RotatingFileHandler("atlasserver.txt", mode = 'w', backupCount = 1)
        logging.basicConfig(filename="atlasserver.txt", level=logging.INFO, format='%(message)s')
        logging.getLogger().addHandler(handler)
        print("Server running...")
        results = find_servers()

        logging.info('Counting results...')
        results = [result.get() for result in results]

        logging.info('Collected {0}'.format(len(results)))
        #logging.handlers.RotatingFileHandler.doRollover()