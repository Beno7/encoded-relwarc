# Description
**encoded-relwarc** is a Python-based application that aims to encode text-based files within a given directory. The encoding process involves multiple methods of encoding such as base64, jwt, and randomization. The output of the procedure is a list of files with encoded content. Each file within the resulting set corresponds to **at least** 1 file from the source directory. The application is also capable of recreating the source directory and its files from within a directory where the encoded files are stored in as long as the keys provided in the required environment variables are the same with that of the encoding.

# Usage
The command signature is  
`python encoder.py <ENCODE|DECODE> <.env>`.
- The first argument could either be of value **ENCODE** or **DECODE** depending on the procedure to be executed.
- The second argument is the env file path to be used by the application. The env file provided will be loaded via the **dotenv** library.

# Requirements
## Python Version
The application was implemented and tested via Python 3.12, and will require the same.

## Python Libraries
The python libraries required by the application are listed in **requirements.txt**. It can be referenced for the creation of a virtual env for the application.

## Environment Files and Variables
The application requires the definition of Environment Variables provided via an Environment File. Each variable is as follows:
### DIR
For argument of type _ENCODE_, the **DIR** must contain a string indicating a directory path where the set of files and directories to be encoded are located. Likewise for _DECODE_ mode, the **DIR** must contain a string indicating a directory path where the list of encoded files to be decoded are located. The directory could either be an absolute or a relative path.
### OUTPUT_DIR
**OUTPUT_DIR** must contain a string indicating a directory path where the output files would be created. For _ENCODE_ mode, the directory will contain the encoded files. Otherwise for _DECODE_ the directory will contain the recreated and / or decoded files. The directory could either be an absolute or a relative path. Defaults to *enc_out* in _ENCODE_ mode, and *dec_out* in _DECODE_ mode.
### EXCEMPTIONS
**EXCEMPTIONS** must contain a comma-separated list of strings. The application will then ignore any file with a filename containing at least one of the provided strings. If _NONE_ is provided, the application will attempt to encode / decode all files within the provided directory **DIR**. Only applicable in mode _DECODE_
### BACKSLASHES
**BACKSLASHES** must contain a comma-separated list of strings. The application will then randomly choose one of these (along with the actual newline character) to replace newlines with. Each string must be unique enough to be discernible during the _DECODE_ mode. If _None_ is provided, newlines will remain as-is. Strings included in the **BACKSLASHES** variable must neither be included, nor be a substring of an entry in **FILE_DIVIDERS**. The order of values in the comma-separated list need not matter in either the _ENCODE_ and _DECODE_ mode.
### FILE_DIVIDERS
**FILE_DIVIDERS** must contain a comma-separated list of strings. The application will then randomly choose one of these to replace indicate an encoded file. Each string must be unique enough to be discernible during the _DECODE_ mode. If _None_ is provided, the application will default to the value of _======_. Strings included in the **FILE_DIVIDERS** variable must neither be included, nor be a substring of an entry in **BACKSLASHES**. The order of values in the comma-separated list need not matter in either the _ENCODE_ and _DECODE_ mode.
### SECRETS
**SECRETS** must contain a comma-separated list of strings. The application will then utilize them randomly to encode / decode each textual line into / from JWTs. This variable is required and must not be left blank. The number of secrets provided indicates the difficulty of decoding the encoded files. The order of values in the comma-separated list must be the same during both of the _ENCODE_ and _DECODE_ modes.
### ISS
A string value indicating the JWT issuer. If _None_ is provided, will default to _relwarc_iss_.
### AUD
A string value indicating the JWT audience. If _None_ is provided, will default to _relwarc_aud_.
### MAX_IN_ONE_FILE
**MAX_IN_ONE_FILE** must contain an integer to indicate the maximum number of files that can be within a single encoded file. The number of files within the encoded file is randomly selected from 1 to _MAX_IN_ONE_FILE_ value. If _None_ is provided, the application will default to a value of _5_. **ONLY** applicable in _ENCODE_ mode.
### OUTPUT_FILE_PREFIX
**OUTPUT_FILE_PREFIX** must contain a string to serve as the prefix of the resulting set of encoded files during _ENCODE_ mode. For instance, if the value provided is _out_, then the resulting files would be named _out0, out1, ..., outn_. If _None_ is provided, the application will default to _out_. For _DECODE_ mode, the application will only attempt to decode files that starts with the value of **OUTPUT_FILE_PREFIX**.
### KEYS_DIR
**KEYS_DIR** must contain the path of the keys file generated during the _ENCODE_ mode. Can contain either an absolute or relative path. If a relative path is provided, the path value will be concatenated to the **DIR** variable's value. **ONLY** applicable during _DECODE_ mode.

# Notes
- The encoding process will generate a key file required during the _DECODE_ mode. The generated file will be of format `<uuidv4>.keys`. The contents of the file will also be printed out upon _ENCODE_ mode execution.
- The contents of the files generated during _ENCODE_ mode must not be changed prior to the execution of _DECODE_ mode.
- The names of the generated _ENCODE_ files must not be altered prior to the execution of _DECODE_ mode.

# Example
The repository includes an example **test** directory to demonstrate how the encoding works. The example provided has been tested in Windows 10, but should run in other Operating Systems as well.

Given the environment variables and the **src** directory in **test**, run the application with the following arguments to encode the files into **test\src**:

```
python encoder.py ENCODE test\.test.enc.env
```

. The application can also decode the encoded files by running the following:

```
python encoder.py DECODE test\.test.dec.env
```

. Additional information regarding the environment variables during the test could be found in `test\.test.dec.env` and `test\.test.enc.env`. Each environment variables are explained within this **README.md** file.
