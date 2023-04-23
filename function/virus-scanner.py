import os
import sys
import subprocess
import uuid
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    operation = None
    filename = None

    try:
        operation = event['operation']
        filename = event['filename']

        if operation == 'scan':
            scan_cmd = 'clamscan -v ' + filename
            sp = subprocess.Popen(scan_cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)

            out, err = sp.communicate()
            # * clamscan return values (documented from man clamscan)
            # *  0 : No virus found.
            # *  1 : Virus(es) found.
            # * 40: Unknown option passed.
            # * 50: Database initialization error.
            # * 52: Not supported file type.
            # * 53: Can't open directory.
            # * 54: Can't open file. (ofm)
            # * 55: Error reading file. (ofm)
            # * 56: Can't stat input file / directory.
            # * 57: Can't get absolute path name of current working directory.
            # * 58: I/O error, please check your file system.
            # * 62: Can't initialize logger.
            # * 63: Can't create temporary files/directories (check permissions).
            # * 64: Can't write to temporary directory (please specify another one).
            # * 70: Can't allocate memory (calloc).
            # * 71: Can't allocate memory (malloc).

            return_code = sp.wait()
            print(out)
            return {
                'result' : return_code
            }
        
        elif operation == 'update':
            #Create the database directory
            mkdir_cmd = 'mkdir -p /mnt/dmzefs/clamav'
            sp = subprocess.Popen(mkdir_cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)

            out, err = sp.communicate()
            return_code = sp.wait()
            print(out)

            #chmod the database directory
            chmod_cmd = 'chmod 777 /mnt/dmzefs/clamav'
            sp = subprocess.Popen(chmod_cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)

            out, err = sp.communicate()
            return_code = sp.wait()
            print(out)

            #Update db
            update_cmd = 'freshclam'
            sp = subprocess.Popen(update_cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)

            out, err = sp.communicate()
            return_code = sp.wait()
            print(out)
            return {
                'result' : return_code
            }
    except:
        print(f"Unknown error occured while scanning {filename} for viruses.")