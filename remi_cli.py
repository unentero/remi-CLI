from difflib import SequenceMatcher
import click
# esta parte del codigo se va a encargar de ingresar y procesar el pdf/word de preguntas


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def dbFilepath(filepath):
    db = filepath[0:len(filepath)-4] + "db.txt"
    return db


def agregar_registro(filepath,question,score):
    from pathlib import Path
    from datetime import datetime
    filepath = Path(filepath)
    if filepath.is_file() or filepath.is_dir():
        file = open(filepath,"a")
        file.write("Q." + question + "\n")
        file.write("Score:" + score + "\n")
        file.write("Date:" + datetime.today().strftime('%Y-%m-%d') + "\n")
        file.write("-----------------------------------------------------------------------------\n")
        file.close()
    else:
        filepath.touch(exist_ok=True)
        file = open(filepath,"w")
        file.write("Q." + question + "\n")
        file.write("Score:" + score + "\n")
        file.write("Date:" + datetime.today().strftime('%Y-%m-%d') + "\n")
        file.write("-----------------------------------------------------------------------------")
        file.close()

@click.command()

def test():
    fname = input('Ingresar Archivo: ')
    try:
        fhand = open(fname,'r')
    except:
        click.echo('El archivo no pudo ser encontrado: '+fname)
        exit()
    linelist = []
    for line in fhand:
        linelist.append(line[3:].rstrip())
    questions = [] #aca se almacenan las preguntas y las respuestas
    for i in range(0,len(linelist),2):
        questions.append((linelist[i],linelist[i+1]))
    fhand.close()
    # esta parte del codigo se encarga de revisar las respuestas del usuario
    for question in questions:
        click.echo('Q.' + question[0])
        user_answer = input('A. ')
        if user_answer == '!exit':
            break
        base_answer = question[1]
        alpha = similar(user_answer, base_answer) # aca se determina la similitud de los strings
        score = alpha*100
        click.echo('Similitud:' + str(score))
        agregar_registro(dbFilepath(fname),question[0],str(score))
    

