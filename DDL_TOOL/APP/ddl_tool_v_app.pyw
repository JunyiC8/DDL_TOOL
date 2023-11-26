import os
import sys
import tkinter as tk
import subprocess
from tkinter import *
from tkinter import scrolledtext


def quit():  # Your exit routine
    root.destroy()

def max_element_in_list(_list):
    list_version=[]
    if len(_list)==1:
        return _list[0]
    else:
        for i in range(0,len(_list)):
            list_version =list_version+[ _list[i][_list[i].find('_v')+2:]]
        return _list[0][:_list[0].find('_v')+2]+max(list_version)


def get_selection() -> list:
    list_sel.clear()
    if (var_ddl_tab.get() == True):
        list_sel.append(var_ddl_tab_opt.get())
    if (var_ddl_view.get() == True):
        list_sel.append(var_ddl_view_opt.get())
    # if (var_ddm.get() == True):
    #     list_sel.append(var_ddm_opt.get())
    return list_sel


def run_bat(exe_path):
    proc = subprocess.Popen(exe_path, shell=True, stderr=subprocess.PIPE)
    return proc.stderr.readlines()


def Scroll(file_name):
    scroll = scrolledtext.ScrolledText(root, width=70, height=16, font=('黑体', 8))
    scroll.place(x=30, y=80)
    # filename = os.path.join(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'App'),'test.txt')
    exe_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'Bin'), file_name)
    for line in run_bat(exe_path):
        scroll.insert(tk.END, line)
    # with open(filename, 'r', encoding='utf-8') as fp:
    #     for line in fp:
    #         scroll.insert(tk.END, line)
    scroll.insert(tk.END, '----END----')


def gotorun():
    if len(list_sel) > 0:
        for widget in frame_top_run.winfo_children():
            widget.destroy()
        for widget in frame_bottom_run.winfo_children():
            widget.destroy()

        frame_top_run.pack()
        filename = list_sel.pop(0)
        _label = Label(frame_top_run, text=filename,
                       image=icon,
                       compound='left',
                       font=('Calibri', 13))
        _label.pack(side=tk.TOP, anchor='nw')
        Scroll(filename + '.exe')

        frame_bottom_run.pack(side=tk.BOTTOM, anchor='e')

        if len(list_sel) > 0:
            button_run = tk.Button(frame_bottom_run, text="NEXT"
                                   , relief='raised', command=gotorun)
        else:
            button_run = tk.Button(frame_bottom_run, text="CLOSE"
                                   , relief='raised', command=quit)

        button_back = tk.Button(frame_bottom_run, text="BACK"
                                , relief='raised', command=menu)

        button_back.pack(side='left', padx=30)

        button_run.pack(side='left',pady=10)

        frame_top_menu.pack_forget()
        frame_top_menu_opt.pack_forget()
        frame_bottom_menu.pack_forget()
    else:
        for widget in frame_top_menu_opt.winfo_children():
            if widget.winfo_class() == 'Label':
                widget.destroy()
        label_warning = tk.Label(frame_top_menu_opt, text='You must select one before press RUN', fg='red', font=('Calibri', 10))
        label_warning.pack(side='bottom', anchor='w')


