import tkinter as tk
import random
from tkinter.constants import CENTER, E, END, LEFT, W
from tkinter import messagebox



def is_it_prime(n):
    d = 2
    while d < n:
        if n % d != 0:
            d += 1
        else:
            return False
    return True 

def get_prime_numbers(fi=200):
    L = list(range(31, fi))
    prime_numbers = []
    for i in L:
        if is_it_prime(i):
            prime_numbers.append(i)
    return prime_numbers

def find_e(fi):
    flag = True
    while flag == True:
        e = random.choice(range(1000))
        if e % 2 == 0:
            e -= 1
        flag = (bool(find_all_dividers(e) & find_all_dividers(fi)))
    return e


def find_all_dividers(n):
    d = 2
    dividers = set()
    while d <= n:
        if n % d != 0:
            d += 1
        else:
            dividers.add(d)
            d += 1
    return dividers

def find_d(e, fi):
    #d - число обратное е по модулю fi => (d * e) % fi = 1
    d = 1
    while (d * e) % fi != 1:
        d += 1
    return d

def RSA_encode(message, e, mod):
    message_in_ASCII = []
    for i in message:
        message_in_ASCII.append(ord(i))
        #message_in_ASCII.reverse()

    encrypted_message = []
    for i in message_in_ASCII:
        a = i ** e % mod
        encrypted_message.append(a)
    return encrypted_message
 
def RSA_decode(encrypted_message, d, mod):
    decrypted_message = []
    for i in encrypted_message:
        a = i ** d % mod
        decrypted_message.append(a)

    message = []
    for i in decrypted_message:
        message.append(chr(i))
    return message

#______________________________________________________________


def tk_p_q_mod_fi():
    p, q = random.choices(get_prime_numbers(), k=2)
    e1.delete(0, END)
    e2.delete(0, END)
    e1.insert(0, p)
    e2.insert(0, q)
    mod_label['text'] = f'mod:  {p * q}'
    fi_label['text'] = f'φ: {(p-1) * (q-1)}'

def tk_keys():
    p = int(e1.get())
    q = int(e2.get())
    mod = p * q
    fi = (p-1) * (q-1)
    e = find_e(fi)
    d = find_d(e, fi)
    public_label['text'] = f'Открытый ключ: {{{e}, {mod}}}'
    privat_label['text'] = f'Личный ключ: {{{d}, {mod}}}'
    e_label['text'] = f'e: {e}'
    d_label['text'] = f'd: {d}'
    print(p, q, mod, fi, '___', e, d)

def self_tk_p_q_mod_fi():
    try:
        p = int(e1.get())
        q = int(e2.get())
        print(p, q)
    except:
        messagebox.showerror('О нет', 'Введите простые числа больше 30!')
    if is_it_prime(p) and is_it_prime(q) and p > 17 and q > 17:             #30
        e1.delete(0, END)
        e2.delete(0, END)
        e1.insert(0, p)
        e2.insert(0, q)
        mod_label['text'] = f'mod:  {p * q}'
        fi_label['text'] = f'φ: {(p-1) * (q-1)}'
    else:
        messagebox.showerror('О нет', 'Числа p и q должны быть простыми, а так же больше 30!')

def tk_RSA_encode():
    m = entry_text.get(1.0, END)
    e = e_label.cget('text')
    e = int(e[3:]) 
    mod = int(e1.get()) * int(e2.get())
    exit_text.delete(1.0, END)
    exit_text.insert(1.0, RSA_encode(m, e, mod))

def tk_RSA_decode():
    m = exit_text.get(1.0, END)
    print('do split: ', m)
    m = m.split()
    print('posle split :', m)
    m = [int(item) for item in m]
    d = d_label.cget('text')
    d = int(d[3:])
    mod = int(e1.get()) * int(e2.get())
    print('m: ', m, '\nd: ', d, '\nmod: ', mod)
    m_decode = ''.join(RSA_decode(m, d, mod))
    entry_text.delete(1.0, END)
    entry_text.insert(1.0, m_decode)

