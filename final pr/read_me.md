Когда в родительськом блоке есть несколько (2+) float елментов он тнряет свои параметры высоты =0. Это решение
```
#contacts_page section::after{
	content: "";
	clear: both;
	display: block;
}
```