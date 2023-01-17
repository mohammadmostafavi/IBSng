<?php




class Log{
    static function debug($message)
    {
        echo '<pre>';
        var_dump($message);
        echo '</pre>';
    }
    static function dd($var)
    {
        self::debug($var);
        die();
    }
}
