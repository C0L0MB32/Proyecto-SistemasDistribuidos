from modificarBD import *

def menu_user(conexion):
    # Solicitar al usuario que ingrese su ID
    id_usuario = input("Por favor, ingrese su ID de usuario: ")

    # Consultar el usuario por ID
    usuario = consultar_usuario_por_id(conexion, id_usuario)
    # Verificar si se encontró el usuario
    if usuario:
        print(f"Bienvenido, {usuario[1]} {usuario[2]}")

        # Mostrar el menú de opciones
        while True:
            print("\nMenú:")
            print("1. Ver perfil")
            print("2. Editar perfil")
            print("3. Ver dispositivos")
            print("4. Abrir ticket de soporte")
            print("5. Ver tickets")
            print("6. Cerrar sesión")

            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                ver_perfil(usuario)
            elif opcion == '2':
                editar_perfil(conexion, usuario)
            elif opcion == '3':
                ver_dispositivos(conexion)
            elif opcion == '4':
                abrir_ticket_soporte(conexion, usuario)
            elif opcion == '5':
                consultar_ticket_por_id_user(conexion, usuario[0])
            elif opcion == '6':
                print("Sesión cerrada. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
    else:
        print("Usuario no encontrado. Por favor, verifique su ID.")

def ver_perfil(usuario):
    print("Perfil del usuario:")
    print("ID:", usuario[0])
    print("Nombre:", usuario[1])
    print("Apellido:", usuario[2])
    print("Correo:", usuario[3])
    print("Teléfono:", usuario[4])

def editar_perfil(conexion, usuario):
    print("Editar perfil:")
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")
    nuevo_correo = input("Nuevo correo electrónico: ")
    nuevo_telefono = input("Nuevo número de teléfono: ")

    editar_datos_usuario(conexion, usuario[0], nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono)

    print("Perfil actualizado correctamente")

def abrir_ticket_soporte(conexion, usuario):
    print("Crear ticket de soporte:")
    descripcion = input("Descripción del problema: ")

    try:
        cursor = conexion.cursor()

        # Seleccionar al ingeniero con la menor cantidad de tickets asignados
        cursor.execute("SELECT id FROM INGENIEROS ORDER BY (SELECT COUNT(*) FROM TICKETS WHERE ingeniero_id = INGENIEROS.id) LIMIT 1")
        ingeniero_id = cursor.fetchone()[0]

        # Insertar el nuevo ticket con el ingeniero asignado
        sql_insert_query = """INSERT INTO TICKETS (usuario_id, ingeniero_id, descripcion, fecha, status) 
                              VALUES (%s, %s, %s, CURRENT_DATE, 'Pendiente')"""
        valores = (usuario[0], ingeniero_id, descripcion)
        cursor.execute(sql_insert_query, valores)
        conexion.commit()
        print("Ticket de soporte creado correctamente")
    except mysql.connector.Error as error:
        print("Error al crear ticket de soporte:", error)

