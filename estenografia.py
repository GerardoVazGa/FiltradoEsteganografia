import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox



#[5]
def abrirArch():

    global ruta
    ruta = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")])
    
    if ruta:
        messagebox.showinfo("Archivo Seleccionado", f"El archivo seleccionado: {ruta}")
    else:
        messagebox.showerror("Error", "No se selecciono ningun archivo")

#[7]
def verificarArchivo(passw):
    contra = passw.get()

    if not ruta:
        messagebox.showerror("Error", "No se selecciono ningun archivo")
        return
    
    try:
        comando = ["steghide", "info", "-p", contra, ruta]
        print(f"Ejecutando comando: {' '.join(comando)}")
        #[8]
        resultado = subprocess.run(comando, capture_output=True, text=True, encoding='latin-1')
        if resultado.returncode == 0:
            messagebox.showinfo("Verificado", resultado.stdout)
        else:
            messagebox.showerror("Error", f"Error al ejecutar steghide: {resultado.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error en la ejecución del comando: {e}")
        print(f"stderr: {e.stderr}")
        messagebox.showerror("Error", f"Error en la ejecución del comando: {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

#[10]
def eliminarDatos(contra):
    print("Entre a la funcion")
    passw = contra.get()

    if not ruta:
        messagebox.showerror("Error", f"El archivo {ruta} no existe")
        return
    
    #[11]
    directorio = os.path.dirname(ruta)
    datosOculto = os.path.join(directorio, "datos_ocultos")
        
    if os.path.exists(datosOculto):
        os.remove(datosOculto)
    
    try:
        #[12]
        comandoext = ["steghide", "extract", "-sf", ruta, "-p", passw, "-f", "-xf", "datos_ocultos"]
        print(f"Ejecutando comando: {' '.join(comandoext)}")
        resultado = subprocess.run(comandoext, capture_output=True, text=True, encoding='latin-1')

        #[13]
        if resultado.returncode == 0:
            #directorio = os.path.dirname(ruta)
            #[14]
            nombreArch, extension= os.path.splitext(os.path.basename(ruta))
            print(nombreArch + extension)
            

            rutaArchivo = os.path.join(directorio, f"{nombreArch}_limpio{extension}")
            
            #[15]
            comandoCpNueva = ["convert", ruta, rutaArchivo]
            print(f"Ejecutando comando: {' '.join(comandoCpNueva)}")
            subprocess.run(comandoCpNueva, check=True)
            print(f"Comando convert ejecutado con éxito")

            #[16]
            comandoRm = ["rm", ruta]
            print(f"Ejecutando comando: {' '.join(comandoRm)}")
            subprocess.run(comandoRm, check=True)
            print(f"Archivo {ruta} eliminado con éxito")
            messagebox.showinfo("Éxito", f"Archivo {ruta} eliminado y {rutaArchivo} creado.")
        else:
            messagebox.showinfo("Error", f"No existen datos es: {resultado.stderr}")
            
    except subprocess.CalledProcessError as e:
        print(f"Error en la ejecución del comando: {e}")
        print(f"stderr: {e.stderr}")
        messagebox.showerror("Error", f"Error en la ejecución del comando: {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

#[6]
def abrirVentanaVerif():
    ventanaVerif = tk.Toplevel(window)
    ventanaVerif.title("Verificar Archivo")
    ventanaVerif.geometry("350x200")

    lblContra = tk.Label(ventanaVerif, text="Ingresa la contraseña:")
    lblContra.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N, padx=10, pady=5)

    entry_contraseña = tk.Entry(ventanaVerif, show="*")
    entry_contraseña.pack(side=tk.TOP, fill=tk.NONE, padx=10, pady=10)

    btnVerificar = tk.Button(ventanaVerif, 
                             text="Verificar", 
                             font=("Arial", 14), 
                             padx=2, 
                             command=lambda: verificarArchivo(entry_contraseña))
    
    btnVerificar.pack(side=tk.TOP, fill=tk.NONE, padx=10, pady=10)

#[9]
def abrirEliminacion():
    ventanaElim = tk.Toplevel(window)
    ventanaElim.title("Eliminar Datos")
    ventanaElim.geometry("350x200")

    lblContra = tk.Label(ventanaElim, text="Ingresa la contraseña:")
    lblContra.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N, padx=10, pady=5)

    entry_contraseña = tk.Entry(ventanaElim, show="*")
    entry_contraseña.pack(side=tk.TOP, fill=tk.NONE, padx=10, pady=10)

    btnVerificar = tk.Button(ventanaElim, 
                             text="Eliminar Datos", 
                             font=("Arial", 14), 
                             padx=2, 
                             command=lambda: eliminarDatos(entry_contraseña))
    
    btnVerificar.pack(side=tk.TOP, fill=tk.NONE, padx=10, pady=10)


#[1]
window = tk.Tk()
window.title("Selecciona un archivo e ingresa un texto")

ruta = ""

#[2]
abrirArchButton = tk.Button(window, text="Abrir archivo", command=abrirArch)
abrirArchButton.pack(padx=40, pady=10)

#[3]
btnVerificarArchVentana = tk.Button(window, text="Verificar archivo", command=abrirVentanaVerif)
btnVerificarArchVentana.pack(padx=40, pady=10)

#[4]
btnEliminacion = tk.Button(window, text="Eliminar datos", command=abrirEliminacion)
btnEliminacion.pack(padx=40, pady=10)

window.mainloop()