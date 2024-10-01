import os, base64, random, jwt, copy, re, datetime, uuid

def __jwt_encode__(data, secret, iss, aud, algo="HS256", meta={}):
    payload = {}
    payload['data'] = data
    payload['iss'] = iss
    payload['aud'] = aud
    for item in meta.items():
        if item[0] not in ['iss', 'aud', 'data']:
            payload[item[0]] = item[1]
    return jwt.encode(payload, secret, algorithm=algo)

def __jwt_decode__(msg, secret, iss, auds, leeway=0, algos=["HS256"], requireds=[], options={}):
    custom_opts = copy.deepcopy(options)
    custom_opts['require'] = ['iss', 'aud'] + requireds
    return jwt.decode(msg, secret, issuer=iss, audience=auds, leeway=leeway, algorithms=algos, options=custom_opts)

def __encode_str__(line, secret, iss, aud):
    # ===
    mystrbytes = line.encode('ascii')
    mybytes = base64.b64encode(mystrbytes)
    mystr = mybytes.decode('ascii')
    # ===
    mystrbytes = mystr.encode('ascii')
    mybytes = base64.b64encode(mystrbytes)
    mystr = mybytes.decode('ascii')

    mystr = __jwt_encode__(mystr, secret, iss, aud)

    mystrbytes = mystr.encode('ascii')
    mybytes = base64.b64encode(mystrbytes)
    mystr = mybytes.decode('ascii')

    return mystr

def __decode_str__(line, secret, iss, aud):
    b64bytes = line.encode('ascii')
    strbytes = base64.b64decode(b64bytes)
    decStr = strbytes.decode('ascii')

    decStr = __jwt_decode__(decStr, secret, iss, aud)
    decStr = decStr['data']

    b64bytes = decStr.encode('ascii')
    strbytes = base64.b64decode(b64bytes)
    decStr = strbytes.decode('ascii')
    # ===
    b64bytes = decStr.encode('ascii')
    strbytes = base64.b64decode(b64bytes)
    decStr = strbytes.decode('ascii')

    return decStr

def __to_abs__(path):
    abs_path = path + ''
    if not os.path.isabs(abs_path):
        abs_path = os.path.abspath(path)
    return os.path.normpath(abs_path)

def __calc_c__(c, mode, oprnd):
    temp_c = ord(c)
    if mode == 'ADD':
        temp_c += oprnd
        if temp_c > 126:
            temp_c = (temp_c - 126) + 32
    elif mode == 'SUB':
        temp_c -= oprnd
        if temp_c < 33:
            temp_c = 127 - (33 - temp_c)
    else:
        raise NotImplementedError
    return chr(temp_c)


