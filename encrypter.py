import os, sys
from dotenv import load_dotenv
load_dotenv('.env' if (len(sys.argv) == 2) else sys.argv[2])
from utils import Encoder, Decoder

if __name__ == '__main__':
    if sys.argv[1].upper() == 'ENCRYPT':
        enc = Encoder(
            os.getenv('DIR'),
            os.getenv('OUTPUT_DIR'),
            os.getenv('OUTPUT_FILE_PREFIX'),
            os.getenv('FILE_DIVIDER'),
            os.getenv('EXCEMPTIONS').split(',') if os.getenv('EXCEMPTIONS') else [],
            os.getenv('BACKSLASHES').split(',') if os.getenv('BACKSLASHES') else [],
            os.getenv('SECRETS').split(',') if os.getenv('SECRETS') else [],
            os.getenv('ISS'),
            os.getenv('AUD'),
            os.getenv('MAX_IN_ONE_FILE')
        )
    elif sys.argv[1].upper() == 'DECRYPT':
        enc = Decoder(
            os.getenv('DIR'),
            os.getenv('OUTPUT_DIR'),
            os.getenv('FILE_DIVIDER'),
            os.getenv('EXCEMPTIONS').split(',') if os.getenv('EXCEMPTIONS') else [],
            os.getenv('BACKSLASHES').split(',') if os.getenv('BACKSLASHES') else [],
            os.getenv('SECRETS').split(',') if os.getenv('SECRETS') else [],
            os.getenv('ISS'),
            os.getenv('AUD')
        )
    else:
        raise KeyError('INVALID MODE ARGUMENT: ' + sys.argv[1])
    enc.start()