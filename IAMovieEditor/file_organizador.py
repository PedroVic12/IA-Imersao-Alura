import os

import shutil
path = "/home/pedrov/Downloads"

files = os.listdir(path)


print("Iniciando organizacação na pasta ", path)
for file in files:
	filename, extension = os.path.splitext(file)
	extension = extension[1:]


	if os.path.exists(path + "/" + extension):
		fil1 = path + "/" + file
		fil2 = path + "/" + extension + "/" + file
		shutil.move(fil1,fil2)
	else:
		os.makedirs(path + "/" + extension)



print("Arquivos organizados:")