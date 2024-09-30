# Description
**encrypted-relwarc** is a Python-based application that aims to encrypt text-based files within a given directory. The encryption process involves multiple methods of encryption such as base64, jwt, and randomization. The output of the procedure is a list of files with encrypted content. Each file within the resulting set corresponds to **at least** 1 file from the source directory. The application is also capable of recreating the source directory and its files from within a directory where the encrypted files are stored in as long as the keys provided in the required environment variables are the same with that of the encryption.

# Usage
The command signature is  
`python encrypter.py <ENCRYPT|DECRYPT> <.env>`.
- The first argument could either be of value **ENCRYPT** or **DECRYPT** depending on the procedure to be executed.
- The second argument is the env file path to be used by the application. The env file provided will be loaded via the **dotenv** library.

# Requirements
## Python Version
The application was implemented and tested via Python 3.12, and will require the same.

## Python Libraries
The python libraries required by the application are listed in **requirements.txt**. It can be referenced for the creation of a virtual env for the application.

## Environment Files and Variables
The application requires the definition of Environment Variables provided via an Environment File. Each variable is as follows:
### DIR
For argument of type _ENCRYPT_, the **DIR** must contain a string indicating a directory path where the set of files and directories to be encrypted are located. Likewise for _DECRYPT_ mode, the **DIR** must contain a string indicating a directory path where the list of encrypted files to be decrypted are located.
### OUTPUT_DIR
**OUTPUT_DIR** must contain a string indicating a directory path where the output files would be  created. For _ENCRYPT_ mode, the directory will contain the encrypted files. Otherwise for _DECRYPT_ the directory will contain the recreated and / or decrypted files.
### EXCEMPTIONS
**EXCEMPTIONS** must contain a comma-separated list of strings. The application will then ignore any file containing at least one of the provided strings. If _NONE_ is provided, the application will attempt to encrypt / decrypt all files within the provided directory **DIR**.
### BACKSLASHES
**BACKSLASHES** must contain a comma-separated list of strings. The application will then randomly choose one of these (along with the actual newline character) to replace newlines with. Each string must be unique enough to be discernible during the _DECRYPT_ mode. If _None_ is provided, newlines will remain as-is. Strings included in the **BACKSLASHES** variable must neither be included, nor be a substring of an entry in **FILE_DIVIDERS**.
### FILE_DIVIDERS
**FILE_DIVIDERS** must contain a comma-separated list of strings. The application will then randomly choose one of these to replace indicate an encrypted file. Each string must be unique enough to be discernible during the _DECRYPT_ mode. If _None_ is provided, the application will default to the value of _======_. Strings included in the **FILE_DIVIDERS** variable must neither be included, nor be a substring of an entry in **BACKSLASHES**.
### SECRETS
**SECRETS** must contain a comma-separated list of strings. The application will then utilize them randomly to encrypt / decrypt each textual line into / from JWTs. This variable is required and must not be left blank. The number of secrets provided indicates the difficulty of decrypting the encrypted files.
### ISS
A string value indicating the JWT issuer. If _None_ is provided, will default to _relwarc_iss_.
### AUD
A string value indicating the JWT audience. If _None_ is provided, will default to _relwarc_aud_.
### MAX_IN_ONE_FILE
**MAX_IN_ONE_FILE** must contain an integer to indicate the maximum number of files that can be within a single encrypted file. The number of files within the encrypted file is randomly selected from 1 to _MAX_IN_ONE_FILE_ value. If _None_ is provided, the application will default to a value of _5_. **ONLY** applicable in _ENCRYPT_ mode.
### OUTPUT_FILE_PREFIX
**OUTPUT_FILE_PREFIX** must contain a string to serve as the prefix of the resulting set of files. For instance, if the value provided is _out_, then the resulting files would be named _out0, out1, ..., outn_. If _None_ is provided, the application will default to _out_.

# Examples