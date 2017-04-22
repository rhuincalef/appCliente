#!/usr/bin/python
import subprocess
import threading

class RunMyCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd 
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def run_the_process(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()   #if your process needs a kill -9 to make 
                                 #it go away, use self.p.kill() here instead.

            self.join()

#RunMyCmd(["sleep", "20"], 3).run_the_process()
RunMyCmd(["sleep", "8"], 10).run_the_process()