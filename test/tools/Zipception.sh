#!/bin/bash
# Indique au système que l'argument qui suit est le programme utilisé pour exécuter ce fichier
# En règle générale, les "#" servent à mettre en commentaire le texte qui suit comme ici
echo Mon premier script
echo Liste des fichiers :
for dir in `find [0-9a-zA-Z]* -type d`;
do
  echo "dir $dir";
  cd "./$dir";
  pwd
  for file in `find ./*.gz` ;
  do echo "trouvé $file";
  gunzip $file ;
  done
  cd ./..
  pwd
done
.
