import laws


class System:
    def __init__(self, client_law, op1_law, op2_law, op3_law, comp1_law, comp2_law, n, method='delta t', dt=1):
        self.laws = {
            'client': client_law,
            'op1': op1_law,
            'op2': op2_law,
            'op3': op3_law,
            'comp1': comp1_law,
            'comp2': comp2_law,
        }
        self.n = n
        self.method = method
        self.dt = dt

        self.now = 0

        self.generated_count = 0
        self.processed_count = 0
        self.rejected_count = 0

        self.op1_busy = False
        self.op2_busy = False
        self.op3_busy = False
        self.comp1_buffer_len = 0
        self.comp2_buffer_len = 0
        self.comp1_busy = False
        self.comp2_busy = False

    def calculate(self):
        if self.method == 'delta t':
            self.calculate_delta_t()
        else:
            self.calculate_events()

        result = {
            'generated_count': self.generated_count,
            'processed_count': self.processed_count,  # == n
            'rejected_count': self.rejected_count,
        }

        self.now = 0

        self.generated_count = 0
        self.processed_count = 0
        self.rejected_count = 0

        return result

    def new_event(self, last_event, event_type=None):
        event_type = event_type or last_event['type']
        new_event = {
            'time': last_event['time'],
            'type': event_type,
        }
        while new_event['time'] <= self.now:
            new_event['time'] += self.laws[event_type].random()
        return new_event

    def calculate_delta_t(self):
        self.event_list = [
            self.new_event({
                'time': 0,
                'type': 'client'
            })
        ]
        while self.processed_count < self.n:
            self.process_new_dt()

    def process_new_dt(self):
        self.now += self.dt
        for event in self.event_list.copy():
            if event['time'] < self.now:
                self.event_list.remove(event)
                self._process_new_event(event)

    def calculate_events(self):
        self.event_list = [
            self.new_event({
                'time': 0,
                'type': 'client'
            })
        ]
        while self.processed_count < self.n:
            self.process_new_event()

    def process_new_event(self):
        new_event = self.event_list.pop(0)
        self.now = new_event['time']
        self._process_new_event(new_event)

    def _process_new_event(self, new_event):
        if new_event['type'] == 'client':
            self.generated_count += 1
            if not self.op1_busy:
                self.op1_busy = True
                self.event_list.append(
                    self.new_event(new_event, event_type='op1')
                )
            elif not self.op2_busy:
                self.op2_busy = True
                self.event_list.append(
                    self.new_event(new_event, event_type='op2')
                )
            elif not self.op3_busy:
                self.op3_busy = True
                self.event_list.append(
                    self.new_event(new_event, event_type='op3')
                )
            else:
                self.rejected_count += 1
            self.event_list.append(
                self.new_event(new_event)
            )
        elif new_event['type'] == 'op1':
            self.op1_busy = False
            self.comp1_buffer_len += 1
            if not self.comp1_busy:
                self.comp1_busy = True
                self.comp1_buffer_len -= 1
                self.event_list.append(
                    self.new_event(new_event, event_type='comp1')
                )
        elif new_event['type'] == 'op2':
            self.op2_busy = False
            self.comp1_buffer_len += 1
            if not self.comp1_busy:
                self.comp1_busy = True
                self.comp1_buffer_len -= 1
                self.event_list.append(
                    self.new_event(new_event, event_type='comp1')
                )
        elif new_event['type'] == 'op3':
            self.op3_busy = False
            self.comp2_buffer_len += 1
            if not self.comp2_busy:
                self.comp2_busy = True
                self.comp2_buffer_len -= 1
                self.event_list.append(
                    self.new_event(new_event, event_type='comp1')
                )
        elif new_event['type'] == 'comp1':
            self.processed_count += 1
            if self.comp1_buffer_len > 0:
                self.comp1_buffer_len -= 1
                self.event_list.append(
                    self.new_event(new_event)
                )
            else:
                self.comp1_busy = False
        elif new_event['type'] == 'comp2':
            self.processed_count += 1
            if self.comp2_buffer_len > 0:
                self.comp2_buffer_len -= 1
                self.event_list.append(
                    self.new_event(new_event)
                )
            else:
                self.comp2_busy = False
        self.event_list.sort(key=lambda event: event['time'])


if __name__ == '__main__':
    system = System(
        client_law=laws.UniformDistributionLaw(a=8, b=12),
        op1_law=laws.UniformDistributionLaw(a=15, b=25),
        op2_law=laws.UniformDistributionLaw(a=30, b=50),
        op3_law=laws.UniformDistributionLaw(a=20, b=60),
        comp1_law=laws.ConstantDistributionLaw(c=15),
        comp2_law=laws.ConstantDistributionLaw(c=30),
        n=300, dt=1, method='events'
    )
    result = system.calculate()
    print(result)
