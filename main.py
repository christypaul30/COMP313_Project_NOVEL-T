from website import create_app
# File launches the program (Should not be touched.)

app = create_app()

if __name__ == '__main__':
    #debug means any changes to website will cause it to restart
    app.run(debug=True)
