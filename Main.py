import os
import re
import sys
import platform
import hashlib
import pymem
import subprocess
from time import sleep

process_name = "dota2.exe"

pattern_plus = rb"\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x53\x00\x00\x00\x00\x00\x00\x00\x13"


class Main:
    def __init__(self) -> None:
        process = self.process_checker()
        if process:
            os.system('cls')
            print(f"Process {process_name} finded.")

            sleep(15)

            print("Search address")

            plus_addres = Memory().get_sig("client.dll", pattern_plus)
            if plus_addres:
                print("Address finded")
                dota_plus = Memory().dota_plus(plus_addres)
                if dota_plus:
                    os.system('cls')
                    print("Partial Dota+ Activated!")

                    sleep(5)
                else:
                    os.system('cls')
                    print(dota_plus)

    def process_checker(self):
        while True:
            progs = str(subprocess.check_output('tasklist'))
            if process_name in progs:
                return True
            else:
                os.system('cls')
                print(f"Waiting for the process {process_name}.")


class Memory:
    def __init__(self) -> None:
        self.process = pymem.Pymem(process_name)

    def get_sig(self, module, pattern):
        module = pymem.process.module_from_name(self.process.process_handle, module)
        bytes = self.process.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
        match = re.search(pattern, bytes).start()
        addres = module.lpBaseOfDll + match
        return addres

    def dota_plus(self, addres):
        try:
            self.process.write_int(addres, 1)
            return True
        except Exception as error:
            return error


if __name__ == "__main__":
    Main()
