import syncall
import logging

from events import Event


MSG_INDEX = 1


class RemoteStore:
    """ Manages communication to a single remote SyncAll instance. """

    def __init__(self, messanger, directory):
        self.logger = logging.getLogger(__name__)

        self.messanger = messanger
        self.directory = directory
        self.file_manager = syncall.FileManager(self)

        self.remote_index = None

        self.address = self.messanger.address[0]
        self.uuid = self.messanger.remote_uuid

        self.disconnected = Event()
        self.messanger.disconnected += self.__disconnected
        self.messanger.packet_received += self._packet_received

    def index_received(self):
        return self.remote_index is not None

    def start_receiving(self):
        self.messanger.start_receiving()

        self.messanger.send({
            'type': MSG_INDEX,
            'index': self.directory.get_index()
        })

    def __disconnected(self, no_data):
        self.disconnected.notify(self)
        self.file_manager.stop_transfers()

    def disconnect(self):
        self.messanger.disconnect()

    def _packet_received(self, packet):
        self.logger.debug("Received packet from {}: {}".format(
            self.address,
            packet['type']
        ))

        if 'type' not in packet:
            self.logger.error("Received packet with no type from {}".format(
                self.address
            ))

        if packet['type'] == MSG_INDEX:
            self.remote_index = packet['index']
            self.__remote_index_updated()

        else:
            self.logger.error("Unknown packet from {}: {}".format(
                self.address,
                packet['type']
            ))

    def __remote_index_updated(self):
        self.logger.debug("{}'s index updated".format(self.address))

        diff = self.directory.diff(self.remote_index)

        # TODO: Handle deleted and conflicted files
        self.file_manager.sync_files(diff[0])
