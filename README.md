# Proyecto1Modelos
Resumen del proyecto:

El proyecto consiste en una página web la cual sube tutoriales sobre informática y ayuda a los usuarios a ampliar sus conocimientos de bakend, fronted y fullStack con muchas herramientas de aprendizajes y cursos llenos de tutoriales.

------------------------------
1 MODELOS: 

En total tenemos 10 modelos: 

1. Usuairo 
2. Perfil
3. Favorito
4. Comentario
5. Categoria
6. Subcategoria
7. Tutorial
8. Certificado
9. Etiqueta
10. Curso

----------------------------

1. Usuario:

Este modelo es el usuario cliente el cual tiene un perfil con sus datos y descripciones, y puede usar la pagina de tutoriales, sacandose certificados de los mismo.

2. Perfil: 

Este modelo es información extra del usuario que no se muetsra solo en el usuario.

3. Favorito:

Este modelo es una referencia a los tutoriales que el usuario marque en favoritos paara poder continuarlos luego o verlos mas tarde o por el simple hecho que le haya gustado.

4. Comentario: 

Este modelo es un campo de texto de cada usuario el cual pueden dejar reseñas sobre los tutoriales o brindar información adllancente de los mismos, no solo enseñan los maestros, tambien se puede aprender de los alumnos.

5. Categoria: 

Este modelo esta hecho con la intencion de actuar como filtro entre los tutoriales como programacion, base de datos...

6. Subcategoria: 

Este modelo es parecido a Categoria solo que este detalla mas dentro del campo escojido por ejemplo s es programacion, filtrar por bakend, fronted, python, java, JS...

7. Certificado: 

Este modelo se basa en una certificacion que obtiene el usuario al completar el tutorial elejido

8. Tutorial: 

Este modelo es la red principal de tutoriales, es decir, es el tutorial que enseña practicas al usuario.

9. Etiqueta: 

Este modelo esta diseñado para ver todo el contenido del tutorial por ejemplo que nos metemos en un tutorial de python, podremos ver en las etiquetas para lo que puede llegar a servir como por ejemplo #bakend #programador #lenjuages ...

10. Curso: 

Este modelo va a ser como referencia si estuvieran en una clase o laboratorio de practicas el cual tendra varios tutoriales, y una vez completado el curso se dara el certificado del mismo. 

------------------------------------

Atributos:

1. Usuario: 

- nombre = Nombre de usuario
- email = correo o email del usuario
- fecha de registro = fecha en la que se registra el usuario
- es_activo = booleano que nos dice si la cuenta de usuario a sido activa o esta activada o fue desactivada.
- puntuacion = puntuacion que dan otros usuario sobre el contenido de este usuario como comentarios.

2. Perfil: 

- bio = biografia del usuario
- estudios = estuduos o niveles del usuario
- fecha_de_nacimiento = fecha de nacimiento del usuario
- redes = enlace a las redes sociales del usuario

3. Tutorial

- titulo = Titulo del tutorial
- contenido = contenido del tutorial 
- fecha_creacion = fecha en la cual se creo el tutorial
- numero_visitas = numero de visitas que tiene el tutorial
- valoracion = valoracion que deja el usuario sobre el tutorial

4. Categoria

- nombre = nombre de la categoria
- descripcion = descripcion breve de la categoria
- es_activa = indica si la categoria esta activa o no
- popularidad = indica el valor numerico que refelja cuantas veces aparece esa categoria en un tutorial

5. Subcategoria

- nombre = nombre de la subcategoria
- descripcion = descripcion breve de la subcategoria
- fecha_creacion = fecha en la cual se creo la subcategoria
- es_activa = booleano que indica si esta o no activa

6. Comentario

- contenido = texto dejado por el usuario
- fecha_comentario = fecha del comentario
- es_visible = booeano que indica si el comentario es visible para el resto de usuarios o no
- puntuacion = valoraciones que ponen los usuario sobre lo util o interesantes que les ha sido

7. Etiqueta

- nombre = nombre de la etiqueta
- color = es un codigo de color para diferencia unas etiquetas de otras (Me estaba quedando sin idead)
- publica = booleano el cual nos dice si la etiqueta es publica o no para el resto de usuarios
- descripcion = breve descripcion de la etiqueta

8. Favorito

- fecha_guardado = fecha en la que se guarda el tutoruial en la seccion de favoritos del usuario
- comentario_favorito = comentario de usuario/os los cuales estasn guardados en la seccion de favoritos
- importancia = valoracion decimal por parte del usuario hacia el tutorial o comentario
- notificacion = booleano el cual nos indica si un tutoria que tenemos en guardado subre nuvo contenido. 

9. Curso

- nombre = nombre del curso
- descripcion = descripcion completa del curso
- duracion = numero de horas totales que dura el curso
- precio = coste del curso para los usuarios

10. Certificado

- fecha_emision = fecha en la que emitio el certificado
- codigo_verificacion = codigo que permite verificar la aunteticidad del certificado
- nivel = nivel de logro del curso
- url_descarga = url para descargarnos nuestro certificado

--------------------------------------------

PARAMETROS: 

- max_length: Establece una longitud maxima de caracteres
- auto_now : Actualiza automaticamente el campo fecha con la fecha y hora actuales
- default : Especifa un valor predeterminado para un campo determinado
- max_digits : Define un numero totales de digitos antes del punto o coma decimal
- decimal_places : Define un numero de caracteres maximos para los decimales despues del punto o coma
- choices : Define un conjunto de opciones predefinidas para un campo el cual podremos elejir
- related_name : Especifica erl nombre de un campo inverso para acceder a una relacion desde el otro lado.
- required : Especifica el campo que si o si es requerido.
- blank : Especifica si el campo se puede dejar en blanco o no. 
- null : Especifica si el campo puede llegar a ser null o no.
