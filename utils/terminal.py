import os

cls = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
