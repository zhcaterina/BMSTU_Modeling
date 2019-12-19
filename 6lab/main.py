import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget

from generator import ConstGenerator, UniformGenerator, nr
from modeller import RequestGenerator, RequestProcessor, event_based_modelling


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._ui = uic.loadUi("window.ui", self)

    @property
    def parameters(self):
        u = self._ui
        return {
            'pg0_m': float(u.le_pg0_m.text()),
            'pg1_m': float(u.le_pg1_m.text()),
            'pg0_d': float(u.le_pg0_d.text()),
            'pg1_d': float(u.le_pg1_d.text()),
            'ev0_m': float(u.le_ev0_m.text()),
            'ev1_m': float(u.le_ev1_m.text()),
            'ev2_m': float(u.le_ev2_m.text()),
            'ev0_d': float(u.le_ev0_d.text()),
            'ev1_d': float(u.le_ev1_d.text()),
            'ev2_d': float(u.le_ev2_d.text()),
            'cid0_m': float(u.le_cid0_m.text()),
            'cid1_m': float(u.le_cid1_m.text()),
            'cid2_m': float(u.le_cid2_m.text()),
            'cid3_m': float(u.le_cid3_m.text()),
            'cid0_d': float(u.le_cid0_d.text()),
            'cid1_d': float(u.le_cid1_d.text()),
            'cid2_d': float(u.le_cid2_d.text()),
            'cid3_d': float(u.le_cid3_d.text()),
            'pcd0_m': float(u.le_pcd0_m.text()),
            'pcd1_m': float(u.le_pcd1_m.text()),
            'pcd0_d': float(u.le_pcd0_d.text()),
            'pcd1_d': float(u.le_pcd1_d.text()),
            'cc0_m': float(u.le_cc0_m.text()),
            'cc0_d': float(u.le_cc0_d.text()),
            'c_count': 100
        }

    @pyqtSlot()
    def on_pushButton_clicked(self):
        procfmt = '{0:13}|{1:5}|{2:5}|{3:5}'
        print(procfmt.format('name', 'reqs', 'drop', 'queue'))
        devices = self.start_modelling(**self.parameters)
        for dev in devices:
            if type(dev) is RequestGenerator:
                print(procfmt.format(dev.name, dev.requests, dev.dropped_requests, ''))
            else:
                print(procfmt.format(dev.name, dev.requests,
                                     dev.dropped_requests, dev.queue_size))
        print('-' * len(procfmt.format('', '', '', '')))
        print(procfmt.format('',
                             sum(dev.requests for dev in devices),
                             sum(dev.dropped_requests for dev in devices),
                             ''))
        u = self._ui
        u.le_ev0_wt.setText('{:.2f}'.format(devices[2].max_waiting_time))
        u.le_ev1_wt.setText('{:.2f}'.format(devices[3].max_waiting_time))
        u.le_ev2_wt.setText('{:.2f}'.format(devices[4].max_waiting_time))
        u.le_cid0_wt.setText('{:.2f}'.format(devices[5].max_waiting_time))
        u.le_cid1_wt.setText('{:.2f}'.format(devices[6].max_waiting_time))
        u.le_cid2_wt.setText('{:.2f}'.format(devices[7].max_waiting_time))
        u.le_cid3_wt.setText('{:.2f}'.format(devices[8].max_waiting_time))
        u.le_pcd0_wt.setText('{:.2f}'.format(devices[9].max_waiting_time))
        u.le_pcd1_wt.setText('{:.2f}'.format(devices[10].max_waiting_time))
        u.le_cc0_wt.setText('{:.2f}'.format(devices[11].max_waiting_time))

    def start_modelling(self, pg0_m, pg1_m, pg0_d, pg1_d,
                        ev0_m, ev1_m, ev2_m, ev0_d, ev1_d, ev2_d,
                        cid0_m, cid1_m, cid2_m, cid3_m, cid0_d, cid1_d, cid2_d, cid3_d,
                        pcd0_m, pcd1_m, pcd0_d, pcd1_d,
                        cc0_m, cc0_d,
                        c_count):
        random = nr.RandomState()
        client_generator0 = RequestGenerator(UniformGenerator(pg0_m, pg0_d, random),
                                                'client0')
        client_generator1 = RequestGenerator(UniformGenerator(pg1_m, pg1_d, random),
                                                'client1')
        clients = (client_generator0, client_generator1)

        check_exist0 = RequestProcessor(UniformGenerator(ev0_m, ev0_d, random),
                                               'check0')
        check_exist1 = RequestProcessor(UniformGenerator(ev1_m, ev1_d, random),
                                               'check1')
        check_exist2 = RequestProcessor(UniformGenerator(ev2_m, ev2_d, random),
                                               'check2')
        check_records = (check_exist0, check_exist1, check_exist2)

        master_working0 = RequestProcessor(UniformGenerator(cid0_m, cid0_d, random),
                                         'master0')
        master_working1 = RequestProcessor(UniformGenerator(cid1_m, cid1_d, random),
                                         'master1')
        master_working2 = RequestProcessor(UniformGenerator(cid2_m, cid2_d, random),
                                         'master2')
        master_working3 = RequestProcessor(UniformGenerator(cid3_m, cid3_d, random),
                                         'master3')
        work = (master_working0, master_working1, master_working2, master_working3)

        payment_for_services0 = RequestProcessor(UniformGenerator(pcd0_m, pcd0_d, random),
                                                  'cashbox0', can_drop=True)
        payment_for_services1 = RequestProcessor(UniformGenerator(pcd1_m, pcd1_d, random),
                                                  'cashbox1', can_drop=True)
        cashbox = (payment_for_services0, payment_for_services1)

        commenting0 = RequestProcessor(UniformGenerator(cc0_m, cc0_d, random),
                                            'comment0', can_drop=True)
        do_comment = (commenting0,)

        leave = RequestProcessor(ConstGenerator(0), 'leave', is_exit=True)

        for p in clients: p.add_receivers(check_records)
        for e in check_records: e.add_receivers(work)
        for c in work: c.add_receivers(cashbox)
        for p in cashbox: p.add_receivers(do_comment)
        for cc in do_comment: cc.add_receiver(leave)

        devices = clients + check_records + work + cashbox + do_comment + (leave,)
        event_based_modelling(devices, lambda: leave.processed_requests == c_count)
        return devices


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
