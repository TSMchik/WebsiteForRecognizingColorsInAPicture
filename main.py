import numpy as np
from PIL import Image, ImageOps
from flask import Flask, render_template, request


def rgb_to_hex(rgb):
	return '%02x%02x%02x' % rgb


def give_most_hex(file_path, code):
	my_image = Image.open(file_path).convert('RGB')
	size = my_image.size
	if size[0] >= 400 or size[1] >= 400:
		my_image = ImageOps.scale(image=my_image, factor=0.2)
	elif size[0] >= 600 or size[1] >= 600:
		my_image = ImageOps.scale(image=my_image, factor=0.4)
	elif size[0] >= 800 or size[1] >= 800:
		my_image = ImageOps.scale(image=my_image, factor=0.5)
	elif size[0] >= 1200 or size[1] >= 1200:
		my_image = ImageOps.scale(image=my_image, factor=0.6)
	my_image = ImageOps.posterize(my_image, 2)
	# Первый шаг — это создание матрицы. Делаем это, используя метод массива NumPy,
	# и передаем в него изображение в качестве аргумента.
	image_array = np.array(my_image)

	# Затем мы создаем словарь, в котором,
	# ключи это цветовые кода, а значения этих ключей количества раз, когда они встречаются на
	# изображении. Сначала создаем пустой словарь. Пересеките матрицу изображения так же, как если бы перемещались
	# по двумерному списку. Для каждого элемента, найденного в матрице, если это значение уже существует в словаре в
	# качестве ключа, просто увеличиваем его значение на 1, если он не входит, добавьте этот элемент в качестве
	# ключа словаря и присвойте ему значение 1, так как мы впервые видим этот цвет.

	# создаем словарь уник цветов со счетчиком каждого цвета, равным 0 увеличивая счетчик на 1, если он есть в словаре
	unique_colors = {}  # (r, g, b): счетчик
	for column in image_array:
		for rgb in column:
			t_rgb = tuple(rgb)
			if t_rgb not in unique_colors:
				unique_colors[t_rgb] = 0
			if t_rgb in unique_colors:
				unique_colors[t_rgb] += 1

	# Используя метод sorted Python, который возвращает объект представления, похожий на список. Используем его,
	# передавая ему словарь unique_colors при вызове метода items словаря, который возвращает ключи и их значения в
	# виде кортежей. Второй аргумент — ключ, которому предоставляется лямбда-функция, которая просто возвращает ключи
	# и их значения, разделенные запятыми. Обратный аргумент, присвоенный значению true, означает, чтобы сортировка
	# происходила в порядке убывания. Поскольку sorted не возвращает словарь , используем метод dict,
	# чтобы преобразовать его в словарь.

	sorted_unique_colors = sorted(
		unique_colors.items(), key=lambda x: x[1],
		reverse=True)
	converted_dict = dict(sorted_unique_colors)
	# print(converted_dict)

	# получить только 10 самых высоких значений
	values = list(converted_dict.keys())
	# print(values)
	top_10 = values[0:10]
	# print(top_10)

	# код для преобразования RGB в HEX
	if code == 'hex':
		hex_list = []
		for key in top_10:
			hex = rgb_to_hex(key)
			hex_list.append(hex)
		return hex_list
	else:
		return top_10


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		f = request.files['file']
		colour_code = request.form['colour_code']
		colours = give_most_hex(f.stream, colour_code)
		return render_template('index.html', colors_list=colours, code=colour_code)
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True)
