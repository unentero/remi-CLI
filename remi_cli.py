from difflib import SequenceMatcher
import click
from pathlib import Path
from datetime import datetime

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def dbFilepath(filepath):
    db = filepath[0:len(filepath)-4] + "db.txt"
    return db

def agregar_registro(filepath,question,score):
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

def test_file(filename):
    try:
        fhand = open(filename,'r')
    except:
        click.secho('El archivo no pudo ser encontrado: '+filename, bg='red')
        exit()
    linelist = []
    for line in fhand:
        linelist.append(line.rstrip())
    questions = [] #aca se almacenan las preguntas y las respuestas
    for i in range(0,len(linelist),2):
        questions.append((linelist[i],linelist[i+1]))
    fhand.close()
    # esta parte del codigo se encarga de revisar las respuestas del usuario
    click.secho('When prompted the question, input the answer and Remi will calculate the similarity to the original answer or type "!exit" to exit the program',bg='red')
    click.secho('The scores of your answers will be stored in: ' + dbFilepath(filename),bg='red')
    for question in questions:
        click.secho('Q.' + question[0],fg='yellow')
        user_answer = input('A.')
        if user_answer == '!exit':
            break
        base_answer = question[1]
        alpha = similar(user_answer, base_answer) # aca se determina la similitud de los strings
        score = round(alpha,2)*100
        click.secho('Similitud:' + str(score),bg='green')
        agregar_registro(dbFilepath(filename),question[0],str(score))

def review_file(filename):
    try:
        fhand = open(filename,'r')
    except:
        click.echo('El archivo no pudo ser encontrado: '+filename)
        exit()
    linelist = []
    for line in fhand:
        linelist.append(line.rstrip())
    questions = [] #aca se almacenan las preguntas y las respuestas
    for i in range(0,len(linelist),2):
        questions.append((linelist[i],linelist[i+1]))
    fhand.close()
    click.secho('> write "next" for next question and press Ctrl + C for exiting the program.',bg='red')
    for question in questions:
        click.secho('Q.' + question[0],fg='yellow')
        click.secho('A.' + question[1],fg='white')
        while True:
            answer = input('> ')
            match answer:
                case 'next':
                    break
                case _:
                    click.secho('Invalid input',fg='red')

@click.command()
@click.argument('filename')
@click.option('--test', is_flag=True ,default=False)
@click.option('--review', is_flag=True, default=False)
def remi_cli(filename,test,review):
    if review:
        review_file(filename)
    else:
        test_file(filename)
    
