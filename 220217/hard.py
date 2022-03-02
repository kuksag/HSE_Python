from datetime import datetime
import multiprocessing as mp
import threading
import codecs
import logging
import time
import os

ARTIFACTS_DIR = 'artifacts'
LOG_NAME = 'hard.txt'
SENT_TIME_MESSAGE_FROM_TO = "{!s}\t Sent {:>16} from {:>16} to {:>16}"
GOT_TIME_MESSAGE_FROM_TO = "{!s}\t Got  {:>16} from {:>16} in {:>16}"


def stdio_reader(writer: mp.Pipe):
    try:
        while True:
            message = input()
            log = [GOT_TIME_MESSAGE_FROM_TO.format(datetime.now(), message, 'stdin', 'main'),
                   SENT_TIME_MESSAGE_FROM_TO.format(datetime.now(), message, 'main', 'process A')]
            writer.send((log, message))
    except EOFError:
        writer.close()


def to_lower(receiver: mp.Pipe, writer: mp.Pipe):
    try:
        while True:
            if receiver.poll(5):
                log, message = receiver.recv()
                log.append(GOT_TIME_MESSAGE_FROM_TO.format(datetime.now(), message, 'main', 'process A'))
                message = message.lower()
                log.append(SENT_TIME_MESSAGE_FROM_TO.format(datetime.now(), message, 'process A', 'process B'))
                time.sleep(5)
                writer.send((log, message))
    except EOFError:
        writer.close()


def rot13(receiver: mp.Pipe, writer: mp.Pipe):
    try:
        while True:
            if receiver.poll(5):
                log, message = receiver.recv()
                log.append(GOT_TIME_MESSAGE_FROM_TO.format(datetime.now(), message, 'process A', 'process B'))
                message = codecs.encode(message, 'rot_13')
                log.append(SENT_TIME_MESSAGE_FROM_TO.format(datetime.now(), message, 'process B', 'main'))
                time.sleep(5)
                writer.send((log, message))
    except EOFError:
        writer.close()


if __name__ == '__main__':
    if not os.path.exists(ARTIFACTS_DIR):
        os.makedirs(ARTIFACTS_DIR)
    logging.basicConfig(filename=os.path.join(ARTIFACTS_DIR, LOG_NAME),
                        level=logging.DEBUG)

    A_receiver, stdio_writer = mp.Pipe(duplex=False)
    B_receiver, A_writer = mp.Pipe(duplex=False)
    main_receiver, B_writer = mp.Pipe(duplex=False)

    io_thread = threading.Thread(target=stdio_reader,
                                 args=(stdio_writer,))
    process_A = threading.Thread(target=to_lower,
                                 args=(A_receiver, A_writer,))
    process_B = threading.Thread(target=rot13,
                                 args=(B_receiver, B_writer,))

    io_thread.start()
    process_A.start()
    process_B.start()

    try:
        while True:
            if main_receiver.poll(5):
                logs, message = main_receiver.recv()
                logs.append(GOT_TIME_MESSAGE_FROM_TO.format(datetime.now(), message, 'process B', 'main'))
                for log in logs:
                    logging.info(log)
                print(message)
    except EOFError:
        pass

    process_B.join()
    process_A.join()
    io_thread.join()
