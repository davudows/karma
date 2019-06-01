#!/usr/bin/env python3

import logging
import sys
import re
import os

try:
    from karma import formatter
    import requests
except Exception as e:
    raise e


def get_logger():

    global logger
    logger = logging.getLogger("Karma")


class pwndb(object):

    """Docstring for pwndb. """

    def __init__(self, args):

        get_logger()
        self.site = "http://pwndb2am4tzkvold.onion/"
        self.args = args
        self.data = {"luseropr": 1, "domainopr": 1, "submitform": "em"}

        proxy = self.args["--proxy"]
        if "//" in proxy:
            proxy = proxy.split("//")[1]

        self.session = requests.session()
        self.session.proxies = {
            "http": "socks5h://%s" % proxy,
            "https": "socks5h://%s" % proxy,
        }

    def get_request(self, data):
        """ Get requests """

        try:
            req = self.session.post(self.site, data=data, timeout=(15, None))

        except requests.exceptions.ConnectTimeout as error:
            logger.error(error)
            logger.info("the site: {} is down, try again later".format(self.site))
            sys.exit(1)

        except requests.exceptions.ConnectionError as error:
            logger.error(error)
            logger.info("please restart the tor service and try again")
            sys.exit(1)

        except Exception as e:
            raise e

        return req.text

    def response_parser(self, response):
        """ Parse pwndb response """

        if not response:
            logger.warn("no results were obtained")
            sys.exit(1)

        logger.info("analyzing results:")
        resp = re.findall(r"\[(.*)", response)
        resp = [resp[n : n + 4] for n in range(0, len(resp), 4)]

        results = {}
        getinfo = lambda s: s.split("=>")[1].strip()
        for item in resp:
            results[getinfo(item[0])] = {
                "email": "{}@{}".format(getinfo(item[1]), getinfo(item[2])),
                "passw": getinfo(item[3]),
            }

        return results

    def email_request(self, target, num_targets=1, i=1):
        """ Request with email """

        regex = r"(^[a-zA-Z0-9_.+%-]+@[a-zA-Z0-9-%]+\.[a-zA-Z0-9-%.]+$)"
        if re.match(regex, target):
            logger.info("{}/{} request email: {}".format(i, num_targets, target))
            self.data["luser"] = target.split("@")[0]
            self.data["domain"] = target.split("@")[1]
            return self.get_request(self.data)

        else:
            logger.warn("invalid email: {}".format(target))
            return ""

    def search_localpart(self, target, num_targets=1, i=1):
        """ Request with localpart """

        regex = r"(^[a-zA-Z0-9_.+%-]+$)"
        if re.match(regex, target):
            logger.info("{}/{} request local-part: {}".format(i, num_targets, target))
            self.data["luseropr"] = 1
            self.data["luser"] = target
            return self.get_request(self.data)

        else:
            logger.warn("invalid local-part: {}".format(target))
            return ""

    def search_domain(self, target, num_targets=1, i=1):
        """ Requests with domain """

        regex = r"(^[a-zA-Z0-9-%]+\.[a-zA-Z0-9-.%]+$)"
        if re.match(regex, target):
            logger.info("{}/{} request domain: {}".format(i, num_targets, target))
            self.data["domainopr"] = 1
            self.data["domain"] = target
            return self.get_request(self.data)

        else:
            logger.warn("invalid domain: {}".format(target))
            return ""

    def search_password(self, target, num_targets=1, i=1):
        """ Requests with password """

        logger.info("{}/{} request password: {}".format(i, num_targets, target))
        self.data["submitform"] = "pw"
        self.data["password"] = target
        return self.get_request(self.data)

    def choose_function(self, target, num_targets=1, i=1):
        """
        Choose the corresponding function 
        according to the parameter
        """

        opts = {
            "--local-part": self.search_localpart,
            "--password": self.search_password,
            "--domain": self.search_domain,
        }

        for key, value in self.args.items():
            if value and key in opts:
                return opts[key](target, num_targets, i)

    def search_info(self):
        """Start the information search"""

        opt_search = self.args["search"]
        opt_target = self.args["target"]
        target = self.args["<target>"]

        response = ""
        if os.path.exists(target):

            targets = open(target, "r").readlines()
            num_targets = len(targets)

            for i, target in enumerate(targets, 1):
                target = target.strip("\n")
                try:
                    if opt_search:
                        response += self.choose_function(target, num_targets, i)

                    if opt_target:
                        response += self.email_request(target, num_targets, i)

                except KeyboardInterrupt:
                    logger.warn("search has stopped")
                    break

        elif opt_search:
            response = self.choose_function(target)

        elif opt_target and target:
            response = self.email_request(target)

        return self.response_parser(response)
