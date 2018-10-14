from selenium import webdriver as wd
from command_line import CommandLine


class Driver:
    driver = None
    mitm_proc = None #Not needed as of now
    port = 8090
    server = "0.0.0.0"

    def get_driver(self):
        PROXY = f"{self.server}:{self.port}"  # IP:PORT or HOST:PORT
        self.__ensure_no_mitmdump()
        self.__start_mitm()
        chrome_options = wd.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = wd.Chrome(chrome_options=chrome_options)
        self.driver.get("http://magazine.trivago.com")
        self.quite_driver()

    def quite_driver(self):
        self.__ensure_no_mitmdump()
        self.driver.quit()


    def __start_mitm(self):
        # import ipdb
        # ipdb.set_trace(context=5)
        self.mitm_proc = CommandLine.execute(f'mitmdump -p {self.port} -s test/analytics_logger.py > /dev/null 2>&1 &')
        # import ipdb
        # ipdb.set_trace(context=5)

    def __ensure_no_mitmdump(self):
        CommandLine.execute(f'kill -9 $(lsof -t -i :{self.port}) > /dev/null 2>&1')
