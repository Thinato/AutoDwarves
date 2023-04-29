from consoledraw import Console
from datetime import datetime

console = Console()

format = """
    ╔══════════╗
    ║ {} ║
    ╚══════════╝
"""

while True:
    with console:
        console.print(format.format(datetime.strftime(datetime.now(), "%H:%M:%S")))
