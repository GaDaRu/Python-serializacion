import tkinter
import pickle
import csv
from tkinter import ttk
from modelo.contacto import *
from tkinter import messagebox

class app(tkinter.Frame):
    contactos = []

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # self.lista()
        self.create_widgets()
        # ventana = tkinter()
        # ventana.title("Agenda")
        # ventana.mainloop()

    def create_widgets(self):
        # self.labelframe1 = tkinter.LabelFrame(self)
        # self.labelframe1.grid(row=0, column=0)

        self.texto = tkinter.Label(self)
        self.texto["text"] = "Lista Contactos"
        self.texto.grid(row=0, column=1)

        for i in self.contactos:
            nom = "hola"+str(i)
            self.nom = tkinter.Label(self)
            self.nom["text"] ="Numbre: {}, Apellidos: {}, Telefono: {}".format(i.nombre, i.apellidos, i.telefono)+"\n"
            self.nom.grid(row=1, column=1)

        self.ana = tkinter.Label(self)
        self.ana["text"] = "Añadir Contacto"
        self.ana.grid(row=2, column=1)

        self.nombre = tkinter.Entry(self)
        self.nombre.grid(row=3, column=0)

        self.apellido = tkinter.Entry(self)
        self.apellido.grid(row=3, column=1)

        self.telefono = tkinter.Entry(self)
        self.telefono.grid(row=3, column=2)

        self.anadir = tkinter.Button(self, text="Guardar", command=lambda: self.guardar())
        self.anadir.grid(row=4, column=0)

        self.anadir = tkinter.Button(self, text="Modificar", command=lambda: self.modificar())
        self.anadir.grid(row=4, column=1)

        self.anadir = tkinter.Button(self, text="Eliminar", command=lambda: self.eliminar())
        self.anadir.grid(row=4, column=2)

        tkinter.Label(self, text='Selecciona la eleccion para moddicficar').grid(
            row=0, column=2, columnspan=3)

        self.combo = ttk.Combobox(self, state='readonly', width=17, justify='center')
        self.combo["values"] = ['Nombre', 'Apellido', 'telefono']
        self.combo.grid(row=1, column=2, padx=15)
        self.combo.current(0)

        three_frame = tkinter.LabelFrame(self)
        three_frame.grid(row=5, column=1)

        self.tree = ttk.Treeview(three_frame, height=10, columns=("one", "two"))
        self.tree.grid(padx=5, pady=5, row=0, column=0, columnspan=1)
        self.tree.heading("#0", text='Nombre', anchor= tkinter.CENTER)
        self.tree.heading("one", text='Apellidos', anchor= tkinter.CENTER)
        self.tree.heading("two", text='Telefono', anchor= tkinter.CENTER)

        self.quit = tkinter.Button(self, text="Salir", fg="red", command=self.master.destroy)
        self.quit.grid(row=6, column=3)

    def guardar(self):
        contac = Contacto(self.nombre.get(), self.apellido.get(), self.telefono.get())
        self.nombre.insert(0, "")
        # self.anadirContacto(contac)
        print("Nombre: "+contac.getNombre()+" Apellido: "+contac.getApellidos()+" Telefono: "+contac.getTelefono())

        nombre = self.nombre.get()
        apellido = self.apellido.get()
        telefono = self.telefono.get()
        contact_check = [nombre, apellido, telefono]
        if contact_check == ['', '', '']:
            self.mensaje()
        else:
            if nombre == '':
                nombre = '<Default>'
            if apellido == '':
                apellido = '<Default>'
            if telefono == '':
                telefono = '<Default>'
            self.save(nombre, apellido, telefono)
            self.tree.insert("", 0, text="------------------------------",
                             values=("------------------------------", "------------------------------"))
            self.tree.insert("", 0, text=str(nombre), values=(str(apellido), str(telefono)))
            self.tree.insert("", 0, text="Nuevo nombre añadido", values=("Nuevo apellido añadido", "Nuevo telefono añadido"))
            self.tree.insert("", 0, text="------------------------------",
                             values=("------------------------------", "------------------------------"))
        contact_check = []
        self.limpiar()

    def mensaje(self):
        print("Introduce todos los datos")

    def save(self, nombre, apellido, telefono):
        s_name = nombre
        s_phone = apellido
        s_email = telefono
        with open('contacts_list.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\r', delimiter=',')
            writer.writerow((s_name, s_phone, s_email))

    def limpiar(self):
        self.nombre.delete(0, "end")
        self.apellido.delete(0, "end")
        self.telefono.delete(0, "end")

    def modificar(self):
        answer = []
        var_search = str(self.combo.get())
        if var_search == 'Nombre':
            var_inbox = self.nombre.get()
            possition = 0
            answer = self.search(var_inbox, possition)
            self.check_1(answer, var_search)
        elif var_search == 'Apellido':
            var_inbox = self.apellido.get()
            possition = 1
            answer = self.search(var_inbox, possition)
            self.check_1(answer, var_search)
        else:
            var_inbox = self.telefono.get()
            possition = 2
            answer = self.search(var_inbox, possition)
            self.check_1(answer, var_search)
        self.limpiar()

    def eliminar(self):
        nombre = str(self.nombre.get())
        a = self.delete_mesageBox(nombre)
        if a == True:
            with open('contacts_list.csv', 'r') as f:
                reader = list(csv.reader(f))
            with open('contacts_list.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                for i, row in enumerate(reader):
                    if nombre != row[0]:
                        writer.writerow(row)
        self.clean()
        self.show_contacts()

    def clean(self):
        self.limpiar()
        self.clean_treeview()

    def show_contacts(self):
        self.tree.insert("", 0, text="------------------------------",
                         values=("------------------------------", "------------------------------"))
        self.view_csv()
        self.tree.insert("", 0, text="------------------------------",
                         values=("------------------------------", "------------------------------"))

    def view_csv(self):
        contacts = self.alphabetic_order.alphabetic_order()
        for i, row in enumerate(contacts):
            nombre = str(row[0])
            apellido = str(row[1])
            telefono = str(row[2])
            self.tree.insert("", 0, text=nombre, values=(apellido, telefono))

    def alphabetic_order(self):
        my_order = []
        my_row = []
        with open('contacts_list.csv', 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                nombre = str(row[0])
                apellido = str(row[1])
                telefono = str(row[2])
                my_row = [nombre, apellido, telefono]
                my_order.append(my_row)
        alphabetic_order_list = self.ordenamiento_por_mezcla(my_order)
        return alphabetic_order_list

    def ordenamiento_por_mezcla(self, lista):
        if len(lista) > 1:
            medio = len(lista) // 2
            izquierda = lista[: medio]
            derecha = lista[medio:]
            self.ordenamiento_por_mezcla(izquierda)
            self.ordenamiento_por_mezcla(derecha)
            i = 0
            j = 0
            k = 0
            while i < len(izquierda) and j < len(derecha):
                if izquierda[i] < derecha[j]:
                    lista[k] = derecha[j]
                    j += 1
                else:
                    lista[k] = izquierda[i]
                    i += 1
                k += 1
            while i < len(izquierda):
                lista[k] = izquierda[i]
                i += 1
                k += 1
            while j < len(derecha):
                lista[k] = derecha[j]
                j += 1
                k += 1
        return lista

    def clean_treeview(self):
        tree_list = self.tree.get_children()
        for item in tree_list:
            self.tree.delete(item)

    def search(self, var_inbox, possition):
        my_list = []
        s_var_inbox = str(var_inbox)
        var_possition = int(possition)
        with open('contacts_list.csv', 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if s_var_inbox == row[var_possition]:
                    my_list = [row[0], row[1], row[2]]
                    break
                else:
                    continue
        return my_list

    def check_1(self, answer, var_search):
        val_modify = answer
        var = var_search
        if val_modify == []:
            self.no_found(var)
        else:
            print("Modificado")
            # TopLevelModify(self, val_modify)

    def no_found(self, var):
        var_s = str(var)
        print("Error X")

    def delete_mesageBox(self, nombre):
        var_name = str(nombre)
        if var_name == '':
            self.write_name()
        else:
            search = messagebox.askquestion("Eliminar", "¿Quieres eliminar este cotacto?\n" + var_name)
            if search == "yes":
                return True
            else:
                return False

    def write_name(self):
        print("Error al eliminar")

    # def lista(self):
    #     try:
    #         listaContactos = open("contactos", "ab+")
    #         listaContactos.seek(0)
    #         self.contactos = pickle.load(listaContactos)
    #         print("Cargados {} contactos".format(len(self.contactos)))
    #     except:
    #         print("No existe ninguna lista de contactos, se procede a crear una.")
    #     finally:
    #         listaContactos.close()
    #         del (listaContactos)
    #
    # def escribirLista(self):
    #     listaContactos = open("contactos", "wb")
    #     pickle.dump(self.contactos, listaContactos)
    #     listaContactos.close()
    #     del (listaContactos)
    #
    # def anadirContacto(self, contacto):
    #     self.contactos.append(contacto)
    #     self.escribirLista()
    #
    # # def mostrarContactos(self):
    # #     for i in self.contactos:
    # #         print("Numbre: {}, Apellidos: {}, Telefono: {}".format(i.nombre, i.apellidos, i.telefono))
    #

root = tkinter.Tk()
app = app(master=root)
app.mainloop()