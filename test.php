<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>

<?php



$conn = pg_connect("host=localhost port=5432 dbname=postgres user=postgres password=");
$result = pg_query($conn, "SELECT * FROM users");

echo "<table cellpadding=10 border=1>";

echo "<tr>
    <th>ID</th>
    <th>Username</th>
    <th>Cash</th>
</tr>";

while ($row = pg_fetch_row($result)) {
    echo "<tr>";

    echo "<td> $row[0] </td>";
    echo "<td> $row[1] </td>";
    echo "<td> $row[2] </td>";
    //echo "<td> <button type='button' class='btn btn-primary'> Continue </button> </td>";  
    echo "<td> <a href='getComputerSetup.php?id={$row[0]}'> Continue </a> </td>";  

    echo "</tr>";
  }

echo '</table>';


