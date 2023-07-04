import tkinter as tk
from tkinter import messagebox
from pypinyin import lazy_pinyin, Style


class ContactListApp:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        # 主窗口标题名称
        self.root.title("通讯录管理系统")
        # 用于存储联系人信息
        self.contacts = []

        # 从文件中读取联系人信息
        with open("联系人.txt", "r") as f:
            # 对于文件中的每一行
            for line in f:
                # 去掉行末的空格并按照逗号分割字段
                fields = line.strip().split(",")
                # 如果字段数量不为3，则跳过当前行
                if len(fields) != 3:
                    continue
                # 将字段分别赋值给name、phone和email变量
                name, phone, email = fields
                # 将联系人信息作为元组添加到self.contacts列表中
                self.contacts.append((name, phone, email))

        # 搜索框
        # 创建一个搜索框的框架，将框架放在主窗口的顶部，水平方向填满
        search_frame = tk.Frame(self.root)
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        # 在搜索框架中添加一个“搜索：”的标签
        search_label = tk.Label(search_frame, text="搜索：")
        search_label.pack(side=tk.LEFT)
        # 创建一个字符串变量用于存储搜索框中的输入，并为其设置回调函数，当该变量发生变化时调用刷新联系人列表的方法
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode, sv=self.search_var: self.refresh_contact_list())
        # 在搜索框架中添加一个文本框，并将其与上面创建的字符串变量绑定，在文本框中输入时展示相关联系人
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 添加联系人按钮
        # 点击按钮执行add_windowa函数
        add_button = tk.Button(self.root, text="添加联系人", command=self.add_window)
        add_button.pack()

        # 联系人列表滑动窗口，以可滑动的列表形式展示联系人
        self.listbox = tk.Listbox(self.root, height=20, font=("Arial", 25))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 将列表中的每个项目绑定到 show_contact 方法，双击联系人展示详细信息
        self.listbox.bind("<Double-Button-1>", self.show_contact)

        # 添加滑动窗口的滚动条，放置在最右侧，竖向填满
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # 将滚动条绑定到联系人列表，实现滑动效果
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # 创建字母导航栏
        alphabet_frame = tk.Frame(self.root)
        alphabet_frame.pack(side=tk.LEFT, fill=tk.Y)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letter_buttons = []
        # 创建字母按钮，点击按钮调用jump_to_letter函数
        for letter in alphabet:
            letter_button = tk.Button(alphabet_frame, text=letter, width=1, height=1, font=("Arial", 8),
                                      command=lambda l=letter: self.jump_to_letter(l))
            letter_button.pack(fill=tk.X)
            self.letter_buttons.append(letter_button)

        # 刷新列表
        self.refresh_contact_list()

    def add_window(self):
        """
          实现添加联系人的窗口
        """
        # 初始化添加联系人窗口
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("添加联系人")
        self.add_window.geometry("300x200")

        # 姓名输入框
        # 标签
        name_label = tk.Label(self.add_window, text="姓名：")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        # 姓名变量
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(self.add_window, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        # 设置光标默认在姓名输入框上
        name_entry.focus()

        # 电话输入框
        phone_label = tk.Label(self.add_window, text="电话：")
        phone_label.grid(row=1, column=0, padx=10, pady=10)
        self.phone_var = tk.StringVar()
        phone_entry = tk.Entry(self.add_window, textvariable=self.phone_var)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)

        # 邮箱输入框
        email_label = tk.Label(self.add_window, text="邮箱：")
        email_label.grid(row=2, column=0, padx=10, pady=10)
        self.email_var = tk.StringVar()
        email_entry = tk.Entry(self.add_window, textvariable=self.email_var)
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        # 添加按钮，点击调用add_contact函数
        add_button = tk.Button(self.add_window, text="添加", command=self.add_contact)
        add_button.grid(row=3, column=1, padx=10, pady=10)

    def add_contact(self):
        """
          实现添加联系人
        """
        # 从输入获取姓名电话和邮箱三个信息
        name = self.name_var.get()
        phone = self.phone_var.get().strip()
        email = self.email_var.get()
        # 判断号码长度是否正确，不正确弹出提示错误信息
        if not phone.isdigit() or len(phone) != 11:
            messagebox.showerror("错误", "请输入正确的11位手机号码！")
            return
        # 姓名和电话不为空
        if name and phone:
            # 将信息添加到contacts中
            self.contacts.append((name, phone, email))
            self.add_window.destroy()

            # 将联系人信息写入文件
            with open("联系人.txt", "a") as f:
                f.write(f"{name},{phone},{email}\n")
            # 更新联系人列表
            self.refresh_contact_list()

    def refresh_contact_list(self):
        """
           刷新联系人列表，包括搜索时展示相关联系人还有刷新字母导航栏按钮状态
                """

        # 获取搜索框输入
        search_text = self.search_var.get()
        # 清空列表框中的所有元素
        self.listbox.delete(0, tk.END)
        # 将联系人列表按照拼音的首字母进行排序，并赋值给变量sorted_contacts。
        sorted_contacts = sorted(self.contacts, key=lambda x: lazy_pinyin(x[0], style=Style.FIRST_LETTER)[0])
        # 判断搜索框中的文本是否在当前遍历到的联系人的姓名或电话中，如果是，将当前遍历到的联系人的姓名插入到列表框中
        for contact in sorted_contacts:
            if search_text.lower() in contact[0].lower() or search_text in contact[1]:
                self.listbox.insert(tk.END, contact[0])
        # 根据联系人列表的首字母设置字母导航栏按钮的状态
        # 获取联系人姓名的首字母
        first_letters = [lazy_pinyin(contact[0], style=Style.FIRST_LETTER)[0].upper() for contact in sorted_contacts]
        # 首字母存在，按钮可点击，否则不可点击
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            if letter in first_letters:
                self.letter_buttons[i].config(state=tk.NORMAL)
            else:
                self.letter_buttons[i].config(state=tk.DISABLED)

    def show_contact(self, event):
        """
           展示联系人详细信息，并添加了修改和删除按钮
                """
        # 获取当前选中的联系人，根据选中的姓名匹配展示相应信息
        selected_name = self.listbox.get(self.listbox.curselection())
        for contact in self.contacts:
            if contact[0] == selected_name:
                selected_contact = contact
                # 创建新窗口并显示联系人详细信息
                self.contact_details_window = tk.Toplevel(self.root)
                self.contact_details_window.title("联系人详情")
                self.contact_details_window.geometry("200x120")
                # 展示姓名电话和邮箱
                name_label = tk.Label(self.contact_details_window, text=f"姓名：{selected_contact[0]}")
                name_label.grid(row=0, column=0, sticky="W")
                phone_label = tk.Label(self.contact_details_window, text=f"电话：{selected_contact[1]}")
                phone_label.grid(row=1, column=0, sticky="W")
                email_label = tk.Label(self.contact_details_window, text=f"邮箱：{selected_contact[2]}")
                email_label.grid(row=2, column=0, sticky="W")
                # 添加修改和删除按钮
                # 点击修改按钮，调用修改函数
                edit_button = tk.Button(self.contact_details_window, text="修改",
                                        command=lambda: self.edit_contact(selected_contact))
                edit_button.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
                # 点击删除按钮，调用删除函数
                delete_button = tk.Button(self.contact_details_window, text="删除",
                                          command=lambda: self.delete_contact(selected_contact))
                delete_button.grid(row=3, column=1, pady=10, stick=tk.E)
                break

    def edit_contact(self, contact):
        """
            实现修改联系人信息
                        """
        # 初始化修改联系人窗口
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("修改联系人")
        self.edit_window.geometry("300x200")
        # 姓名输入框
        name_label = tk.Label(self.edit_window, text="姓名：")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        self.edit_name_var = tk.StringVar(value=contact[0])
        name_entry = tk.Entry(self.edit_window, textvariable=self.edit_name_var)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.focus()
        # 电话输入框
        phone_label = tk.Label(self.edit_window, text="电话：")
        phone_label.grid(row=1, column=0, padx=10, pady=10)
        self.edit_phone_var = tk.StringVar(value=contact[1])
        phone_entry = tk.Entry(self.edit_window, textvariable=self.edit_phone_var)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        # 邮箱输入框
        email_label = tk.Label(self.edit_window, text="邮箱：")
        email_label.grid(row=2, column=0, padx=10, pady=10)
        self.edit_email_var = tk.StringVar(value=contact[2])
        email_entry = tk.Entry(self.edit_window, textvariable=self.edit_email_var)
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        # 保存按钮，点击后调用保存函数
        save_button = tk.Button(self.edit_window, text="保存", command=lambda: self.save_contact(contact))
        save_button.grid(row=3, column=1, padx=10, pady=10, sticky=tk.E)
        # 取消按钮，点击可退出修改窗口
        cancel_button = tk.Button(self.edit_window, text="取消", command=self.edit_window.destroy)
        cancel_button.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

    def save_contact(self, contact):
        """
           验证修改后的信息是否合法，不合法给出提示信息，合法则修改并将修改后的信息写入文件
                        """
        # 保存联系人信息
        name = self.edit_name_var.get()
        phone = self.edit_phone_var.get().strip()
        email = self.edit_email_var.get()
        # 检查手机号是否为11位
        if not phone.isdigit() or len(phone) != 11:
            messagebox.showerror("错误", "请输入正确的11位手机号码！")
            return
        if name and phone:
            index = self.contacts.index(contact)
            self.contacts[index] = (name, phone, email)
            self.edit_window.destroy()

            # 将修改后的联系人信息写入文件
            with open("联系人.txt", "w") as f:
                for contact in self.contacts:
                    f.write(f"{contact[0]},{contact[1]},{contact[2]}\n")
            # 更新联系人列表
            self.refresh_contact_list()

    def delete_contact(self, contact):
        """
           删除功能
                        """
        # 弹出提示框，询问是否删除联系人
        answer = messagebox.askyesno("删除联系人", "是否删除该联系人？")
        if answer:
            # 删除联系人信息
            self.contacts.remove(contact)
            self.contact_details_window.destroy()

            # 将删除后的联系人信息写入文件
            with open("联系人.txt", "w") as f:
                for contact in self.contacts:
                    f.write(f"{contact[0]},{contact[1]},{contact[2]}\n")

            self.refresh_contact_list()

    def jump_to_letter(self, letter):
        """
           跳转功能，实现点击字母导航栏跳转到与之匹配的联系人
                        """
        # 跳转到指定字母开头的联系人
        for i in range(self.listbox.size()):
            name = self.listbox.get(i)
            if lazy_pinyin(name, style=Style.FIRST_LETTER)[0].lower() == letter.lower():
                # 滚动列表框，使当前选定的联系人可见。
                self.listbox.see(i)
                # 清除之前选定的联系人
                self.listbox.selection_clear(0, tk.END)
                # 选定当前联系人
                self.listbox.selection_set(i)
                break

    def run(self):
        # 运行应用程序
        self.root.mainloop()


app = ContactListApp()
app.run()