class Encoder():

    def __init__(self, dir, output_dir, output_file_prefix, file_dividers, excemptions, backslashes, secrets, iss, aud, max_in_one_file):
        self.__to_check_dir = __to_abs__(dir)
        self.__output_dir = __to_abs__(output_dir) if output_dir else 'enc_out'
        self.__output_file_prefix = output_file_prefix if output_file_prefix else 'out'
        self.__excempted_list = excemptions
        self.__backslashes = backslashes
        self.__secrets = secrets
        self.__iss = iss
        self.__aud = aud
        self.__max_in_one_file = int(max_in_one_file)
        self.__file_dividers = file_dividers if file_dividers else ['======']
        self.__seeds = []
        print('CONFIGS:')
        print('Input Directory:', self.__to_check_dir)
        print('Output Directory:', self.__output_dir)
        print('Output File Prefix:', self.__output_file_prefix)
        print('Excempted Files:', self.__excempted_list)
        print('Backslashes:', self.__backslashes)
        print('Secrets:', self.__secrets)
        print('JWT ISS:', self.__iss)
        print('JWT AUD', self.__aud)
        print('Max number of files in an output file:', self.__max_in_one_file)
        print('File Dividers:', self.__file_dividers)
        print('\n\n')

    def file_reset(self):
        self.__seed = int( datetime.datetime.now().strftime("%M%d%H%j%m%S%f%y%W") )
        random.seed(self.__seed)
        myrand = random.randint(1,999)
        self.__seed *= myrand
        if self.__seed % 10 == 0:
            self.__seed -= 1
        self.__seeds.append(str(self.__seed))

        temp_seed = []
        for c in self.__seeds[len(self.__seeds) - 1]:
            temp_seed.append(int(c))
        
        self.__seed = temp_seed
        self.__counter = 0
        self.__offset_mode = sum(self.__seed) % 2

    def offset(self, c):
        seed = self.__seed[self.__counter]
        if self.__offset_mode == 0:
            new_c = __calc_c__(c, 'ADD' if (self.__counter % 2) == 0 else 'SUB', seed)
        else:
            new_c = __calc_c__(c, 'SUB' if (self.__counter % 2) == 0 else 'ADD', seed)
        self.update_counter()
        return new_c

    def update_counter(self):
        self.__counter = self.__counter + 1
        if self.__counter == len(self.__seed):
            self.__counter = 0

    def dump_keys(self):
        file_str = str(uuid.uuid4()) + '.keys'
        keys = base64.b64encode((",".join(self.__seeds)).encode('ascii')).decode('ascii')
        print('\nKEYS:', keys)
        with open(os.path.join(self.__output_dir, file_str), 'w') as output:
            output.write(keys)

    def start(self):
        to_parse = []
        for root, dirs, files in os.walk(self.__to_check_dir):
            for f in files:
                to_cont = False
                full_path = os.path.normpath(os.path.join(root, f))
                temp_file = os.path.relpath(full_path, self.__to_check_dir)
                for excemption in self.__excempted_list:
                    if excemption in temp_file:
                        to_cont = True
                if to_cont:
                    continue
                to_parse.append(temp_file)
        print("\nFiles to parse:", to_parse)

        out_file_cnt = 1
        curr_out_file_cnt = 0
        max_in_one_file = random.randint(1, self.__max_in_one_file)
        self.file_reset()
        file_str = ""
        print('\nDIRECTORIES TO ENCODE:')
        for file in to_parse:
            file_abs = os.path.join(self.__to_check_dir, file)
            f_const = self.__file_dividers[random.randint(0, len(self.__file_dividers) - 1)] + ""
            print('-', file_abs)
            with open(file_abs, 'r') as iter_to_parse:
                lines = iter_to_parse.readlines()
                if max_in_one_file == curr_out_file_cnt:
                    # output files
                    with open(f"{self.__output_dir}/{self.__output_file_prefix}{out_file_cnt}", "w") as output:
                        output.write(file_str)
                    out_file_cnt = out_file_cnt + 1
                    curr_out_file_cnt = 0
                    self.file_reset()
                    file_str = ""
                    max_in_one_file = random.randint(1, self.__max_in_one_file)
                temp_file_str = __encode_str__(
                    file, self.__secrets[int(curr_out_file_cnt % len(self.__secrets))],
                    self.__iss, self.__aud
                )
                temp_file_str = "".join([self.offset(c) for c in temp_file_str])
                file_str = file_str + ("\n" if file_str else "") + f_const + temp_file_str + f_const + "\n"

                count = 0
                # Strips the newline character
                if len(lines) == 0:
                    mystr = self.__backslashes[random.randint(0, len(self.__backslashes) - 1)]
                    file_str = file_str + mystr
                else:
                    for line in lines:
                        secret = self.__secrets[int(count % len(self.__secrets))]

                        if line.strip() == '':
                            line = line.replace('\n', '')
                        else:
                            line = line.rstrip()
                        
                        if line == '':
                            mystr = (self.__backslashes + ['\n'])[random.randint(0, len(self.__backslashes))]
                            file_str = file_str + mystr
                        else:
                            mystr = __encode_str__(line, secret, self.__iss, self.__aud)
                            mystr = "".join([self.offset(c) for c in mystr])
                            file_str = file_str + mystr + (self.__backslashes + ['\n'])[random.randint(0, len(self.__backslashes))]
                        
                        count = count + 1
                curr_out_file_cnt = curr_out_file_cnt + 1
        # output files
        with open(f"{self.__output_dir}/{self.__output_file_prefix}{out_file_cnt}", "w") as output:
            output.write(file_str)
        print('\nENCODING DONE!!!')
        self.dump_keys()


