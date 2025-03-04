COMANDO DOKCER: 

docker run -p 8092:8092 --name mi_api_container carlospereafiguera/mi_api_image:1.0


Los usuarios que hay dentro de este proyecto son:

1.- Administrador 

2.- Profesor

3.- Estudiante

Los permisos varian dependiendo que que tipo de usuarios seremos: 

1.- Administrador:

Acceso a todo y cual quier tipo de modificaciones sin restricciones.

2.- Profesor:

Acceso a la mayoria de los apartados, pudiendo crear, modificar, eliminar y buscar:

-Cursos
-Usuarios
-Tutoriales
-Etiquetas
-Comentarios


3.- Estudiante pudiendoo acceder a los requisitos minimos para poder estudiar: 

-Cursos (solo ver).
-Comentarios (ver y crear).
-Tutoriales (Solo ver).
-Etiquetas (solo ver).
