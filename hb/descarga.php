<?php
function downloadFile($url, $savePath) {
    $ch = curl_init($url);
    $fp = fopen($savePath, 'wb');
    if ($fp === false) {
        return false;
    }
    curl_setopt($ch, CURLOPT_FILE, $fp);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_FAILONERROR, true);
    curl_exec($ch);
    $err = curl_error($ch);
    curl_close($ch);
    fclose($fp);
    return $err === '';
}

$results = [];

$languages = [
    // 'S' => ['folder'=>'es', 'start'=>1101978051, 'count'=>125, 'label'=>'Español (S)'],
    // 'E' => ['folder'=>'en', 'start'=>1101978051, 'count'=>125, 'label'=>'Inglés (E)'],
    // 'T' => ['folder'=>'pt', 'start'=>1101978051, 'count'=>125, 'label'=>'Portugués (T)'],
    // 'X' => ['folder'=>'de', 'start'=>1101978051, 'count'=>125, 'label'=>'Alemán (X)'],
    // 'O' => ['folder'=>'nl', 'start'=>1101978051, 'count'=>125, 'label'=>'Holandés (O)'],
    'F' => ['folder'=>'fr', 'start'=>1101978051, 'count'=>125, 'label'=>'Francés (F)'],
    'I' => ['folder'=>'it', 'start'=>1101978051, 'count'=>125, 'label'=>'Italiano (I)'],
    'N' => ['folder'=>'no', 'start'=>1101978051, 'count'=>125, 'label'=>'Noruego (N)'],
    'P' => ['folder'=>'pl', 'start'=>1101978051, 'count'=>125, 'label'=>'Polaco (P)'],
    'R' => ['folder'=>'ru', 'start'=>1101978051, 'count'=>125, 'label'=>'Ruso (R)'],
    'S' => ['folder'=>'sv', 'start'=>1101978051, 'count'=>125, 'label'=>'Sueco (S)'],
    'U' => ['folder'=>'uk', 'start'=>1101978051, 'count'=>125, 'label'=>'Ucraniano (U)'],
];

$selectedLang = $_POST['lang'] ?? 'S';

$start_docid = $_POST['start_docid'] ?? $languages[$selectedLang]['start'];
$end_docid = $_POST['end_docid'] ?? ($languages[$selectedLang]['start'] + $languages[$selectedLang]['count'] - 1);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $start = intval($_POST['start_docid']);
    $end = intval($_POST['end_docid']);
    $lang = array_key_exists($_POST['lang'], $languages) ? $_POST['lang'] : 'S';

    $folder = $languages[$lang]['folder'];

    if ($start > 0 && $end >= $start) {
        for ($docid = $start; $docid <= $end; $docid++) {
            $apiUrl = "https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS?docid={$docid}&output=json&fileformat=MP3&alllangs=0&langwritten={$lang}&txtCMSLang={$lang}";

            $json = @file_get_contents($apiUrl);
            if ($json === false) {
                $results[$docid] = "No response or error";
                continue;
            }

            $data = json_decode($json, true);
            if (!$data || !isset($data['files'][$lang]['MP3'][0]['file']['url'])) {
                $results[$docid] = "No MP3 found";
                continue;
            }

            $mp3Url = $data['files'][$lang]['MP3'][0]['file']['url'];
            $filename = basename(parse_url($mp3Url, PHP_URL_PATH));
            $saveDir = __DIR__ . DIRECTORY_SEPARATOR . $folder;

            if (!is_dir($saveDir)) {
                mkdir($saveDir, 0777, true);
                chmod($saveDir, 0777);
            }

            $savePath = $saveDir . DIRECTORY_SEPARATOR . $filename;

            $downloaded = downloadFile($mp3Url, $savePath);
            $results[$docid] = $downloaded ? "Downloaded as {$folder}/{$filename}" : "Failed to download {$filename}";
        }
    } else {
        $results['error'] = "Rango inválido";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<title>Descargar MP3 JW - Selección de idioma y rango</title>
<script>
function updateRange() {
    const langs = <?= json_encode($languages) ?>;
    const select = document.getElementById('langSelect');
    const startInput = document.getElementById('start_docid');
    const endInput = document.getElementById('end_docid');
    const selected = select.value;

    if (langs[selected]) {
        startInput.value = langs[selected].start;
        endInput.value = langs[selected].start + langs[selected].count - 1;
    }
}
</script>
</head>
<body>
<h1>Descargar MP3 desde JW API (Multi idioma y rango)</h1>

<form method="post" action="">
    <label>Idioma:
      <select name="lang" id="langSelect" onchange="updateRange()">
        <?php foreach ($languages as $code => $info): ?>
          <option value="<?= htmlspecialchars($code) ?>" <?= ($code === $selectedLang) ? 'selected' : '' ?>>
            <?= htmlspecialchars($info['label']) ?>
          </option>
        <?php endforeach; ?>
      </select>
    </label><br><br>

    <label>DocID inicial: <input type="number" id="start_docid" name="start_docid" required min="1" value="<?= htmlspecialchars($start_docid) ?>" /></label><br><br>
    <label>DocID final: <input type="number" id="end_docid" name="end_docid" required min="1" value="<?= htmlspecialchars($end_docid) ?>" /></label><br><br>

    <button type="submit">Descargar MP3</button>
</form>

<?php if (!empty($results)): ?>
    <h2>Resultados:</h2>
    <ul>
        <?php foreach ($results as $docid => $msg): ?>
            <li><strong><?= is_int($docid) ? "DocID $docid" : htmlspecialchars($docid) ?>:</strong> <?= htmlspecialchars($msg) ?></li>
        <?php endforeach; ?>
    </ul>
<?php endif; ?>

<script>
document.addEventListener('DOMContentLoaded', () => {
    updateRange();
});
</script>

</body>
</html>