class Decoder():

    def __init__(self, dir, output_dir, enc_file_prefix, file_dividers, backslashes, secrets, iss, aud, key_dir):
        self.__to_check_dir = __to_abs__(dir)
        self.__output_dir = __to_abs__(output_dir) if output_dir else 'dec_out'
        self.__file_prefix = enc_file_prefix if enc_file_prefix else 'out'
        # self.__excempted_list = excemptions
        self.__backslashes = backslashes
        self.__backslash_regex = "|".join([re.escape(b) for b in self.__backslashes])
        self.__secrets = secrets
        self.__iss = iss
        self.__aud = aud
        self.__file_dividers = file_dividers if file_dividers else ['======']
        self.__file_counter = 0
        self.__keys = self.__read_keys__(key_dir)
        print('CONFIGS:')
        print('Input Directory:', self.__to_check_dir)
        print('Output Directory:', self.__output_dir)
        # print('Excempted Files:', self.__excempted_list)
        print('Backslashes:', self.__backslashes)
        print('Backslash Regex:', self.__backslash_regex)
        print('Secrets:', self.__secrets)
        print('JWT ISS:', self.__iss)
        print('JWT AUD', self.__aud)
        print('File Dividers:', self.__file_dividers)
        print('\n\n')

    def __read_keys__(self, key_dir):
        key_dir = os.path.normpath(key_dir)
        if not os.path.isabs(key_dir):
            key_dir = os.path.join(self.__to_check_dir, key_dir)
        with open(key_dir, 'r') as iter_to_parse:
            keys = (iter_to_parse.readlines())[0]
        keys = keys.encode('ascii')
        keys = base64.b64decode(keys)
        keys = keys.decode('ascii')
        return keys.split(',')

    def file_reset(self):
        self.__seed = str(self.__keys[self.__file_counter])

        temp_seed = []
        for x in self.__seed:
            temp_seed.append(int(x))
        
        self.__seed = temp_seed
        self.__counter = 0
        self.__offset_mode = sum(temp_seed) % 2
        self.__file_counter += 1

    def offset(self, c):
        seed = self.__seed[self.__counter]
        if self.__offset_mode == 1:
            new_c = __calc_c__(c, 'ADD' if (self.__counter % 2) == 0 else 'SUB', seed)
        else:
            new_c = __calc_c__(c, 'SUB' if (self.__counter % 2) == 0 else 'ADD', seed)
        self.update_counter()
        return new_c

    def update_counter(self):
        self.__counter = self.__counter + 1
        if self.__counter == len(self.__seed):
            self.__counter = 0
    
    def start(self):
        to_parse = []
        for root, dirs, files in os.walk(self.__to_check_dir):
            for f in files:
                # to_cont = False
                full_path = os.path.normpath(os.path.join(root, f))
                temp_file = os.path.relpath(full_path, self.__to_check_dir)
                # for excemption in self.__excempted_list:
                #     if excemption in temp_file:
                #         to_cont = True
                # if to_cont:
                #     continue
                if os.path.isfile(full_path) and os.path.basename(full_path).startswith(self.__file_prefix):
                    to_parse.append({"temp_file": temp_file, "order": int(os.path.basename(full_path).replace(self.__file_prefix, ""))})
        to_parse.sort(key=lambda x: x['order'])
        to_parse = [x['temp_file'] for x in to_parse]
        print("\nFiles to parse:", to_parse)

        count = 0
        running_fname = None
        running_fcontent = None
        print('\nDIRECTORIES TO DECODE:')
        for file in to_parse:
            self.file_reset()
            curr_out_file_cnt = 0
            file_abs = os.path.join(self.__to_check_dir, file)
            print('-', file_abs)
            with open(file_abs, 'r') as iter_to_parse:
                lines = iter_to_parse.readlines()
                for line in lines:
                    div_idx = -1
                    for idx, f_const in enumerate(self.__file_dividers):
                        if line.strip().startswith(f_const) and line.strip().endswith(f_const):
                            div_idx = idx
                            break
                    if div_idx > -1:
                        line = line.strip().replace(f_const, "")
                        line = "".join([self.offset(c) for c in line])
                        line = __decode_str__(line, self.__secrets[int(curr_out_file_cnt % len(self.__secrets))], self.__iss, self.__aud)
                        if running_fname is not None and running_fcontent is not None:
                            running_fcontent = running_fcontent.strip() + '\n'
                            dirs = running_fname.split(os.path.sep)
                            if len(dirs) > 1:
                                dirs.pop()
                                dirs = os.path.join(self.__output_dir, *dirs)
                                os.makedirs(dirs, exist_ok=True)
                            with open(os.path.join(self.__output_dir, running_fname), 'w') as output:
                                output.write(running_fcontent)
                        running_fname = line + ''
                        running_fcontent = ''
                        curr_out_file_cnt = curr_out_file_cnt + 1
                        count = 0
                    else:
                        line = line.strip()
                        # replace backslashes with \n
                        line_exp = re.split(self.__backslash_regex, line) if len(self.__backslashes) > 0 else [line + '']
                        for line_exp_entry in line_exp:
                            if line_exp_entry == '':
                                dec_line_exp_entry = ''
                            else:
                                dec_line_exp_entry = "".join([self.offset(c) for c in list(line_exp_entry)])
                                dec_line_exp_entry = __decode_str__(
                                    dec_line_exp_entry, self.__secrets[int(count % len(self.__secrets))], self.__iss, self.__aud
                                )
                            running_fcontent = running_fcontent + dec_line_exp_entry + '\n'
                            count = count + 1
                running_fcontent = running_fcontent.strip() + '\n'
                dirs = running_fname.split(os.path.sep)
                if len(dirs) > 1:
                    dirs.pop()
                    dirs = os.path.join(self.__output_dir, *dirs)
                    os.makedirs(dirs, exist_ok=True)
                with open(os.path.join(self.__output_dir, running_fname), 'w') as output:
                    output.write(running_fcontent)
        print('\nDECODING DONE!!!')
