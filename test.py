from engine.collider import *

col = Collider(PolygonBox(((0,0),(0,2),(1,1),(3,1),(3,2),(2,3),(3,4),(4,4),(5,3),(4,2),(4,1),(6,1),(7,2),(7,0))))

print(col.get_collision(Box(5,2), move=(-3.2,0.3)));

def print_file_stats(fileName:str)->None:
    with open(fileName) as file:
        n = file.read();
        v=n.count("\n")
        print(f'lines : {v}')
        n1 = n.replace('!', '').replace('\n',' ').replace('  ', ' ').split(' ')
        v = len(n1);
        print(f'words : {v}')
        v = len([i for i in n1 if i.isalpha()])
        print(f'- only alpha : {v}')
        v = len([i for i in n1 if i.isdigit()])
        print(f'- only digits : {v}')
        v = len(n)
        print(f'chars : {v}')
        al = [i for i in n if i.isalpha()]
        di = len([i for i in n if i.isdigit()])
        oth = v-len(al)-di
        print(f'- alpha : {len(al)}')
        print(f'--- lower : {len([i  for i in al if i.lower()==i])}')
        print(f'--- upper : {len([i  for i in al if i.upper()==i])}')
        print(f'- digits : {di}')
        print(f'- other : {oth}')