def menu():
    global frame_top_run
    global frame_bottom_run
    global frame_top_menu,frame_top_menu_opt, frame_bottom_menu
    global list_sel
    global var_ddl_tab
    global var_ddl_view #, var_ddm
    global choice_ddl_tab, choice_ddl_view #, choice_ddm
    global button_run
    global name_ddl_tab, name_ddl_view #, name_ddm
    global var_ddl_tab_opt
    global var_ddl_view_opt #, var_ddm_opt

    for widget in root.winfo_children():
        widget.destroy()

    frame_top_run = tk.Frame(root, padx=60, pady=10)

    frame_bottom_run = tk.Frame(root, padx=30)

    frame_top_menu = tk.Frame(root, padx=50, pady=30) ##

    frame_top_menu_opt = tk.Frame(root,  pady=40)

    frame_bottom_menu = tk.Frame(root)

    frame_top_run.pack()

    frame_bottom_run.pack(side=tk.BOTTOM, anchor='e')

    frame_top_menu.pack(side=tk.LEFT, anchor='nw')

    frame_top_menu_opt.pack(side=tk.LEFT, anchor='ne')

    list_ddl_table = []
    list_ddl_view = []
    # list_ddm = []
    for file_name in os.listdir(os.path.join(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'Bin'))):
        if 'DDL_TABLE_GENERATOR' in file_name:
            list_ddl_table = list_ddl_table + [file_name.replace('.exe', '')]
        elif 'DDL_VIEW_GENERATOR' in file_name:
            list_ddl_view = list_ddl_view + [file_name.replace('.exe', '')]
        # elif 'DDM_GENERATOR' in file_name:
        #     list_ddm = list_ddm + [file_name.replace('.exe', '')]

    name_ddl_tab=max_element_in_list(list_ddl_table)
    name_ddl_view=max_element_in_list(list_ddl_view)
    # name_ddm=max_element_in_list(list_ddm)

    var_ddl_tab_opt = tk.StringVar()
    var_ddl_tab_opt.set(max_element_in_list(list_ddl_table))
    var_ddl_view_opt = tk.StringVar()
    var_ddl_view_opt.set(max_element_in_list(list_ddl_view))
    var_ddm_opt = tk.StringVar()
    # var_ddm_opt.set(max_element_in_list(list_ddm))

    opt_ddl_tab = tk.OptionMenu(frame_top_menu_opt, var_ddl_tab_opt, *list_ddl_table)
    opt_ddl_tab.config(width=30, font=('Calibri', 10))
    opt_ddl_tab.pack(side='top',anchor='w')

    opt_ddl_view = tk.OptionMenu(frame_top_menu_opt, var_ddl_view_opt, *list_ddl_view)
    opt_ddl_view.config(width=30, font=('Calibri', 10))
    opt_ddl_view.pack(side='top',anchor='w', pady=48)

    # opt_ddm = tk.OptionMenu(frame_top_menu_opt, var_ddm_opt, *list_ddm)
    # opt_ddm.config(width=30, font=('Calibri', 10))
    # opt_ddm.pack(side='top',anchor='w')


    list_sel = []
    var_ddl_tab = tk.BooleanVar()
    var_ddl_view = tk.BooleanVar()
    # var_ddm = tk.BooleanVar()
    choice_ddl_tab = tk.Checkbutton(frame_top_menu,
                                    image=icon,
                                    compound='right',
                                    font=('Calibri', 13),
                                    variable=var_ddl_tab, onvalue=True, offvalue=False,
                                    command=get_selection,
                                    )
    choice_ddl_view = tk.Checkbutton(frame_top_menu,
                                     image=icon,
                                     compound='left',
                                     font=('Calibri', 13)
                                     , variable=var_ddl_view, onvalue=True, offvalue=False,
                                     command=get_selection
                                     )
    # choice_ddm = tk.Checkbutton(frame_top_menu,
    #                             image=icon,
    #                             compound='left',
    #                             font=('Calibri', 13), variable=var_ddm, onvalue=True, offvalue=False,
    #                             command=get_selection
    #                             )

    choice_ddl_tab.pack(side='top', anchor='nw')
    choice_ddl_view.pack(side='top', anchor='w', pady=20)
    # choice_ddm.pack(side='top', anchor='sw')

    frame_bottom_menu.pack(side=tk.BOTTOM,padx=10,pady=10)

    button_run = tk.Button(frame_bottom_menu, text="RUN", relief='raised', command=gotorun)
    button_run.pack(side=tk.BOTTOM, anchor='se')


def main():
    global root \
        , icon \
        , image_exe_path

    root = tk.Tk()

    root.geometry('493x324')

    root.geometry('+400+250')

    # root.resizable(False, False)

    root.title('DDL Tool')


    image_exe_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'Image'),
                                  'icon-console.png')
    icon = PhotoImage(file=image_exe_path)


    menu()

    root.protocol("WM_DELETE_WINDOW", quit)

    root.mainloop()


if __name__ == '__main__':
    main()