#_________________________________________________________________________________


win = tk.Tk()
win.title('Алгоритм RSA')
win.geometry('700x500+420+100')
win.resizable(False, False)

photo = tk.PhotoImage(file='C:/Users/250/Desktop/Py/RSA/bg.PNG')
bg_label = tk.Label(win, image=photo).place(x=0,y=0)

entry_text = tk.Text(win, width=44, height=10, wrap='word')
exit_text = tk.Text(win, width=44, height=10, wrap='word')
entry_text.place(x=0, y=120)
exit_text.place(x=350, y=120)

rsa_label = tk.Label(text="RSA", font=('Verdana',30, 'bold'), anchor=E, bg='#000D01', fg='#59FA69', relief='sunken', borderwidth=8).place(x=302, y=23)
l1 = tk.Label(text='Расшифрованный текст:', font=('Verdana',11)).place(x=0, y=95)
l2 = tk.Label(text='Зашифрованный текст:', font=('Verdana',11)).place(x=350, y=95)

p_label = tk.Label(text='p:',font=('Verdana',9))
q_label = tk.Label(text='q:',font=('Verdana',9))
mod_label = tk.Label(text='mod:',font=('Verdana',9))
fi_label = tk.Label(text='φ:',font=('Verdana',9))
p_label.place(x=10, y=290)
q_label.place(x=10, y=320)
mod_label.place(x=10, y=350)
fi_label.place(x=10, y=380)

e1 = tk.Entry(width=10)
e2 = tk.Entry(width=10)
e1.place(x=30, y=290)
e2.place(x=30, y=320)

btn_prime = tk.Button(text='Сгенерировать простые числа', command=tk_p_q_mod_fi)
btn_prime.place(x=100, y=290)
btn_self_prime = tk.Button(text='Ввести свои числа', command=self_tk_p_q_mod_fi)
btn_self_prime.place(x=100, y=320)

public_label = tk.Label(text='Открытый ключ: {e, mod}',font=('Verdana',9))
privat_label = tk.Label(text='Личный ключ: {d, mod}',font=('Verdana',9))
public_label.place(x=350, y=290)
privat_label.place(x=350, y=320)

e_label = tk.Label(text='e:',font=('Verdana',9))
d_label = tk.Label(text='d:',font=('Verdana',9))
e_label.place(x=350, y=350)
d_label.place(x=350, y=380)

btn_keys = tk.Button(text='Сгенерировать ключи', command=tk_keys)
btn_keys.place(x=550, y=290)

btn_encode = tk.Button(text='Зашифровать', font=('Verdana',29), width=13, bd=5, command=tk_RSA_encode)
btn_decode = tk.Button(text='Расшифровать', font=('Verdana',29), width=13, bd=5, command=tk_RSA_decode)
btn_encode.place(x=10, y=410)
btn_decode.place(x=350, y=410)

fav = tk.PhotoImage(file='C:/Users/250/Desktop/Py/RSA/favicon.png')
win.iconphoto(False, fav)




# p, q = random.choices(get_prime_numbers(), k=2)
# mod = p * q
# fi = (p-1) * (q-1)
# e = find_e(fi)
# d = find_d(e, fi)


# publickey =  {e, mod}
# privalkey  = {d, mod}

# message = 'hello' #entry_text.get(1.0, END)

# encode_m = RSA_encode(message, e, mod)
# decode_m = ''.join(RSA_decode(encode_m, d, mod))

# print(encode_m)
# print(decode_m)


# print('p, q, mod is ', p, q, mod)
# print('fi is ',fi)
# print('e is ',e)
# print(RSA_encode('Hello', e, mod))
# q = (RSA_encode('Hello', e, mod))
# print(''.join(RSA_decode(q, d, mod)))

win.mainloop()