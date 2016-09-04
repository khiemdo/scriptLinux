define("BASE_PATH", "/var/www/codiad");
define("BASE_URL", "codiad.fnick2812.com");
define("THEME", "default");
define("WHITEPATHS", BASE_PATH . ",/home/gogs/gogsData");//user www-data in group gogs
$cookie_lifetime = "0";
date_default_timezone_set("Australia/Perth");
define("COMPONENTS", BASE_PATH . "/components");
define("PLUGINS", BASE_PATH . "/plugins");
define("THEMES", BASE_PATH . "/themes");
define("DATA", BASE_PATH . "/data");
define("WORKSPACE", BASE_PATH . "/workspace");

define("WSURL", BASE_URL . "/workspace");
