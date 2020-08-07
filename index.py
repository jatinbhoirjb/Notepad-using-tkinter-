from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont 
import tkinter
from tkinter.filedialog import *
ftar = None
ftts = None
word = ""
index=None
replaceWord= ""
class Notepad: 
	# default window width and height 
	root = Tk() 
	mainFont =tkFont.Font()
	mainFont.config(family="arial",size=14,weight="normal")
	ftts = None
	ftar=None
	thisWidth = 300
	thisHeight = 300
	thisTextArea = Text(root ,wrap=NONE,undo=True)
	thisMenuBar = Menu(root) 
	thisFileMenu= Menu(thisMenuBar, tearoff=0) 
	thisEditMenu = Menu(thisMenuBar, tearoff=0) 
	thisHelpMenu = Menu(thisMenuBar, tearoff=0)
	thisFormatMenu = Menu(thisMenuBar, tearoff=0)
	# To add scrollbar 
	YScrollBar = Scrollbar(thisTextArea,orient=tkinter.VERTICAL)	
	XScrollBar = Scrollbar(thisTextArea,orient=tkinter.HORIZONTAL) 
	file = None


	def __init__(self,**kwargs):
		#self.mainFont = Font
		#self.mainFont.config(family='arial', weight='normal', size=14)
		self.thisTextArea.config(font=self.mainFont)
		self.text_is_edited = False
		# Set icon 
		try: 
			self.root.wm_iconbitmap("Notepad.icon") 
		except: 
				pass
		# Set window size (the default is 300x300) 
		try: 
			self.thisWidth = kwargs['width'] 
		except KeyError: 
			pass
		try: 
			self.thisHeight = kwargs['height'] 
		except KeyError: 
			pass
		# Set the window text 
		self.root.title("Untitled - Notepad") 
		# Center the window 
		screenWidth = self.root.winfo_screenwidth() 
		screenHeight = self.root.winfo_screenheight() 
		# For left-alling 
		left = (screenWidth / 2) - (self.thisWidth / 2) 
		# For right-allign
		top = (screenHeight / 2) - (self.thisHeight /2) 
		# For top and bottom 
		self.root.geometry('%dx%d+%d+%d' % (self.thisWidth, self.thisHeight,left, top)) 
		# To make the textarea auto resizable 
		self.root.grid_rowconfigure(0, weight=1) 
		self.root.grid_columnconfigure(0, weight=1) 
		# Add controls (widget) 
		self.thisTextArea.grid(sticky = N + E + S + W) 
		# To open new file 
		self.thisFileMenu.add_command(label="New", command=self.newFile)	 
		# To open a already existing file 
		self.thisFileMenu.add_command(label="Open", command=self.openFile) 
		# To save current file 
		self.thisFileMenu.add_command(label="Save", command=self.saveFile)
		# To save current file as 
		self.thisFileMenu.add_command(label="Save As", command=self.saveAsFile)	 
		# To create a line in the dialog
		self.thisFileMenu.add_separator()										 
		self.thisFileMenu.add_command(label="Exit", command=self.quitApplication) 
		self.thisMenuBar.add_cascade(label="File", menu=self.thisFileMenu)	 
		# To give a feature of undo 
		self.thisEditMenu.add_command(label="Undo", command=self.undo)	 
		# To give a feature of redo 
		self.thisEditMenu.add_command(label="Redo", command=self.redo)
		self.thisEditMenu.add_separator()		 
		# To give a feature of cut 
		self.thisEditMenu.add_command(label="Cut", command=self.cut)			
		# to give a feature of copy	 
		self.thisEditMenu.add_command(label="Copy", command=self.copy)		 		
		# To give a feature of paste 
		self.thisEditMenu.add_command(label="Paste", command=self.paste)	 		
		# To give a feature of paste 
		self.thisEditMenu.add_command(label="Delete", command=self.delete)
		self.thisEditMenu.add_separator()
		# To give a feature of find 
		self.thisEditMenu.add_command(label="Find", command=self.FindAsk)
		# To give a feature of replace 
		self.thisEditMenu.add_command(label="Replace", command=self.ReplaceAsk)	
		# To give a feature of goto 
		self.thisEditMenu.add_command(label="Goto", command=self._goto_)		 		
		self.thisEditMenu.add_separator()		
		# To give a feature of select all 
		self.thisEditMenu.add_command(label="Select All", command=self.selectAll)	 
		# To give a feature of editing 
		self.thisMenuBar.add_cascade(label="Edit",menu=self.thisEditMenu)
		# To create a find function of the notepad 
		self.thisFormatMenu.add_command(label="Font", command=self.FontAsk) 
		self.thisMenuBar.add_cascade(label="Format", menu=self.thisFormatMenu) 
		self.root.config(menu=self.thisMenuBar) 	 		
		# To create a feature of description of the notepad 
		self.thisHelpMenu.add_command(label="About Notepad", command=self.showAbout) 
		self.thisMenuBar.add_cascade(label="Help", menu=self.thisHelpMenu) 

		self.XScrollBar.pack(side=BOTTOM,fill=X)
		self.YScrollBar.pack(side=RIGHT,fill=Y)					 		
		# Scrollbar will adjust automatically according to the content	
	 
		self.thisTextArea.config(xscrollcommand=self.XScrollBar.set) 
		self.thisTextArea.config(yscrollcommand=self.YScrollBar.set)
		self.XScrollBar.config(command = self.thisTextArea.xview)	 
		self.YScrollBar.config(command = self.thisTextArea.yview)
		self.thisTextArea.focus()
		#shortcuts
		self.thisTextArea.bind('<Control-s>', self.saveFile)
		self.thisTextArea.bind('<Control-f>', self.FindAsk)
		self.thisTextArea.bind('<Control-h>', self.ReplaceAsk)
		self.thisTextArea.bind('<Control-Shift-KeyPress-S>', self.saveAsFile)
		self.thisTextArea.bind('<Control-n>', self.newFile)
		self.thisTextArea.bind('<Control-c>', self.copy)
		self.thisTextArea.bind('<Control-v>', self.paste) 
		self.thisTextArea.bind('<Control-o>', self.openFile)
		self.thisTextArea.bind('<Control-a>', self.selectAll)
		self.thisTextArea.bind('<Control-z>', self.undo)
		self.thisTextArea.bind('<Control-y>', self.redo)
		self.thisTextArea.bind('<Key>', self.is_text_edited)
		self.thisTextArea.bind('<Any-Button>',self.reset_tags)
		self.thisTextArea.bind('<Button-3>',self._pop_up_) 
		self.thisTextArea.bind('<Control-g>',self._goto_) 
		#window closing listener
		self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
	def FontAsk(self,event=None):
		fofm =Toplevel(self.root)
		fofm.title('Find')
		fofm.geometry('{}x{}'.format(424, 440))	
		fofm.transient(self.root)
		font_1=tkFont.Font()
		font_1.config(family="arial",size=14,weight="normal")
		varFont =StringVar()
		varStyle =StringVar()
		varSize =StringVar()
		varFont.set(self.mainFont.actual('family'))
		varStyle.set(self.mainFont.actual('weight'))
		varSize.set(self.mainFont.actual('size'))
		Label(fofm, text = 'Font:').place(x=10,y=10)
		Label(fofm, text = 'Font Style').place(x=195,y=10)
		Label(fofm, text = 'Size:').place(x=340,y=10)
		top1 = Frame(fofm, width=170, height=140)
		top1.pack_propagate(False)
		top1.place(x=15,y=30)
		top2 = Frame(fofm, width=130, height=140)
		top2.pack_propagate(False)
		top2.place(x=200,y=30)
		top3 = Frame(fofm, width=63, height=130)
		top3.place(x=345,y=30)
		top3.pack_propagate(False)
		lbl = LabelFrame(fofm, text="Sample", width=208, height=90)
		lbl.place(x=200,y=190)
		lbl.pack_propagate(False)
		Label(lbl,text="AaBbYyZz",font=font_1).pack(fill = BOTH,expand=True,anchor='center')
		def out():
			#result=(self.var.get(), self.var1.get(), self.var2.get(), self.var3.get(), self.var4.get(), self.var5.get())
			self.mainFont['family']=varFont.get()
			self.mainFont['size']=varSize.get()
			self.mainFont['weight']=varStyle.get()
			fofm.destroy()
		btnOk = Button(fofm,text='OK', width = 10,height=1,relief="solid", bg='#C7C6C1', bd=1,command=out)
		btnOk.focus_set()
		btnOk.place(x=245,y=400)
		btnCancel = Button(fofm,text='Cancel', width = 10,height=1,relief="solid", bg='#C7C6C1', bd=1,command=lambda:fofm.destroy())
		btnCancel.place(x=330,y=400)
		
		#font 
		entFont = Entry(top1, textvariable=varFont)
		listFont = Listbox(top1,highlightthickness=0, exportselection=False)  
		scrFont = Scrollbar(top1)  
		entFont.pack(side = TOP, fill = BOTH) 
		scrFont.pack(side = RIGHT, fill = BOTH)  
		listFont.pack(side = LEFT, fill = BOTH, expand=True)
		for i in tkFont.families():
			listFont.insert(END, i)
		listFont.config(yscrollcommand = scrFont.set) 
		scrFont.config(command = listFont.yview)
		
		#style
		entStyle = Entry(top2, textvariable=varStyle)
		listStyle = Listbox(top2,highlightthickness=0, exportselection=False)  
		scrStyle = Scrollbar(top2)  
		entStyle.pack(side = TOP, fill = BOTH) 
		scrStyle.pack(side = RIGHT, fill = BOTH)  
		listStyle.pack(side = LEFT, fill = BOTH, expand=True)
		for i in ["normal","bold"]:
			listStyle.insert(END, i)
		listStyle.config(yscrollcommand = scrStyle.set) 
		scrStyle.config(command = listStyle.yview)
		
		#size
		entSize = Entry(top3, textvariable=varSize)
		listSize = Listbox(top3,highlightthickness=0, exportselection=False)  
		scrSize = Scrollbar(top3) 
		entSize.pack(side = TOP, fill = BOTH) 
		scrSize.pack(side = RIGHT, fill = BOTH)  
		listSize.pack(side = LEFT, fill = BOTH, expand=True)
		for values in [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]: 
			listSize.insert(END, values) 
		listSize.config(yscrollcommand = scrSize.set) 
		scrSize.config(command = listSize.yview)
		
		
		def fontSelect(event=None):
			try:
				varFont.set(str(listFont.get(listFont.curselection())))
				font_1.config(family=varFont.get(), weight=varStyle.get(), size=varSize.get())
			except:
				pass
		
		
		def styleSelect(event=None):
			try:
				varStyle.set(str(listStyle.get(listStyle.curselection())))
				font_1.config(family=varFont.get(), weight=varStyle.get(), size=varSize.get())
			except:
				pass
		
		
		def sizeSelect(event=None):
			try:
				varSize.set(int(listSize.get(listSize.curselection())))
				font_1.config(family=varFont.get(), weight=varStyle.get(), size=varSize.get())
			except:
				pass
		
		
		def on_focus_in(event):
			if event.widget==listFont:
				entFont.focus()
				entFont.selection_range(0, END)
			if event.widget==listStyle:
				entStyle.focus()
				entStyle.selection_range(0, END)
			if event.widget==listSize:
				entSize.focus()
				entSize.selection_range(0, END)
		def searched_Font(*args):
			search = varFont.get()
			for i,item in enumerate(all_Fonts):
				if search.lower() in item.lower():
					listFont.see(i)
					listFont.selection_set(i)
				else:
					listFont.selection_clear(i)
			if search == '':
				listFont.selection_clear(0, END)
		def searched_Style(*args):
			search = varStyle.get()
			for i,item in enumerate(all_Styles):
				if search.lower() in item.lower():
					listStyle.see(i)
					listStyle.selection_set(i)
				else:
					listStyle.selection_clear(i)
			if search == '':
				listStyle.selection_clear(0, END)

		def searched_Size(*args):
			try:
				search = int(varSize.get())
				for i,item in enumerate(all_Sizes):
					if item==search:
						listSize.selection_set(i)
						listSize.see(i)
					else:
						varSize.set(search)
						font_1.config(family=varFont.get(), weight=varStyle.get(), size=varSize.get())
						listSize.selection_clear(i)
					if search == '':
						listSize.selection_clear(0, END)
			except:
				pass
		
		entFont.focus()
		entFont.selection_range(0, END)
		varFont.trace('w', searched_Font)
		varStyle.trace('w', searched_Style)
		varSize.trace('w', searched_Size)
		listFont.bind('<<ListboxSelect>>', fontSelect)
		listStyle.bind('<<ListboxSelect>>', styleSelect)
		listSize.bind('<<ListboxSelect>>', sizeSelect)
		listFont.bind('<FocusIn>', on_focus_in)
		listStyle.bind('<FocusIn>', on_focus_in)
		listSize.bind('<FocusIn>', on_focus_in)
		all_Fonts = listFont.get(0, END)
		all_Styles = listStyle.get(0, END)
		all_Sizes = listSize.get(0,END)
		searched_Font()
		searched_Style()
		searched_Size()
	def quitApplication(self): 
		#exit
		self.root.destroy()  
	def showAbout(self):
		messagebox.showinfo("Notepad","Jatin Bhoir") 
	def openFile(self,event=None):
		self.file = askopenfilename(defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Documents","*.txt")]) 
		if self.file == "": 
			# no file to open 
			self.file = None
		else: 			
			# Try to open the file 
			# set the window title 
			self.root.title(os.path.basename(self.file) + " - Notepad") 
			self.thisTextArea.delete(1.0,END) 
			file = open(self.file,"r") 
			self.thisTextArea.insert(1.0,file.read()) 
			file.close() 		
	def newFile(self,event=None):
		self.root.title("Untitled - Notepad") 
		self.file = None
		self.thisTextArea.delete(1.0,END) 
	def saveFile(self,event=None):
		self.text_is_edited = False
		if self.file == None: 
			# Save as new file 
			self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")])
			if self.file == "":
				self.file = None
			else:
				# Try to save the file
				file = open(self.file,"w")
				file.write(self.thisTextArea.get(1.0,END)) 
				file.close() 				
				# Change the window title 
				self.root.title(os.path.basename(self.file) + " - Notepad") 			
		else: 
			file = open(self.file,"w")
			file.write(self.thisTextArea.get(1.0,END)) 
			file.close()
			self.root.title(os.path.basename(self.file) + " - Notepad") 

	def saveAsFile(self,event=None):
		self.text_is_edited = False
			# Save as new file 
		self.file = asksaveasfilename(initialfile=self.file, defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")]) 
		if self.file == "":
			self.file = None
		else: 				
			# Try to save the file 
			self.thisTextArea.edit_reset()
			file = open(self.file,"w") 
			file.write(self.thisTextArea.get(1.0,END)) 
			file.close() 				
			# Change the window title 
			self.root.title(os.path.basename(self.file) + " - Notepad") 

	def undo(self,event=None):
		try:
			self.thisTextArea.edit_undo()
		except:
			pass
	def redo(self,event=None):
		try:
			self.thisTextArea.edit_redo()
		except:
			pass
	def selectAll(self,event=None):
		self.thisTextArea.event_generate("<<SelectAll>>")
	def delete(self): 
		self.thisTextArea.event_generate("<<Clear>>")
	def cut(self): 
		self.thisTextArea.event_generate("<<Cut>>") 
	def copy(self,event=None): 
		self.thisTextArea.event_generate("<<Copy>>") 
	def paste(self,event=None): 
		self.thisTextArea.event_generate("<<Paste>>")

	def is_text_edited(self,event=None):
		if self.text_is_edited == False:
			self.text_is_edited = True
		else:
			if self.file is not None:
				msg = "*"+os.path.basename(self.file)+"- Notepad"
			else:
				msg = "*%s - Notepad"%("untitled document")
			self.root.title(msg)		

	def run(self): 
		self.root.mainloop()
	def on_closing(self):
		if self.text_is_edited == True:
			message = "Do you want to save ' %s ' before closing?"%(self.file or "this untitled document")
			res=messagebox.askyesnocancel('Notepad', message,default='yes')	
			if res == True :
				self.saveFile()
				self.root.destroy()
			elif res== False:
				self.root.destroy()
			else:
				pass
		else:
			self.root.destroy() 


	def FindAsk(self,event=None):
		dir = IntVar()
		def _search_():
			global index
			index = self.thisTextArea.index(INSERT)
			self.thisTextArea.tag_delete("search")
			if CheckVar2.get() == 1:
				word=str(entFind.get())
			else : 
				word=str(entFind.get()).strip(" ")
			if word:
				countvar =  StringVar()
				if dir.get()==2:
					f = self.thisTextArea.search(word, index , nocase= not(CheckVar1.get()))
					if not f:
						messagebox.showinfo("Notepad","cannot find "+"'"+word+"'")
						return
					starting_index =int(f.split(".")[0])
					ending_index  = len(word)+int(f.split(".")[1])
					coordinates = "{}.{}".format(starting_index, ending_index)
					self.thisTextArea.tag_add("search", f, coordinates)
					self.thisTextArea.tag_configure("search", background="skyblue", foreground="white")
					index = coordinates
					self.thisTextArea.mark_set("insert",index)
				if dir.get()==1:
					starting_index =int(index.split(".")[0])
					ending_index  = int(index.split(".")[1])-len(word)
					index = "{}.{}".format(starting_index, ending_index)
					f = self.thisTextArea.search(word,index ,backwards=True, nocase= not(CheckVar1.get()))
					if not f:
						messagebox.showinfo("Notepad","cannot find "+"'"+word+"'")
						return
					starting_index =int(f.split(".")[0])
					ending_index  = len(word)+int(f.split(".")[1])
					coordinates = "{}.{}".format(starting_index, ending_index)
					self.thisTextArea.tag_add("search", f, coordinates)
					self.thisTextArea.tag_configure("search", background="skyblue", foreground="white")
					index = coordinates
					#index= "{}.{}".format(starting_index, ending_index-len(word))
					self.thisTextArea.mark_set("insert",index)
		global word,ftar,ftts ,entFind
		if ftar is not None:
			ftar.destroy()
		if ftts is not None:
			ftts.destroy()
		ftts =Toplevel(self.root)
		ftts.title('Find')
		ftts.geometry('{}x{}'.format(355, 120))	
		ftts.transient(self.root)	
		Label(ftts, text = 'Find What:').place(x=5,y=10)
		entFind = Entry(ftts, width = 30,relief="solid", highlightbackground="grey", highlightcolor="RoyalBlue1", highlightthickness=1, bd=0)
		entFind.place(x=80,y=10)
		btnFind = Button(ftts,text='Find Next', width = 8,height=1,relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1, bg='light grey',command = _search_)
		btnFind.focus_set()
		btnFind.place(x=280,y=10)
		btnCancel = Button(ftts,text='Cancel', bg='light grey', width = 8,height=1,relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1,command=lambda:ftts.destroy()).place(x=280,y=40)
		ctr_mid = Frame(ftts, width=115, height=40, padx=3, pady=3, highlightbackground="grey",highlightthickness=1).place(x=150,y=45)
		Label(ftts, text = 'Direction').place(x=160,y=35)
		entFind.focus()
		CheckVar1 = IntVar()
		CheckVar2 = IntVar()
		Checkbutton(ftts, text = "Match case", variable = CheckVar1).place(x=5,y=65)
		Checkbutton(ftts, text = "Wrap around", variable = CheckVar2).place(x=5,y=90)
		ftts.resizable(0,0)
		dir.set(2)
		rdUp = Radiobutton(ftts, text='Up',variable=dir, value=1)
		rdDown = Radiobutton(ftts, text='Down',variable=dir, value=2)
		rdUp.place(x=155,y=55)
		rdDown.place(x=200,y=55)
		entFind.bind('<Any-Button>',self.reset_tags)
		try:
			entFind.insert(0,self.thisTextArea.selection_get())
			word=self.thisTextArea.selection_get()
		except TclError:
			entFind.insert(0,word)
		entFind.focus()
		entFind.selection_range(0, END)

	def _goto_(self,event=None):
		def _go_():
			line = entGoto.get()
			if int(line) >  (int(self.thisTextArea.index('end').split('.')[0]) - 1):
				messagebox.showinfo(" ","line number exceeds total line")
				return
			starting_index =line
			ending_index  = 0
			coordinates = "{}.{}".format(starting_index, ending_index)
			self.thisTextArea.mark_set("insert",coordinates)
			gtfm.destroy()
			self.thisTextArea.event_generate("<<LineEnd>>")
			self.thisTextArea.focus()
			
			
			
			
			
		
		def only_numbers(char):
			return char.isdigit()
	
		validation = self.root.register(only_numbers)
		gtfm = Toplevel(self.root)
		gtfm.title('Go To Line')
		gtfm.geometry('{}x{}'.format(250, 95))	
		gtfm.transient(self.root)
		Label(gtfm, text = 'Line number:').place(x=5,y=10)
		entGoto = Entry(gtfm, width = 36,relief="solid", highlightbackground="grey", highlightcolor="RoyalBlue1", highlightthickness=1, bd=0, validate="key", validatecommand=(validation, '%S'))
		entGoto.place(x=10,y=30)
		btnGoto = Button(gtfm,text='Go To', width = 9,height=1, bg='light grey',relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1,command=_go_)
		btnGoto.focus_set()
		btnGoto.place(x=80,y=60)
		btnCancel = Button(gtfm,text='Cancel', width = 9,height=1, bg='light grey',relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1,command=lambda:gtfm.destroy())
		btnCancel.place(x=160,y=60)
		#entGoto.bind("<Enter>", lambda event:btnGoto.invoke())
		gtfm.resizable(0,0)
		index = self.thisTextArea.index(INSERT)
		starting_index =int(index.split(".")[0])
		entGoto.insert(0,starting_index)
		entGoto.focus()
		entGoto.selection_range(0, END)




	def ReplaceAsk(self,event=None):
		def _search_all_():
			index="1.0"
			if CheckVar2.get() == 1:
				word=str(findText.get())
			else : 
				word=str(findText.get()).strip(" ")
			if word:
				while True:
					f = self.thisTextArea.search(word,index, stopindex = END,nocase = not(CheckVar1.get()))
					if not f:
						break
					starting_index =int(f.split(".")[0])
					ending_index  = len(word)+int(f.split(".")[1])
					coordinates = "{}.{}".format(starting_index, ending_index)
					self.thisTextArea.tag_add("search", f, coordinates)
					self.thisTextArea.tag_configure("search", background="RoyalBlue1",foreground='white')
					self.thisTextArea.tag_raise("sel")
					index = coordinates
				return True
			else:
				return None
		def _replace_all_():
			_search_all_()
			_replace_()
		def _search_():
			self.thisTextArea.tag_delete("search")
			index = self.thisTextArea.index(INSERT)
			if CheckVar2.get() == 1:
				word=str(findText.get())
			else : 
				word=str(findText.get()).strip(" ")
			if word:
				countvar =  StringVar()	
				f = self.thisTextArea.search(word,index, count=countvar,nocase= not(CheckVar1.get()))
				if not f:
					messagebox.showinfo("Notepad","cannot find "+"'"+word+"'");
					return
				starting_index = f
				ending_index = "{}+{}c".format(starting_index, countvar.get())
				self.thisTextArea.tag_add("search", starting_index, ending_index)
				self.thisTextArea.tag_configure("search", background="RoyalBlue1", foreground="white")
				index = ending_index
			self.thisTextArea.mark_set("insert",index)
			
			
		def _replace_():
			word = str(replaceText.get())	
			if word:
				coordinates=[]
				l=list(self.thisTextArea.tag_ranges("search"))
				l.reverse()
				while l:
					coordinates.append([l.pop(),l.pop()])
				for start, end in coordinates:
					self.thisTextArea.delete(start, end)
					self.thisTextArea.insert(start, word)
					ending_index = "{}+{}c".format(start,len(replaceText.get()))
					self.thisTextArea.tag_add("insert",start,ending_index)
					self.thisTextArea.tag_configure("insert", background="RoyalBlue1", foreground="white")
			return

		global ftar,ftts,word,replaceWord
		fields = {}
		if ftar is not None:
			ftar.destroy()
		if ftts is not None:
			ftts.destroy()
		ftar = Toplevel(self.root)
		ftar.title('Replace')
		ftar.transient(self.root)
		ftar.geometry('{}x{}'.format(355, 160))	
		Label(ftar,text= 'Find What:').place(x=5,y=10)
		findText = Entry(ftar, width = 30,relief="solid", highlightbackground="grey", highlightcolor="RoyalBlue1", highlightthickness=1, bd=0)
		findText.place(x=80,y=10)
		Label(ftar, text= 'Replace With:').place(x=5,y=40)
		replaceText = Entry(ftar, width = 30,relief="solid", highlightbackground="grey", highlightcolor="RoyalBlue1", highlightthickness=1, bd=0)
		replaceText.place(x=80,y=40)
		btnFind = Button(ftar,text='Find Next', width = 8,height=1, bg='light grey',relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1,command=_search_).place(x=280,y=10)
	
		btnReplace = Button(ftar,text='Replace', width = 8, bg='light grey',height=1,relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1,command = _replace_).place(x=280,y=40)
		fields['submit']=False
		btnReplaceAll = Button(ftar,text='Replace All', bg='light grey', width = 8,height=1,relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1,command = _replace_all_).place(x=280,y=70)
		btnCancel = Button(ftar,text='Cancel', width = 8,height=1, bg='light grey',relief="solid", highlightbackground="blue", highlightcolor="RoyalBlue1", bd=1,command=lambda:ftar.destroy()).place(x=280,y=100)
		CheckVar1 = IntVar()
		CheckVar2 = IntVar()
		Checkbutton(ftar, text = "Match case", variable = CheckVar1).place(x=5,y=105)
		Checkbutton(ftar, text = "Wrap around", variable = CheckVar2).place(x=5,y=130)
		ftar.resizable(0,0)
	
		findText.bind('<Any-Button>',self.reset_tags)
		try:
			findText.insert(0,self.thisTextArea.selection_get())
			word=self.thisTextArea.selection_get()
		except TclError:
			findText.insert(0,word)
		replaceText.insert(0,replaceWord)
		findText.focus()
		findText.selection_range(0, END)

	def _pop_up_(self,event=None):
		self.menu = tkinter.Menu(self.root,tearoff=0)
		self.menu.add_command(label="Undo", command=self.undo)
		self.menu.add_command(label="Redo", command=self.redo)
		self.menu.add_separator()	
		self.menu.add_command(label="Copy", command=self.copy)		
		self.menu.add_command(label="Cut", command=self.cut)
		self.menu.add_command(label="Paste", command=self.paste)
		self.menu.add_separator()
		self.menu.add_command(label="Select All", command=self.selectAll)
		self.menu.add_separator()	
		self.menu.tk_popup(event.x_root, event.y_root)

	def reset_tags(self,event=None):
		self.thisTextArea.tag_delete("insert")
		self.thisTextArea.tag_delete("search")
		return

# Run main application
if __name__ == '__main__':
	notepad = Notepad(width=800,height=400) 
	notepad.run() 	
