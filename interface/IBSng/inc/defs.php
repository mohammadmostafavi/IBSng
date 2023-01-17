<?php


define("DATE_TYPE","gregorian"); //gregorian or jalali, this can be overide per request/session
define("MONEY_UNIT","UNITS");
define("DEFAULT_LANGUAGE","en");
define("TimeZone","Asia/Tehran");


define("IBSNG_VERSION","P3.24");


define("IBS_ROOT",dirname(getcwd(), 3)."/");
define("INTERFACE_ROOT",IBS_ROOT."interface/");
//define("INTERFACE_ROOT","/var/www/html/");
define("IMAGES_ROOT",INTERFACE_ROOT."IBSng/images/");

define("JPGRAPH_ROOT",INTERFACE_ROOT."jpgraph/");

define("XMLRPCINC",INTERFACE_ROOT."xmlrpc/");

define("IBSINC",INTERFACE_ROOT."IBSng/inc/");

define("SMARTY_ROOT",INTERFACE_ROOT."smarty/");
define("SMARTY_DIR",SMARTY_ROOT."libs/");

define("XMLRPC_SERVER_IP","127.0.0.1");
define("XMLRPC_SERVER_PORT","1235");
define("XMLRPC_TIMEOUT",240);
