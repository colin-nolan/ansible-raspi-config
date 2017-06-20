BOOT_CONFIG_PATH = "/boot/config.txt"

RASPI_CONFIG_BIN = "/usr/bin/raspi-config"


class ConfigFile:

    @staticmethod
    def __param_string(param, value):
        return param + "=" + value

    def __init__(self, file_name=BOOT_CONFIG_PATH):
        self.is_changed = False
        self.file_name = file_name

        with open(self.file_name) as fp:
            self.lines = fp.readlines()

    def __find_starting_with(self, searched):
        try:
            return [x.find(self.__param_string(searched, "")) == 0 for x in self.lines].index(True)
        except ValueError:
            return -1

    def set(self, param, value):
        # search for an uncommented line, and a commented one if that fails
        line_num = self.__find_starting_with(param)
        if line_num == -1:
            line_num = self.__find_starting_with('#'+param)

        # ...and finally just create an empty line
        if line_num == -1:
            self.lines.append("")

        target_value = self.__param_string(param, value)+"\n"
        if self.lines[line_num] != target_value:
            self.lines[line_num] = target_value
            self.is_changed = True
            with open(self.file_name, 'w') as fp:
                fp.writelines(self.lines)
            return True
        else:
            return False
