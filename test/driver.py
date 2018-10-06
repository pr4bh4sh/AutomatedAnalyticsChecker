from selenium import webdriver as wd
from command_line import CommandLine


class Driver:
    driver = None
    mitm_proc = None

    def get_driver(self):
        PROXY = "0.0.0.0:8080"  # IP:PORT or HOST:PORT
        # self.__ensure_no_mitmdump()
        # self.__start_mitm()
        chrome_options = wd.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = wd.Chrome(chrome_options=chrome_options)
        self.driver.get("https://www.delta.com/")
        import ipdb
        ipdb.set_trace(context=5)

    def quite_driver(self):
        self.__ensure_no_mitmdump()
        self.driver.quit()


    def __start_mitm(self):
        import ipdb
        ipdb.set_trace(context=5)
        self.mitm_proc = CommandLine.execute('mitmdump -p 8090 -s test/analytics_logger.py collect &')
        import ipdb
        ipdb.set_trace(context=5)

    def __ensure_no_mitmdump(self):
        CommandLine.execute('killall mitmdump')
