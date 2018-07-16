# Dataset

Para crear una instancia se recive *X*, *y*, *X_unlabeled* [, *test_size*,
*random_state*]

Al iniciarse la clase, divide el *X* dejando un porcentaje del mismo para test.
Ademas se crea un unico arreglo donde se guarda *X* y *X_unlabeled* juntos. Tambien
se crea otro arreglo de se ponen las etiquetas *y* y se agregan *-1* por cada
elemento sin etiquetar. Esto es para ahorrar tiempo y memoria dado que se
accese a *X* y *X_unlabeled* a traves de mascaras en *X*. De esta forma, al etiquetar
elementos nuevos solo tenemos que agregar el valor de la etiqueta al *y*
correspondiente y listo. La mascara sabra que esa entrada ahora es parte del
*X* para entrenamiento y no parte del *X_unlabeled*. De esta forma nos ahorramos
crear tablas nuevas cada vez que se etiquete un elemento.
