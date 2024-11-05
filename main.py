# Импортируем нужные библиотеки
import os
import cv2
import flet as ft

# Глобальная переменная для пути к файлу
global path
path = ''

# Функция для создания странички приложения
def main(page: ft.Page):
   # Устанавливаем заголовок странички и режим темы
   page.title = "Convector"
   page.theme_mode = 'dark'

   # Текстовое поле для отображения выбранных файлов
   selected_files = ft.Text()
   # Контейнер для отображения изображений
   images = ft.Row(expand=1, wrap=True, scroll="always")

   # Функция для обработки результата выбора файла
   def pick_result(e: ft.FilePickerResultEvent):
       if not e.files:
           selected_files.value = "Ничего не выбрано"
       else:
           selected_files.value = ''
           for el in e.files:
               if el.path:
                   selected_files.value += f"Файл выбран: {el.path}\n"
                   print(f"Выбранный файл: {el.path}")

   # Диалог выбора файлов и добавление его в страницу
   pick_dialog = ft.FilePicker(on_result=pick_result)
   page.overlay.append(pick_dialog)

   # Текстовое поле для ввода названия файла
   zzz = ft.TextField(value='Название файла', width=150)

   # Функция для конвертации изображения
   def convert(e):
       # Проверка на пустое название файла
       if not zzz.value.strip():
           selected_files.value = "Ошибка: введите название файла"
           page.update()
           return

       # Обработка каждого выбранного файла
       selected_files_text = selected_files.value.splitlines()
       for selected_file in selected_files_text:
           path = selected_file.split(": ")[1] if ": " in selected_file else ""
           if path:
               print(f"Путь к файлу перед загрузкой: {path}")
               png_img = cv2.imread(path)
               if png_img is None:
                   selected_files.value = "Ошибка: не удалось загрузить изображение"
                   print("Ошибка: не удалось загрузить изображение")
                   page.update()
                   return

               # Создание директории для сохраненных изображений
               save_dir = os.path.join(os.getcwd(), 'converted_images')
               os.makedirs(save_dir, exist_ok=True)
               # Путь для сохранения конвертированного изображения
               save_path = os.path.join(save_dir, f"{zzz.value}.jpg")
               cv2.imwrite(save_path, png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
               print(f"Изображение сохранено успешно: {save_path}")

               # Добавление изображения в контейнер
               img = ft.Image(
                   src=save_path,
                   width=100,
                   height=100,
                   fit=ft.ImageFit.CONTAIN,
               )
               images.controls.append(img)  # Добавление изображения в `Row`
               page.update()

       # Проверка, удалось ли добавить изображения
       if not images.controls:
           selected_files.value = "Ошибка: не удалось сохранить ни одно изображение"
           page.update()

   # Добавление элементов на страницу
   page.add(
       ft.Row(
           [
               ft.ElevatedButton(
                   'Выбрать файл',
                   icon=ft.icons.UPLOAD_FILE,
                   on_click=lambda _: pick_dialog.pick_files(allow_multiple=False)
               )
           ]
       ),
       ft.Row(
           [
               zzz,
               ft.TextButton('Convert', on_click=convert)
           ]
       ),
       ft.Row([selected_files]),
       images  # Добавление `Row` для изображений в страницу
   )

# Запуск приложения
ft.app(target=main)
