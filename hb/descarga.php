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
    'X' => ['folder'=>'de','name'=>'alemán','vernacular'=>'Deutsch','mp3'=>125],
    'AN' => ['folder'=>'cat','name'=>'catalán','vernacular'=>'català','mp3'=>125],
    'CR' => ['folder'=>'ht','name'=>'criollo haitiano','vernacular'=>'Kreyòl ayisyen','mp3'=>125],
    'S' => ['folder'=>'es','name'=>'español','vernacular'=>'español','mp3'=>125],
    'GL' => ['folder'=>'kl','name'=>'groenlandés','vernacular'=>'Kalaallisut','mp3'=>125],
    'MO' => ['folder'=>'ho','name'=>'hiri motu','vernacular'=>'Hiri Motu','mp3'=>125],
    'HM' => ['folder'=>'hmn','name'=>'hmong (blanco)','vernacular'=>'Hmoob Dawb','mp3'=>125],
    'E' => ['folder'=>'en','name'=>'inglés','vernacular'=>'English','mp3'=>125],
    'O' => ['folder'=>'nl','name'=>'neerlandés','vernacular'=>'Nederlands','mp3'=>125],
    'SB' => ['folder'=>'sr-cyrl','name'=>'serbio (alfabeto cirílico)','vernacular'=>'српски (ћирилица)','mp3'=>125],
    'SI' => ['folder'=>'th','name'=>'tailandés','vernacular'=>'ไทย','mp3'=>125],
    'MP' => ['folder'=>'tpi','name'=>'tok pisin','vernacular'=>'Tok Pisin','mp3'=>125],
    'AW' => ['folder'=>'tsc','name'=>'tshwa','vernacular'=>'ciTshwa','mp3'=>125],
    'ZU' => ['folder'=>'zu','name'=>'zulú','vernacular'=>'IsiZulu','mp3'=>125],
    'GI' => ['folder'=>'gug','name'=>'guaraní','vernacular'=>'guarani','mp3'=>123],
    'T' => ['folder'=>'pt','name'=>'portugués de Brasil','vernacular'=>'Português (Brasil)','mp3'=>123],
    'TB' => ['folder'=>'tum','name'=>'chitumbuka','vernacular'=>'Chitumbuka','mp3'=>122],
    'CW' => ['folder'=>'bem','name'=>'cibemba','vernacular'=>'Cibemba','mp3'=>119],
    'YA' => ['folder'=>'yao','name'=>'chiyao','vernacular'=>'Chiyao','mp3'=>59],
    'AF' => ['folder'=>'af','name'=>'afrikáans','vernacular'=>'Afrikaans','mp3'=>0],
    'AL' => ['folder'=>'sq','name'=>'albanés','vernacular'=>'shqip','mp3'=>0],
    'AM' => ['folder'=>'am','name'=>'amárico','vernacular'=>'አማርኛ','mp3'=>0],
    'AE' => ['folder'=>'as','name'=>'asamés','vernacular'=>'অসমীয়া','mp3'=>0],
    'AJ' => ['folder'=>'az-cyrl','name'=>'azerí (alfabeto cirílico)','vernacular'=>'Aзәрбајҹан (кирил әлифбасы)','mp3'=>0],
    'BI' => ['folder'=>'bcl','name'=>'becol','vernacular'=>'Bicol','mp3'=>0],
    'BE' => ['folder'=>'bn','name'=>'bengalí','vernacular'=>'বাংলা','mp3'=>0],
    'BU' => ['folder'=>'my','name'=>'birmano','vernacular'=>'မြန်မာ','mp3'=>0],
    'CV' => ['folder'=>'ceb','name'=>'cebuano','vernacular'=>'Cebuano','mp3'=>0],
    'CN' => ['folder'=>'ny','name'=>'chichewa','vernacular'=>'Chichewa','mp3'=>0],
    'CH' => ['folder'=>'cmn-hant','name'=>'chino mandarín (tradicional)','vernacular'=>'中文繁體（國語）','mp3'=>0],
    'CK' => ['folder'=>'cjk','name'=>'chokue','vernacular'=>'Chokwe','mp3'=>0],
    'CU' => ['folder'=>'cv','name'=>'chuvacho','vernacular'=>'чӑвашла','mp3'=>0],
    'SN' => ['folder'=>'si','name'=>'cingalés','vernacular'=>'සිංහල','mp3'=>0],
    'KO' => ['folder'=>'ko','name'=>'coreano','vernacular'=>'한국어','mp3'=>0],
    'SC' => ['folder'=>'crs','name'=>'criollo de las Seychelles','vernacular'=>'Kreol Seselwa','mp3'=>0],
    'DG' => ['folder'=>'ada','name'=>'dangme','vernacular'=>'Dangme','mp3'=>0],
    'LF' => ['folder'=>'dhv','name'=>'dehu','vernacular'=>'Drehu','mp3'=>0],
    'JL' => ['folder'=>'dyu','name'=>'diula','vernacular'=>'Jula','mp3'=>0],
    'EF' => ['folder'=>'efi','name'=>'efik','vernacular'=>'Efịk','mp3'=>0],
    'OD' => ['folder'=>'ng','name'=>'endonga','vernacular'=>'Oshindonga','mp3'=>0],
    'NZ' => ['folder'=>'nzi','name'=>'enzema','vernacular'=>'Nzema','mp3'=>0],
    'SV' => ['folder'=>'sv','name'=>'esloveno','vernacular'=>'slovenščina','mp3'=>0],
    'ST' => ['folder'=>'et','name'=>'estonio','vernacular'=>'eesti','mp3'=>0],
    'EW' => ['folder'=>'ee','name'=>'ewe','vernacular'=>'Eʋegbe','mp3'=>0],
    'FR' => ['folder'=>'fo','name'=>'feroés','vernacular'=>'Føroyskt','mp3'=>0],
    'FI' => ['folder'=>'fi','name'=>'finlandés','vernacular'=>'suomi','mp3'=>0],
    'FN' => ['folder'=>'fj','name'=>'fiyiano','vernacular'=>'vakaViti','mp3'=>0],
    'F' => ['folder'=>'fr','name'=>'francés','vernacular'=>'Français','mp3'=>0],
    'GE' => ['folder'=>'ka','name'=>'georgiano','vernacular'=>'ქართული','mp3'=>0],
    'EG' => ['folder'=>'guw','name'=>'gun','vernacular'=>'Gungbe','mp3'=>0],
    'HV' => ['folder'=>'hil','name'=>'hiligaynon','vernacular'=>'Hiligaynon','mp3'=>0],
    'HI' => ['folder'=>'hi','name'=>'hindi','vernacular'=>'हिंदी','mp3'=>0],
    'IB' => ['folder'=>'ig','name'=>'ibo','vernacular'=>'Igbo','mp3'=>0],
    'IL' => ['folder'=>'ilo','name'=>'ilocano','vernacular'=>'Iloko','mp3'=>0],
    'IN' => ['folder'=>'id','name'=>'indonesio','vernacular'=>'Indonesia','mp3'=>0],
    'IS' => ['folder'=>'iso','name'=>'isoko','vernacular'=>'Isoko','mp3'=>0],
    'I' => ['folder'=>'it','name'=>'italiano','vernacular'=>'Italiano','mp3'=>0],
    'KJ' => ['folder'=>'kln','name'=>'kalenjin','vernacular'=>'Kalenjin','mp3'=>0],
    'KA' => ['folder'=>'kn','name'=>'kannada','vernacular'=>'ಕನ್ನಡ','mp3'=>0],
    'KD' => ['folder'=>'kqn','name'=>'kaonde','vernacular'=>'Kikaonde','mp3'=>0],
    'KR' => ['folder'=>'ksw','name'=>'karen sgaw','vernacular'=>'ကညီ(စှီၤ)ကျိာ်','mp3'=>0],
    'AZ' => ['folder'=>'kk','name'=>'kazajo','vernacular'=>'қазақ','mp3'=>0],
    'GK' => ['folder'=>'kek','name'=>'kekchí','vernacular'=>'q’eqchi’','mp3'=>0],
    'KG' => ['folder'=>'kwy','name'=>'kikongo','vernacular'=>'Kikongo','mp3'=>0],
    'KQ' => ['folder'=>'ki','name'=>'kikuyu','vernacular'=>'Gĩkũyũ','mp3'=>0],
    'KU' => ['folder'=>'lu','name'=>'kiluba','vernacular'=>'Kiluba','mp3'=>0],
    'RU' => ['folder'=>'run','name'=>'kirundi','vernacular'=>'Ikirundi','mp3'=>0],
    'KI' => ['folder'=>'kss','name'=>'kisi','vernacular'=>'Kisiei','mp3'=>0],
    'YW' => ['folder'=>'rw','name'=>'kiñaruanda','vernacular'=>'Ikinyarwanda','mp3'=>0],
    'KY' => ['folder'=>'kj','name'=>'kwanyama','vernacular'=>'Oshikwanyama','mp3'=>0],
    'LT' => ['folder'=>'lv','name'=>'letón','vernacular'=>'latviešu','mp3'=>0],
    'LO' => ['folder'=>'luo','name'=>'luo','vernacular'=>'Dholuo','mp3'=>0],
    'MC' => ['folder'=>'mk','name'=>'macedonio','vernacular'=>'македонски','mp3'=>0],
    'ML' => ['folder'=>'ms','name'=>'malayo','vernacular'=>'Melayu','mp3'=>0],
    'MY' => ['folder'=>'ml','name'=>'malayálam','vernacular'=>'മലയാളം','mp3'=>0],
    'MZ' => ['folder'=>'mam','name'=>'mam','vernacular'=>'mam','mp3'=>0],
    'RA' => ['folder'=>'rar','name'=>'maorí de las Islas Cook','vernacular'=>'Kuki Airani','mp3'=>0],
    'MR' => ['folder'=>'mr','name'=>'maratí','vernacular'=>'मराठी','mp3'=>0],
    'ME' => ['folder'=>'men','name'=>'mendé','vernacular'=>'Mɛnde','mp3'=>0],
    'MX' => ['folder'=>'mco','name'=>'mixe medio','vernacular'=>'ayuk','mp3'=>0],
    'LS' => ['folder'=>'lus','name'=>'mizo','vernacular'=>'Mizo','mp3'=>0],
    'MM' => ['folder'=>'mos','name'=>'more','vernacular'=>'Moore','mp3'=>0],
    'NP' => ['folder'=>'ne','name'=>'nepalés','vernacular'=>'नेपाली','mp3'=>0],
    'NN' => ['folder'=>'niu','name'=>'niueano','vernacular'=>'Faka-Niue','mp3'=>0],
    'NK' => ['folder'=>'nyk','name'=>'nyaneka','vernacular'=>'Nyaneka','mp3'=>0],
    'OA' => ['folder'=>'om','name'=>'oromo','vernacular'=>'Afaan Oromoo','mp3'=>0],
    'PN' => ['folder'=>'pag','name'=>'pangasinán','vernacular'=>'Pangasinan','mp3'=>0],
    'PR' => ['folder'=>'fa','name'=>'persa','vernacular'=>'فارسی','mp3'=>0],
    'SP' => ['folder'=>'pis','name'=>'pidgin de las islas Salomón','vernacular'=>'Solomon Islands Pidgin','mp3'=>0],
    'QU' => ['folder'=>'quz','name'=>'quechua cuzqueño','vernacular'=>'quechua (Cusco)','mp3'=>0],
    'SM' => ['folder'=>'sm','name'=>'samoano','vernacular'=>'Faa-Samoa','mp3'=>0],
    'SG' => ['folder'=>'sg','name'=>'sango','vernacular'=>'Sango','mp3'=>0],
    'SU' => ['folder'=>'st','name'=>'sesoto de Lesoto','vernacular'=>'Sesotho (Lesotho)','mp3'=>0],
    'TN' => ['folder'=>'tn','name'=>'setsuana','vernacular'=>'Setswana','mp3'=>0],
    'DM' => ['folder'=>'sid','name'=>'sidama','vernacular'=>'Sidaamu Afoo','mp3'=>0],
    'SW' => ['folder'=>'sw','name'=>'suajili','vernacular'=>'Kiswahili','mp3'=>0],
    'SR' => ['folder'=>'srn','name'=>'surinamés','vernacular'=>'Sranantongo','mp3'=>0],
    'TG' => ['folder'=>'tl','name'=>'tagalo','vernacular'=>'Tagalog','mp3'=>0],
    'TL' => ['folder'=>'ta','name'=>'tamil','vernacular'=>'தமிழ்','mp3'=>0],
    'TJ' => ['folder'=>'tg','name'=>'tayiko','vernacular'=>'тоҷикӣ','mp3'=>0],
    'TU' => ['folder'=>'te','name'=>'telugu','vernacular'=>'తెలుగు','mp3'=>0],
    'TV' => ['folder'=>'tiv','name'=>'tivo','vernacular'=>'Tiv','mp3'=>0],
    'TO' => ['folder'=>'to','name'=>'tongano','vernacular'=>'Faka-Tonga','mp3'=>0],
    'TK' => ['folder'=>'tr','name'=>'turco','vernacular'=>'Türkçe','mp3'=>0],
    'VI' => ['folder'=>'tyv','name'=>'tuviniano','vernacular'=>'тыва','mp3'=>0],
    'TW' => ['folder'=>'tw','name'=>'twi','vernacular'=>'Twi','mp3'=>0],
    'UG' => ['folder'=>'ug-cyrl','name'=>'uigur (alfabeto cirílico)','vernacular'=>'Уйғур (кирилл йезиғи)','mp3'=>0],
    'UB' => ['folder'=>'umb','name'=>'umbundu','vernacular'=>'Umbundu','mp3'=>0],
    'WO' => ['folder'=>'wo','name'=>'uolof','vernacular'=>'Wolof','mp3'=>0],
    'UZ' => ['folder'=>'uz-cyrl','name'=>'uzbeko','vernacular'=>'ўзбекча','mp3'=>0],
    'WA' => ['folder'=>'wls','name'=>'wallisiano','vernacular'=>'Faka\'uvea','mp3'=>0],
    'SA' => ['folder'=>'war','name'=>'waray-waray','vernacular'=>'Waray-Waray','mp3'=>0],
    'WY' => ['folder'=>'guc','name'=>'wayúunaiki','vernacular'=>'Wayuunaiki','mp3'=>0],
    'YR' => ['folder'=>'yo','name'=>'yoruba','vernacular'=>'Yorùbá','mp3'=>0],
    'RT' => ['folder'=>'ttj','name'=>'ñoro-tooro','vernacular'=>'Rutoro','mp3'=>0],
];

$selectedLang = $_POST['lang'] ?? 'S';

$start_docid = $_POST['start_docid'] ?? 1101978051;
$end_docid = $_POST['end_docid'] ?? 1101978175;

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
        startInput.value = 1101978051;
        endInput.value = 1101978175;
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
            <?= htmlspecialchars($info['vernacular']) ?> (<?= htmlspecialchars($info['folder']) ?>)<?= $info['mp3'] ? '' : ' — sin MP3' ?>
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
