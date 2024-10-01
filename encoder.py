import os, sys
from dotenv import load_dotenv
load_dotenv('.env' if (len(sys.argv) == 2) else sys.argv[2])
from utils import Encoder, Decoder

if __name__ == '__main__':
    if sys.argv[1].upper() == 'ENCODE':
        enc = Encoder(
            os.getenv('DIR'),
            os.getenv('OUTPUT_DIR'),
            os.getenv('OUTPUT_FILE_PREFIX'),
            os.getenv('FILE_DIVIDERS').split(',') if os.getenv('FILE_DIVIDERS') else None,
            os.getenv('EXCEMPTIONS').split(',') if os.getenv('EXCEMPTIONS') else [],
            os.getenv('BACKSLASHES').split(',') if os.getenv('BACKSLASHES') else [],
            os.getenv('SECRETS').split(',') if os.getenv('SECRETS') else [],
            os.getenv('ISS') if os.getenv('ISS') else 'relwarc_iss',
            os.getenv('AUD') if os.getenv('AUD') else 'relwarc_aud',
            os.getenv('MAX_IN_ONE_FILE') if os.getenv('MAX_IN_ONE_FILE') else '5'
        )
    elif sys.argv[1].upper() == 'DECODE':
        enc = Decoder(
            os.getenv('DIR'),
            os.getenv('OUTPUT_DIR'),
            os.getenv('ENCODED_FILE_PREFIX'),
            os.getenv('FILE_DIVIDERS').split(',') if os.getenv('FILE_DIVIDERS') else None,
            # os.getenv('EXCEMPTIONS').split(',') if os.getenv('EXCEMPTIONS') else [],
            os.getenv('BACKSLASHES').split(',') if os.getenv('BACKSLASHES') else [],
            os.getenv('SECRETS').split(',') if os.getenv('SECRETS') else [],
            os.getenv('ISS') if os.getenv('ISS') else 'relwarc_iss',
            os.getenv('AUD') if os.getenv('AUD') else 'relwarc_aud',
            os.getenv('KEYS_DIR')
        )
    else:
        raise KeyError('INVALID MODE ARGUMENT: ' + sys.argv[1])
    enc.start()