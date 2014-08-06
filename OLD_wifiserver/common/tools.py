#!/usr/bin/env python


def get_ap_list(self):
    wc = common.WiFiClient()
    self.ap_list = wc.list_networks()
