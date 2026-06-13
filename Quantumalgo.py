import tkinter as tk
from tkinter import messagebox,ttk
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#--------------- Grover's algorithm --------------------------------------------------------------------------------------------

def oracle_grover(qc,tar):
    n=len(tar)
    for i in range(n):
        if tar[i]=="0":
            qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)),n-1)
    qc.h(n-1)
    for i in range(n):
        if tar[i]=="0":
            qc.x(i)
def diffusion(qc,n):
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)),n-1)
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))

#----------------- Algorithm running logic -------------------------------------------------------------------------------------

def run_simulation():
    selected=algorithm_var.get()
    if selected== "Deutsch-Jozsa":
        run_deutsch_jozsa()
    elif selected== "Grover":
        run_grover()
    elif selected=="Bernstein-Vazirani":
        run_bv()
    else:
        messagebox.showinfo("info : algorithm is not yet selected and being processed")

#---------------------------- Deutsch - Jozsa algorithm simulation and implementation ------------------------------------------

def run_deutsch_jozsa():
    try:
        n=int(qubit_entry.get())
        shot=int(shots_entry.get())
        oracle_choice=oracle_var.get()
        qc=QuantumCircuit(n+1,n)
        qc.x(n)
        qc.h(range(n+1))
        if oracle_choice=="Balanced":
            for i in range(n):
                qc.cx(i,n)
        elif oracle_choice=="Constant (0)":
            pass
        elif oracle_choice=="Constant (1)":
            qc.x(n)
        qc.h(range(n))
        qc.measure(range(n),range(n))
        qc.draw("mpl")
        plt.title("Deutsch Jozsa Algorithm")
        plt.show()
        simulator=Aer.get_backend("qasm_simulator")
        results=simulator.run(qc,shots=shot).result()
        count=results.get_counts()
        plot_histogram(count)
        plt.title("Measurement results")
        plt.show()
        
        if "0"*n in count:
            explanation=("result analysis :Deutsch jozsa algorithn \n\n"
                        "Since the output is all zeroes it points to constructive interference\n\n"
                        "conclusion:\n"
                        "the function is a constant function")
        else:
            explanation=("result analysis : Deutsch Jozsa algorithm\n\n"
                         "Since non-zero outputs also occur there  is destructive interference \n\n "
                         "Conclusion:\n"
                         "the function is a balanced function")
        result_text.delete("1.0",tk.END)
        result_text.insert(tk.END,explanation)
    except Exception as e:
        messagebox.showerror("Error",str(e))

#------------------------ Grover's search algorithm  ---------------------------------------------------------------------------
def run_grover():
    try:
        n=int(qubit_entry.get())
        shot=int(shots_entry.get())
        target=target_entry.get().strip()
        if len(target)!=n:
            messagebox.showerror(f"Error : Target must be{n}bits long ")
            return
        qc=QuantumCircuit(n,n)
        qc.h(range(n))
        import math
        iterations=max(1,int((math.pi/4)*(2**(n/2))))
        for _ in range(iterations):
            oracle_grover(qc,target[::-1])
            diffusion(qc,n)
        qc.measure(range(n),range(n))
        qc.draw("mpl")
        plt.title("Grover's algorithm")
        plt.show()
        simulator=Aer.get_backend("qasm_simulator")
        results=simulator.run(qc,shots=shot).result()
        count=results.get_counts()
        plot_histogram(count)
        plt.title("Grover results")
        plt.show()
        explanation=("result analysis: Grover's algorithm \n"
                         f"target state:{target}\n\n"
                         "oracle marks target\n"
                         "Diffusion amplifies probability\n"
                         "conclusion:"
                        "Target state appears with the highest probability\n"
            )
        result_text.delete("1.0",tk.END)
        result_text.insert(tk.END,explanation)
    except Exception as e:
        messagebox.showerror("Error ",str(e))

#--------------------   Bernstein-Vazirani algorithm -----------------------------------------------------------------------------

