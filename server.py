from app import create_app, shell_plus_command

app = create_app()
app.cli.add_command(shell_plus_command)

@app.route('/ping')
def ping():
    return 'pong'