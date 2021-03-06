<?php
require_once(dirname(__FILE__)."/common_functions.php");
require_once(dirname(__FILE__)."/globals.php");

if ($global_opened_db === FALSE) {
	if (open_db()) {
		$global_opened_db = TRUE;
	}
}

function replace_values_in_db_query_string($s_query, $a_values) {
	global $mysqli;

	foreach($a_values as $k=>$v) {
			$s_query = str_replace("[$k]", "[--$k--]", $s_query);
	}
	foreach($a_values as $k=>$v) {
			$s_query = str_replace("[--$k--]", $mysqli->real_escape_string($v), $s_query);
	}
	return $s_query;
}

function db_query($s_query, $a_values=NULL, $b_print_query = FALSE) {
	global $mysqli;

	if ($a_values !== NULL && gettype($a_values) == 'array')
			$s_query_string = replace_values_in_db_query_string($s_query, $a_values);
	else
			$s_query_string = $s_query;
	if ($b_print_query === TRUE || $b_print_query === 2)
			error_log($s_query_string);
	else if ($b_print_query === 1)
			echo $s_query_string;
	$wt_retval = $mysqli->query($s_query_string);
	if ($wt_retval === TRUE || $wt_retval === FALSE)
			return $wt_retval;
	$a_retval = array();
	while ($row = $wt_retval->fetch_assoc())
			$a_retval[] = $row;
	$wt_retval->free_result();
	return $a_retval;
}

function open_db() {
	global $global_opened_db;
	global $mysqli;

	if ($global_opened_db === TRUE) {
			return TRUE;
	}

	$a_configs = array();
	$filename = dirname(__FILE__)."/mysql_config.ini";
	if (file_exists($filename)) {
		$a_configs = parse_ini_file($filename);
	}
	if (!isset($a_configs["host"]) ||
		!isset($a_configs["user"]) ||
		!isset($a_configs["password"])) {
		return FALSE;
	}

	$mysqli = mysqli_connect($a_configs["host"], $a_configs["user"], $a_configs["password"]);
	if ($mysqli->connect_errno) {
		return FALSE;
	}
	$global_opened_db = TRUE;
	return TRUE;
}

// returns "`key1`='value1' AND `key2`='value2' AND ..."
function array_to_where_clause($a_vars) {
	global $mysqli;

	$a_where = array();
	foreach($a_vars as $k=>$v) {
			$k = $mysqli->real_escape_string($k);
			$v = $mysqli->real_escape_string($v);
			$a_where[] = "`$k`='$v'";
	}
	$s_where = implode(' AND ', $a_where);
	return $s_where;
}

// returns "(`key1`,`key2`,...) VALUES ('value1','value2',...)"
function array_to_set_clause($a_vars) {
	global $mysqli;

	$a_set = array();
	$a_values = array();
	foreach($a_vars as $k=>$v) {
			$k = $mysqli->real_escape_string($k);
			$v = $mysqli->real_escape_string($v);
			$a_set[] = $k;
			$a_values[] = $v;
	}
	$s_set = "(`".implode("`,`", $a_set)."`) VALUES ('".implode("','",$a_values)."')";
	return $s_set;
}

// returns "`key1`='[key1]', `key2`='[key2]'"
function array_to_update_clause($a_vars) {
	$a_retval = array();
	foreach($a_vars as $k=>$v)
			$a_retval[] = "`{$k}`='[{$k}]'";
	return implode(",", $a_retval);
}

// returns "(`key1`, `key2`, ...) VALUES ('[key1]', '[key2]', ...)"
function array_to_insert_clause($a_vars) {
	if (count($a_vars) == 0)
			return "";
	$a_keys = array();
	foreach($a_vars as $k=>$v)
			$a_keys[] = $k;
	return "(`".implode("`,`",$a_keys)."`) VALUES ('[".implode("]','[",$a_keys)."]')";
}

function create_row_if_not_existing($a_vars, $b_print_queries = FALSE) {
	// get the database, table, and properties
	$database = $a_vars['database'];
	$table = $a_vars['table'];
	$a_properties = $a_vars;
	foreach($a_properties as $k=>$v)
			if (in_array($k, array('database','table')))
					unset($a_properties[$k]);
	if (count($a_properties) == 0)
			return FALSE;
	// get the where and set strings
	$s_where = array_to_where_clause($a_properties);
	$s_set = array_to_set_clause($a_properties);
	// check if it exists
	$s_query_string = "SELECT `id` FROM `[database]`.`[table]` WHERE $s_where";
	$a_query_vars = array("database"=>$database, "table"=>$table);
	$a_result = db_query($s_query_string, $a_query_vars, $b_print_queries);
	if ($a_result !== NULL) {
			if (count($a_result) == 0) {
					$s_query_string = "INSERT INTO `[database]`.`[table]` $s_set";
					$a_query_vars = array_merge($a_properties, array("database"=>$database, "table"=>$table));
					$a_result = db_query($s_query_string, $a_query_vars, $b_print_queries);
					return TRUE;
			}
	}
	return FALSE;
}

?>
