<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>

<Script Language="JavaScript">
    var jsonData = ""

    function categoryChanged(jsonData) {
        catList = document.getElementById("categoryList")
        modelList = document.getElementById("modelList")
        modelList.innerHTML = ""

        category = catList.value

        var keys = []
        for(var k in jsonData[category])
        {
            opt = document.createElement("option")
            opt.innerText = k
            modelList.append(opt)
        }

        priceInput = document.getElementById("price")
        priceInput.value = 0

        perfInput = document.getElementById("perf")
        perfInput.value = 0


    }

    function modelChanged(jsonData) {
        catList = document.getElementById("categoryList")
        modelList = document.getElementById("modelList")

        category = catList.value
        model = modelList.value
        price = jsonData[category][model]["Цена"]
        perf = jsonData[category][model]["Производительность"]
        
        priceInput = document.getElementById("price")
        priceInput.value = price

        perfInput = document.getElementById("perf")
        perfInput.value = perf

    }
</Script>

<?php

$id = $_GET["id"];

$fn = fopen("assortment","r");


$resultAssortment = "";
  
while(! feof($fn))  {

    $resultAssortment .= fgets($fn);
}

//$resultAssortment = iconv("utf-8", "windows-1251", $resultAssortment);

fclose($fn);

for ($i = 0; $i <= 31; ++$i) { 
    $resultAssortment = str_replace(chr($i), "", $resultAssortment); 
}
$resultAssortment = str_replace(chr(127), "", $resultAssortment);

if (0 === strpos(bin2hex($resultAssortment), 'efbbbf')) {
    $resultAssortment = substr($resultAssortment, 3);
 }



$jsonData = json_decode($resultAssortment, true);

$ErrorMSG = json_last_error_msg();

$keys = array_keys($jsonData);
$modelArray = array();

foreach ($keys as $key)
    {
        echo $key;

        array_push($modelArray, $key."--------------");
        foreach (array_keys($jsonData[$key]) as $subitem)
        {    
            array_push($modelArray, $subitem);
            echo $subitem;
        }
    }
//echo $id;

$conn = pg_connect("host=localhost port=5432 dbname=postgres user=postgres password=");
$result = pg_query($conn, "SELECT * FROM computerSetup_{$id}");

echo "<table cellpadding=10 border=1>";

echo "<tr>
    <th>Type</th>
    <th>Model</th>
    <th>Price</th>
    <th>Perf</th>
    <th>Activ</th>
</tr>";

while ($row = pg_fetch_row($result)) {
    echo "<tr>";

    echo "<td> $row[0] </td>";
    echo "<td> $row[1] </td>";
    echo "<td> $row[2] </td>";
    echo "<td> $row[3] </td>";
    echo "<td> $row[4] </td>";
    echo "<td> <button type='button' class='btn btn-primary'> Delete </button> </td>";  
    //echo "<td> <a href='getComputerSetup.php?id={$row[0]}'> Continue </a> </td>";  

    echo "</tr>";
  }

echo '</table>';

echo "<br>";

echo "<table cellpadding=10 border=1>";

echo "<tr>";
echo "<td> <p>Type</p>";
echo "<select onchange='categoryChanged({$resultAssortment})' id='categoryList'>";

foreach ($keys as $key)
    echo "<option>{$key}</option>";

echo "</select>";
echo  "</td>";



echo "<td> <p>Model</p>";
echo "<select onchange='modelChanged({$resultAssortment})' id='modelList'>";

echo "<option>------------</option>";

echo "</select>";
echo  "</td>";

echo "<td> <p>Price</p> <input id='price' value = 0> </td>";
echo "<td> <p>Perf</p> <input  id='perf' value = 0> </td>";

echo "<td> <p>Activ</p> <input id='activ' value = 0> </td>";
echo "</tr>";

echo "</table>";


echo "<td> <button type='button' class='btn btn-primary'> Add component </button> </td>"; 