#почни тут створювати додаток з розумними замітками\
#

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QFormLayout, QInputDialog
import json
#
app = QApplication([])

notes = {
    'Ласкаво просимо!' : {
        'текст' : 'Ляля',
        'теги' : ['добро', 'інструкція']
    }
}
with open('notes_data.json', 'w') as file:
    json.dump(notes, file, sort_keys=True,ensure_ascii=False)


#
notes_win = QWidget()
notes_win.setWindowTitle("Розумні замітки")
notes_win.resize(900,600)
#
#
list_notes = QListWidget()#
list_notes_label = QLabel("Список замірок")

button_note_create = QPushButton("Створити замітку")
button_note_del = QPushButton("Видалити замітку")
button_note_save = QPushButton("Зберигти замітку")

field_text = QTextEdit()#
field_tag = QLineEdit()#
field_tag.setPlaceholderText("Введіть тег...")

list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")

button_tag_add = QPushButton("Додати до замітки")
button_tag_search = QPushButton("Шукати замітки по тегу")
button_tag_del = QPushButton("Відкріпити від замітки")

#
#
layuot_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(field_text)
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_2 = QHBoxLayout()
row_3 = QHBoxLayout()
row_4 = QHBoxLayout()
row_5 = QHBoxLayout()
row_6 = QHBoxLayout()

col_2.addLayout(row_1)#
col_2.addLayout(row_2)

row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2.addWidget(button_note_save)

row_3.addWidget(field_tag)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)

row_5.addWidget(button_tag_add)
row_5.addWidget(button_tag_search)
row_6.addWidget(button_tag_del)

col_2.addLayout(row_3)
col_2.addLayout(row_4)
col_2.addLayout(row_5)
col_2.addLayout(row_6)

layuot_notes.addLayout(col_1, stretch=2)#
layuot_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layuot_notes)#

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки: ")
    if ok and note_name !="":
        notes[note_name] = {"текст" :"", "теги" : []}
        list_notes.addItems(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для збереження не вибрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для збереження не вибрана!")


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка не вибрана!")


def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Замітка не вибрана!")



def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Шукати замітку по тегу")
    else:
        pass



button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
#
notes_win.show()
with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()
