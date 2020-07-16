#!bin/bash
for dir in package/*     # list directories in the form "/tmp/dirname/"
do
    echo $dir
    mkdir -p minified_pyminifier/$dir
    pyminifier --destdir=minified_pyminifier/$dir --obfuscate --gzip $dir/*.py
    for dir2 in $dir/*     # list directories in the form "/tmp/dirname/"
    do
        echo $dir2
        mkdir -p minified_pyminifier/$dir2
        pyminifier --destdir=minified_pyminifier/$dir2 --obfuscate --gzip $dir2/*.py
        for dir3 in $dir2/*     # list directories in the form "/tmp/dirname/"
        do  
            mkdir -p minified_pyminifier/$dir2
            pyminifier --destdir=minified_pyminifier/$dir2 --obfuscate --gzip $dir2/*.py
            echo $dir3
        done
    done
    
    #pyminifier --destdir=minified_pyminifier/$dir --obfuscate --gzip $dir/*.py
done