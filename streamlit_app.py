import streamlit as st

# Diccionario con usuarios registrados
usuarios_registrados = {
    "111111": "Samuel León",
    "222222": "Mariana Contreras",
    "333333": "Anny Sandoval",
    "444444": "Sebastián Ariza",
    "555555": "Alejandro Mendoza"
}

# Inventario inicial
if "inventario" not in st.session_state:
    st.session_state.inventario = [
        ["Máquina de espresso", "1001", "maquinaria", "N/A", 2],
        ["Molinillo de café", "1002", "maquinaria", "N/A", 3],
        ["Granos de café (variedad)", "2001", "materia prima", "N/A", 50],
        ["Café americano", "3002", "producto terminado", "terminado", 25],
    ]
    st.session_state.lista_cambios = []

categorias = {"maquinaria", "materia prima", "producto terminado", "en proceso"}

# ---- LOGIN ----
st.title("☕ Bienvenido a la Cafetería 'Cafecito' ☕")

doc = st.text_input("Ingrese su número de documento:")
if doc:
    if doc in usuarios_registrados:
        st.success(f"Acceso permitido. Bienvenido, {usuarios_registrados[doc]}!")
    else:
        st.error("Acceso denegado. Usuario no registrado en el sistema.")

# ---- MENÚ ----
opcion = st.sidebar.selectbox("Seleccione una opción:", [
    "Ver Inventario",
    "Agregar Implemento o Producto",
    "Quitar Implemento o Producto",
    "Modificar Cantidad",
    "Imprimir Lista de Cambios"
])

# ---- FUNCIONES ----
def mostrar_inventario():
    if not st.session_state.inventario:
        st.info("El inventario está vacío.")
        return
    for categoria in categorias:
        items = [i for i in st.session_state.inventario if i[2] == categoria]
        if items:
            st.subheader(f"🌟 {categoria.capitalize()} 🌟")
            for item in items:
                st.write(f"{item[0]} (Código: {item[1]}, Cantidad: {item[4]})")

def agregar_implemento():
    with st.form("agregar_form"):
        nombre = st.text_input("Nombre")
        codigo = st.text_input("Código (numérico)")
        tipo = st.selectbox("Tipo", list(categorias))
        cantidad = st.number_input("Cantidad inicial", min_value=0, step=1)
        enviado = st.form_submit_button("Agregar")
        if enviado:
            if any(i[1] == codigo for i in st.session_state.inventario):
                st.error("El código ya existe.")
            else:
                estado = "terminado" if tipo == "producto terminado" else "en proceso" if tipo == "en proceso" else "N/A"
                st.session_state.inventario.append([nombre, codigo, tipo, estado, cantidad])
                st.session_state.lista_cambios.append(["agregar", nombre, codigo, cantidad])
                st.success(f"'{nombre}' agregado al inventario.")

def quitar_implemento():
    codigos = [i[1] for i in st.session_state.inventario]
    codigo = st.selectbox("Seleccione el código a eliminar", codigos)
    if st.button("Eliminar"):
        for i in st.session_state.inventario:
            if i[1] == codigo:
                st.session_state.inventario.remove(i)
                st.session_state.lista_cambios.append(["quitar", i[0], codigo])
                st.success(f"'{i[0]}' eliminado.")
                break

def modificar_cantidad():
    codigos = [i[1] for i in st.session_state.inventario]
    codigo = st.selectbox("Seleccione el código a modificar", codigos)
    item = next((i for i in st.session_state.inventario if i[1] == codigo), None)
    if item:
        nueva_cantidad = st.number_input(f"Nueva cantidad para '{item[0]}'", min_value=0, value=item[4])
        if st.button("Actualizar"):
            item[4] = nueva_cantidad
            st.session_state.lista_cambios.append(["modificar", item[0], codigo, nueva_cantidad])
            st.success(f"Cantidad de '{item[0]}' actualizada.")

def imprimir_movimientos():
    if not st.session_state.lista_cambios:
        st.info("No se han realizado cambios.")
    else:
        for cambio in st.session_state.lista_cambios:
            accion, nombre, codigo, *cantidad = cambio
            cantidad_info = f", Cantidad: {cantidad[0]}" if cantidad else ""
            st.write(f"🌟 {accion.capitalize()} - {nombre} (Código: {codigo}){cantidad_info}")

# ---- EJECUCIÓN ----
if opcion == "Ver Inventario":
    mostrar_inventario()
elif opcion == "Agregar Implemento o Producto":
    agregar_implemento()
elif opcion == "Quitar Implemento o Producto":
    quitar_implemento()
elif opcion == "Modificar Cantidad":
    modificar_cantidad()
elif opcion == "Imprimir Lista de Cambios":
    imprimir_movimientos()