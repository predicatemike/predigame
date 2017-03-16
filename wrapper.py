import sys, os, predigame

def err():
    print('Error: Invalid Python file provided')
    sys.exit()

run_path = sys.argv[1:][0]
if not os.path.isfile(run_path):
    err()
run_path = run_path[:-3]

predigame.init()

try:
    script = __import__(run_path)
except:
    err()

while True:
    predigame.main_loop()
