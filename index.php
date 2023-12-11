<?php
    if (isset($_POST["query"])) {
        $query = $_POST["query"];
        $script = 'backend.py';
        $output = shell_exec("python $script \"$query\"");
        if ($output !== null) {
            $ids = array_slice(explode("\n", $output), -4, 3);
        } else {
            echo "Error executing Python script.\n";
        }
    }
?>
<h1>YouTube Video Search</h1>
<form method="post">
    <input type="text" name="query" required>
    <input type="submit">
</form>
<?php
    if (isset($ids)) {
        foreach ($ids as $id) {
            echo "<iframe src=\"https://www.youtube.com/embed/$id\"></iframe>";
        }
    }
?>