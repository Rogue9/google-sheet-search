<!DOCTYPE html>
<html>
<head>
<title>Sheet Search</title>

<style>
body{
font-family:Arial;
margin:40px;
}

table{
border-collapse:collapse;
}

td,th{
border:1px solid #ccc;
padding:8px;
}
</style>

</head>

<body>

<h2>Google Sheet Search</h2>

<form method="post">
<input name="search" placeholder="Enter code (703, 723F, etc)">
<button type="submit">Search</button>
</form>

<br>

<table>

{% for row in results %}

<tr>
{% for cell in row %}
<td>{{cell}}</td>
{% endfor %}
</tr>

{% endfor %}

</table>

</body>
</html>
