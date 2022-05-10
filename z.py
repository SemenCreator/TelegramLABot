from schedule import every, repeat, run_pending
import datetime
import time

period = datetime.datetime.today()
period += datetime.timedelta(minutes=1)
period = period.strftime('%H:%M')


@repeat(every().day.at(period))
def job_that_executes_once():
    # Выполните некоторую работу, которая должна выполняться только один раз...
    print('sfjdujfds')


while True:
    run_pending()
    time.sleep(1)
