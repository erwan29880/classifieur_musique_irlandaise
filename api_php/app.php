<?php
declare(strict_types=1);
include('conn.php');

class Data extends Connexion
{
    // return a json of 50 irish tunes 
    private string $tunes = "select id_irish, path_son from irish2 where vgg_11_14<0.5 order by rand() limit 50;";
    private string $airs = "select id_irish, path_son from irish2 where cnn2>0.5 and vgg_11_14>0.5 order by rand() limit 50;";
    private string $songs = "select id_irish, path_son from irish2 where vgg_11_14<0.5 order by rand() limit 50;";
    private $ids = array("instrus", "songs", "airs");
    private token = "mySecretToken";

    private function getIndexes($id)
    {
        // get ids and path from bdd
        return $this->getTunes($id);
    }

    public function getDevicesArray()
    {
        // get registred devices and path of music's folder
        return $this->getDevices();
    }

    private function veriGetPrefix(): bool
    {
        isset($_GET['prefix']) ? $cond = true : $cond = false;
        return $cond;
    }

    private function veriGetId(): bool
    {
        isset($_GET['id']) ? $cond = true : $cond = false;
        return $cond;
    }

    private function verifToken(): bool
    {
        if(isset($_GET['token'])) {
            $_GET['token']== $this->token ? $cond = true : $cond = false;
        } else {
            $cond = false;
        }
        return $cond;
    }

    private function path($prefix, $id): void
    {
        // format path 
        $newli = array();
        $prefix = $this->getPrefix($prefix);
        $tunes = $this->getIndexes($id);
        foreach ($tunes as $key => $value) {
            $path = str_replace('@', "'", $value['path']);
            $newli[] = array(
                "id" => $value['id'],
                "path" => $prefix.$path
            );
        }
        $json=json_encode($newli, JSON_PRETTY_PRINT);
        print($json);
    }

    private function noWay() 
    {
        // error function
        $newli = array("status"=> "error");
        $json=json_encode($newli, JSON_PRETTY_PRINT);
        print($json);
    }

    public function checkPrefix($id): bool 
    {
        // device registred ?
        $li = array();
        $devices = $this->getDevicesArray();
        foreach ($devices as $key => $value) {
            $li[] = $value['device'];
        }
        if(in_array($id, $li)) {
            return true;
        } else {
            return false;
        }
    }

    public function getPrefix($id): string
    {
        // from bdd
        if($this->checkPrefix($id) == true) {
            $devices = $this->getDevicesArray();
            $key = in_array($id, array_column( $devices, 'device'));
            return $devices[$key]['path'];
        } else {
            return "";
        }
    }


    public function run() 
    {
        $test_prefix = $this->veriGetPrefix();
        $test_token = $this->verifToken();
        $test_id = $this->veriGetId();
        if($test_token == true && $test_id == true) {
            $test_prefix == true ? $prefix = $this->getPrefix($_GET['prefix']) : $prefix = "";
            if ($_GET['id'] == "instrus") {
                $this->path($prefix, $this->tunes);
            } else if ($_GET['id'] == "airs") {
                $this->path($prefix, $this->airs);
            } else if ($_GET['id'] == "songs") {
                $this->path($prefix, $this->songs);
            } else {
                $this->noWay();
            }
        } else {
            $this->noWay();
        }

    }

}

$conn = new Data;
$conn->run();
?>
