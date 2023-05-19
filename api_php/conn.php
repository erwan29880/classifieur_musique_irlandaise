<?php 

abstract class Connexion
{
    private string $host_name = 'myHost';
    private string $database = 'Mydb';
    private string $user_name = 'myName';
    private string $password = 'myPass';

    private function connect()
    {
        return new mysqli($this->host_name, $this->user_name, $this->password, $this->database);
    }

    protected function getTunes($req): array
    {
        $link = $this->connect();
        $res = $link->query($req);
        
        $li = array();

        while ($enr = $res->fetch_row())
        {
            $li[] = array(
                'id' => $enr[0],
                'path' => $enr[1]
            );
        }
        return $li;
    }

    protected function getDevices()
    {
        $link = $this->connect();
        $res = $link->query("select device, path from pathes order by id;");
        
        $li = array();

        while ($enr = $res->fetch_row())
        {
            $li[] = array(
                'device' => $enr[0],
                'path' => $enr[1]
            );
        }
        return $li;
    }
}


?>