def run_bv():
    try:
        n=int(qubit_entry.get())
        shot=int(shots_entry.get())
        secret=target_entry.get().strip()
        if len(secret)!=n:
            messagebox.showerror("Error", f"The length of the string must be {n} bits long")
            return
        qc=QuantumCircuit(n+1,n)
        qc.x(n)
        qc.h(range(n+1))
        for i in range(n):
            if secret[i]=="1":
                qc.cx(i,n)
        qc.h(range(n))
        qc.measure(range(n),range(n))
        qc.draw("mpl")
        plt.title("Bernstein-Vazirani algorithm")
        plt.show()
        simulator=Aer.get_backend("qasm_simulator")
        results=simulator.run(qc,shots=shot).result()
        count=results.get_counts()
        plot_histogram(count)
        plt.title("Bernstein-Vazirani results")
        plt.show()
        explanation=("result analysis : Bernstein-Vazirani algorithm\n\n"
            f"hidden string is {secret}\n\n"
            "oracle encodes secret string\n\n"
            "extracted in one query instead of n queries in classical algorithm\n\n"
            "conclusion\n"
            "The secret string is found"
        )
        result_text.delete("1.0",tk.END)
        result_text.insert(tk.END,explanation)

    except Exception as e:
        messagebox.showerror("Error ",str(e))

#------------------------- Dynamic UI ---------------------------------------------------------------------------------------------

def update_parameters(event=None):
    selected=algorithm_var.get()
    oracle_frame.pack_forget()
    target_frame.pack_forget()
    if selected=="Deutsch-Jozsa":
        oracle_frame.pack(pady=5)
    elif selected in ["Grover","Bernstein-Vazirani"]:
        target_frame.pack(pady=5)

#---------------------------  Graphical User Interface --------------------------------------------------------------------------
root=tk.Tk()
root.title("Quantum Algorithm Simulation Software")
root.geometry("500x650")
root.configure(bg="#E3F2FD")
tk.Label(root,
         text="Quantum Algorithm Simulation Software",
         font=("Arial",13,"bold"),bg="#E3F2FD",
    fg="#0D47A1").pack(pady=10)
tk.Label(root,text="Select your Algorithm").pack()
algorithm_var=tk.StringVar()
algorithm_dropdown=ttk.Combobox(root,textvariable=algorithm_var)
algorithm_dropdown["values"]=("Deutsch-Jozsa","Grover","Bernstein-Vazirani")
algorithm_dropdown.current(0)
algorithm_dropdown.pack(pady=5)
algorithm_dropdown.bind("<<ComboboxSelected>>",update_parameters)
tk.Label(root,text="Parameters",font=("Arial",12,"bold"),bg="#E3F2FD",
    fg="#B71C1C").pack(pady=10)
tk.Label(root,text="Enter number of input qubits:", bg="#E3F2FD",
    fg="#0D47A1").pack()
qubit_entry=tk.Entry(root)
qubit_entry.insert(0,"2")
qubit_entry.pack(pady=5)

tk.Label(root,text="Enter number of shots:", bg="#E3F2FD",
    fg="#0D47A1").pack()
shots_entry=tk.Entry(root)
shots_entry.insert(0,"1024")
shots_entry.pack(pady=5)

# oracle frame
oracle_frame=tk.Frame(root,bg="#E3F2FD")
tk.Label(oracle_frame,text="Select the required type of oracle:", bg="#E3F2FD",
    fg="#0D47A1").pack(pady=5)
oracle_var=tk.StringVar()
oracle_dropdown=ttk.Combobox(oracle_frame,textvariable=oracle_var)
oracle_dropdown["values"]=("Balanced","Constant (0)","Constant (1)")
oracle_dropdown.current(0)
oracle_dropdown.pack(pady=5)
#Target frame

target_frame=tk.Frame(root,bg="#E3F2FD")
tk.Label(target_frame,text="Enter target or secret string :", bg="#E3F2FD",
    fg="#0D47A1").pack()
target_entry=tk.Entry(target_frame)
target_entry.insert(0,"11")
target_entry.pack(pady=5)

oracle_frame.pack(pady=5)

tk.Button(root,text="Run simulation",command=run_simulation,
          bg="#DA2748",fg="white").pack(pady=20)
tk.Label(root,text="Result Explaination:",font=("Arial",12,"bold")).pack()
result_text= tk.Text(root,height=10,width=70,wrap="word",font=("Arial",10),bg="#E8F4FD",
    fg="#0D47A1")
result_text.pack(pady=10)
root.mainloop()









                             




