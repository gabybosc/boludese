# renombra archivos, borrando los ocho últimos caracteres
for file in ./*.cdf; do
    mv "$file" "${file%????????}".cdf
done