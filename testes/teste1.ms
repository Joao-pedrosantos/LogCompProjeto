// Definindo uma variável
times = 30;

// Tentando pressionar a tecla W várias vezes
try:
    press W, times;
    exit();
catch:
    show("error pressing W");
    tryagain();
