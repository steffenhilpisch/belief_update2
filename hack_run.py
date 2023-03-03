from otree.cli.base import call_command
from otree.cli import devserver_inner
from otree.cli.prodserver1of2 import run_asgi_server

# devserver_inner.Command().outer_handle(["8000"])
call_command("devserver")
# call_command("timeoutsubprocess", "8000")
# run_asgi_server("localhost", 8000)