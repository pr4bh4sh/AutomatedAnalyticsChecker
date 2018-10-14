from subprocess import Popen, PIPE
from collections import namedtuple
import logging

Output = namedtuple('Output', 'result error')


class CommandLine:

    @staticmethod
    def execute(cmd):
        logging.info(cmd)
        # cmd_arr = cmd.split(' ')
        p_ = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        out, err = p_
        print(p_)
        return Output(out.decode('utf-8'), err.decode('utf-8'))
