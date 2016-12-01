<?php
require_once("../../../inc/init.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("img_url") and preg_match("/^[a-z_]+\.php/",$_REQUEST["img_url"]))
    face($_REQUEST["img_url"]);
else
    redirect("/IBSng/admin/graph");
    

function face($url)
{
    $smarty = new IBSSmarty();

    $smarty->assign("refresh_times",array(5,10,15,20,30,60));
    if(isset($_REQUEST['refresh']) && is_numeric($_REQUEST['refresh']))
       $smarty->assign("refresh_default",requestVal("refresh",15));
    else
        $smarty->assign("refresh_default",15);
    $smarty->assign("url",urlencode($url));
    $smarty->display("admin/graph/realtime.tpl");
}