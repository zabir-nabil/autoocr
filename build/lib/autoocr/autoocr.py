import os
import subprocess
import sys
import json
from sys import platform
from colorama import Fore, Style
import shutil
from pkg_resources import resource_filename


class AutoOCR:
    def __init__(self, lang='english'):
        config_path = resource_filename(__name__, "config.json")
        lang_map_path = resource_filename(__name__, "lang_map.json")
        init_token_path = resource_filename(__name__, "init.token")

        # load config.json file
        with open(config_path) as f:
            config = json.load(f)
        # load language url mapper
        with open(lang_map_path) as f:
            lang_map = json.load(f)

        

      
        # check if the library is running for the first time from token
        if os.path.isfile(init_token_path):
            pass
        else:
            # WARNINGS, ERRORS in color
            subprocess.call([sys.executable,"-m","pip","install","colorama"])
            print('Installing backend dependency.')


            try:
                if platform == "linux" or platform == "linux2":
                    print("After installing tesseract, copy the tessdata folder path to config.json or run set_datapath function")
                    pass
                    #print('linux system')
                elif platform == "darwin":
                    try:
                        subprocess.call(["brew", "list", "tesseract"])
                        print(f'{Fore.RED}')
                        print("Copy the tessdata folder path to config.json")
                        print(f'{Style.RESET_ALL}')
                    except:
                        print('tesseract not installed, installing now ...')
                        subprocess.call(["brew", "install", "tesseract"])
                        subprocess.call(["brew", "list", "tesseract"])
                        print(f'{Fore.RED}')
                        print("Copy the tessdata folder path to config.json by calling set_datapath function")
                        print(f'{Style.RESET_ALL}')

                    #print('mac system')
                    #subprocess.call(["brew", "install", "tesseract"])
                elif platform == "win32":
                    print("After installing tesseract, copy the tessdata folder path to config.json or run set_datapath function")
                    pass
                    #print('win system')
            except:
                print(f'{Fore.YELLOW}')
                print('OS recognition failed')
                print(f'{Style.RESET_ALL}')
                
            # install tesseract engine support, will replace later
            subprocess.call([sys.executable,"-m","pip","install","pytesseract"])

            # dump the token file
            with open(init_token_path, "w") as f:
                f.write("installation done")
        
        # support for other languages

        if lang not in config['support_lang']:
            if config['tessdata_path'] == '':
                print(f'{Fore.RED}')
                print('tessdata path is not assigned to config.json file.')
                print('Use set_datapath function to set the tessdata path')
                print(f'{Style.RESET_ALL}')
            elif os.path.isdir(config['tessdata_path']): # additional checks may be needed
                if lang in lang_map:
                    # download the weight
                    
                    download_url = lang_map[lang]
                    model_name = lang + '.traineddata'
                    if os.path.isfile(model_name):
                        print('weight file already downloaded')
                    else:
                        print(f'{Fore.GREEN}')
                        print('downloading language model ...')
                        subprocess.call(['wget', '-c', download_url, '-O', model_name])
                        print(f'{Style.RESET_ALL}')
                    dest_path = config['tessdata_path']
                    try:
                        shutil.move(model_name, dest_path)
                    except:
                        print(f'{Fore.RED}')
                        print('Path access error for tessdata ... ')
                        print(f'{Style.RESET_ALL}')

                    config['support_lang'].append(lang)

                    with open(config_path, 'w') as f:
                        json.dump(config, f)


                else:
                    print(f'{Fore.RED}')
                    print("%s: Language code not correct."%lang)
                    print(f'{Style.RESET_ALL}')

        self.lang = lang

    def set_datapath(self, path):
        config_path = resource_filename(__name__, "config.json")
        # load config.json file
        with open(config_path) as f:
            config = json.load(f)
        config['tessdata_path'] = path
        with open(config_path, 'w') as f:
            json.dump(config, f)

        print('tessdata path set to %s'%path)



    def get_text(self, path):
        try:
            from PIL import Image
        except ImportError:
            import Image
        import pytesseract

        return (pytesseract.image_to_string(Image.open(path), lang = self.lang))



