<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>

<?php
    $conn = pg_connect("host=localhost port=5432 dbname=postgres user=postgres password=");
    $result = pg_query($conn, "SELECT * FROM users");

    $id = $_GET["id"];
    $category = $_GET["category"];

    $category1 = str_replace("'",'', $category);

    $model = $_GET["model"];

    $model1 = str_replace('\'','', $model);
    
    $price = $_GET["price"];
    $perf = $_GET["perf"];
    $activ = $_GET["activ"];

    $insertResult = pg_insert($conn, "computersetup_{$id}", array('type' => $category1, 'model' => $model1, 'price' => $price, 'perf' => $perf, 'activ' => $activ, 
    'motherboard' => 1, 'level' => 1));

?>