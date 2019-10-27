<html>
<style type="text/css">
.button {
  text-align: center;
  padding-top: 7px;
  padding-bottom: 7px;
  display: block;
  padding-right: 36px;
  padding-left: 36px;
  border: none;
  background-color: #EB232F;
  color: #FFFFFF;
  cursor: pointer;
}
input{
  font-family: muli, sans-serif;
  font-style: normal;
  font-weight: 300;
  font-size: 17px;
}
</style>
<body>
<h2>{{ question.question_text }}</h2>

{% for a in question.answer_set.all %}
	<?php echo {{a.answer_text}}; ?>
{% endfor %}
</body>
<html>
